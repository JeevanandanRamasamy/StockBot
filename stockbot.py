from http.client import MOVED_PERMANENTLY
import os
import discord
import pymongo
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient

#load env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
API_KEY = os.getenv('API_KEY')

bot = commands.Bot(command_prefix = '$')

# Database setup
cluster = MongoClient("mongodb+srv://stockbot:XLoy90B9uUYMCkZf@stockbot.t61sf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["stockbot"]
collection = db["users"]

# helper functions
# function that returns a user from the database given its id 
def get_user_db(id):
    return collection.find_one({"_id": id})

# method returns the amount of stocks of the stock desired to sell and the index of that stock in the portfolio array
def has_x_stock(user, stock):
    for i in range(0, len(user['portfolio'])):
        if (user['portfolio'][i]['stock_symbol'] == stock):
            return [user['portfolio'][i]['stock_qty'], i]
    return [-1, -1]

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
    if message.content == 'test':
        await message.channel.send('Testing 1 2 3!')
    await bot.process_commands(message)


@bot.command(help = 'Set a new balance')
async def setBalance(ctx, bal):
    user_id = ctx.message.author.id
    user_name = ctx.message.author.name
    user = get_user_db(user_id)
    # If user already exists, locate the user and change the balance
    if user:
        collection.update_one(user, {"$set": {"balance": float(bal)}})
    # If not create a new user
    else:
        user = {"_id": user_id, "name": user_name, "balance": float(bal), "portfolio": []}
        collection.insert_one(user)
    await ctx.send(f'{user_name}, your balance was set to ${bal}')

@bot.command(help = 'Returns your current balance')
async def getBalance(ctx):
    user = get_user_db(ctx.message.author.id)
    if user:
        msg = f"{user['name']}, your balance is: ${user['balance']}"
    else: 
        msg = f"{user['name']}, set a balance first."
    await ctx.send(msg)

@bot.command(help = 'Adds the stock to your account and subtracts cost from balance if you have sufficient funds')
async def buy(ctx, num, stock):
    user_id = ctx.message.author.id
    user = get_user_db(user_id)

    if (not user): 
        await ctx.send("You don't have a balance to purchase stocks!")
        return
    
    num = int(num)
    balance = user['balance']

    response = requests.get(f'https://api.twelvedata.com/price?symbol={stock}&apikey={API_KEY}')
    price = float(json.loads(response.text)['price'])

    if (balance < num * price):
        await ctx.send('Unable to buy stock (Not enough funds)')
        return

    collection.update_one(user, {"$set": {'balance': user['balance'] - (price*num)}})
    # add the stock to the portfolio of the user
    newStock = {
        "stock_qty": num,
        "stock_symbol": stock
    }
    collection.update_one({'_id': ctx.message.author.id}, {'$push': {'portfolio': newStock}})
    await ctx.send(f"{user['name']} bought {num} shares of {stock}")

@bot.command(help = 'Removes the stock from your account and adds current stock price to balance if you own the stock')
async def sell(ctx, num, stock):
    #parsing num into an integer
    num = int(num)
    user_id = ctx.message.author.id
    user = get_user_db(user_id)
    if (not user): 
        await ctx.send("You don't have stocks to sell!")
    balance = user['balance']

    # destructure qty and index of stock to sell
    stock_qty, stock_index = has_x_stock(user, stock)

    # If user doesn't have any stock or less than the amount trying to sell
    if (stock_qty == -1 or stock_qty < num):
        print(stock_qty)
        await ctx.send(f"{user['name']}, unable to sell stock (You do not own {num} of this stock)")
        return
    
    # If selling all shares, remove stock from portfolio
    if (stock_qty == num):
        collection.update_one({"_id": user_id}, {"$pull": { 'portfolio': { 'stock_symbol': stock } }})
    else:
        # If selling less than all shares, just decrease stock_qty
        collection.update_one({"_id": user_id}, {"$set": { f'portfolio[{stock_index}]': { 'stock_qty': stock_qty - num } }})

    response = requests.get(f'https://api.twelvedata.com/price?symbol={stock}&apikey={API_KEY}')
    price = float(json.loads(response.text)['price'])

    collection.update_one(user, {"$set": {"balance": balance + (num * price)}})

    await ctx.send(f"{user['name']} sold {num} {stock}")

@bot.command(help = 'Lists some suggested stocks that you can buy')
async def listStocks(ctx):
    await ctx.send('AAPL, MSFT, GOOG, AMZN, TSLA, BRK.A, NVDA, FB, UNH, V, JNJ, WMT, JPM, PG, MA, XOM, BAC, CVX, HD, BABA')

@bot.command(help = 'Lists stocks that you bought along with your balance')
async def showPortfolio(ctx):
    user = get_user_db(ctx.message.author.id)
    embed = discord.Embed(title = 'Stock Portfolio')
    embed.add_field(name = 'User', value = user['name'])
    embed.add_field(name = 'Balance', value = user['balance'])
    s = ''
    portfolio = user['portfolio']
    for stock in portfolio:
        s += str(stock['stock_qty']) + ' ' + stock['stock_symbol'] + ', '
    embed.add_field(name = 'Stocks', value = s[:-2])
    await ctx.send(embed = embed)

@bot.command(help = 'Add given quantity to your current balance')
async def deposit(ctx, qty):
    user = get_user_db(ctx.message.author.id)
    user['balance'] += float(qty)
    await ctx.send(f"{user['name']}, added ${qty} to your balance. Your new balance is ${user['balance']}")

@bot.command(help = 'reset the balance') 
async def reset(ctx):
    userId = ctx.message.author.id
    # delete data from this user from the DB
    collection.delete_one({"_id" : userId})
    await ctx.channel.send('Balance and operations were reset')

bot.run(TOKEN)