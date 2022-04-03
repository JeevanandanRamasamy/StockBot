from http.client import MOVED_PERMANENTLY
import os
import discord
import pymongo
import requests
import json
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


bot = commands.Bot(command_prefix = '$')

# Database setup
cluster = MongoClient("mongodb+srv://stockbot:XLoy90B9uUYMCkZf@stockbot.t61sf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["stockbot"]
collection = db["users"]

# helper functions
# function that returns a user from the database given its id 
def get_user_db(id):
    return collection.find_one({"_id": id})

def get_stocks_qty(stockSymbol, portfolio):
    for i in range(0, len(portfolio)):
        if portfolio[i]["stock_symbol"] is stockSymbol:
            return portfolio[i]["shares_qty"]
    return


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
        user = {"_id": user_id, "balance": float(bal), "portfolio": []}
        collection.insert_one(user)
    await ctx.send(f'{user_name}, your balance was set to ${bal}')

@bot.command(help = 'Returns your current balance')
async def getBalance(ctx):
    user_name = ctx.message.author.name
    user = get_user_db(ctx.message.author.id)
    msg = f'{user_name}, '
    # If the user exists, retrieve the user balance
    if user:  # check if user exists
        balance = user['balance']
        msg =+ f'your balance is: ${balance}'
    else: 
        msg =+ f'{user_name}, set a balance first.'
    await ctx.send(msg)

@bot.command(help = 'Adds the stock to your account and subtracts cost from balance if you have sufficient funds')
async def buy(ctx, num, stock):
    num = int(num)
    user_id = ctx.message.author.id
    user_name = ctx.message.author.name
    user = get_user_db(user_id)
    if user:
        balance = user['balance']

    response = requests.get(f'https://api.twelvedata.com/price?symbol={stock}&apikey=a8b0b60da8d84235a0da19805b2552f3')
    price = float(json.loads(response.text)['price'])

    if (balance < num * price):
        await ctx.send('Unable to buy stock (Not enough funds)')
        return

    collection.update_one(user, {"$set": {'balance': balance - (price*num)}})
    # add the stock to the portfolio of the user
    newStock = {
        "stock_qty": num,
        "stock_symbol": stock
    }
    collection.update_one({'_id': ctx.message.author.id}, {'$push': {'portfolio': newStock}})
    await ctx.send(f'{user_name} bought {num} shares of {stock}')


@bot.command(help = 'Removes the stock from your account and adds current stock price to balance if you own the stock')
async def sell(ctx, num, stock):
    #parsing num into an integer
    num = int(num)
    user = get_user_db(ctx.message.author.id)
    portfolio = user['portfolio']
    stocks_qty = get_stocks_qty(stock, portfolio)
    balance = user['balance']

    # If selling all shares, remove stock from portfolio

    # If selling less than all shares, just decrease stock_qty

    response = requests.get(f'https://api.twelvedata.com/price?symbol={stock}&apikey=a8b0b60da8d84235a0da19805b2552f3')
    price = float(json.loads(response.text)['price'])

    if num <= user['portfolio'].any("stock" == stock):
        collection.update_one(user, {"$set": {"balance": balance + (num * price)}})
        msg = f'Sold {num} {stock}'
    else:
        msg = f'Unable to sell stock (You do not own {num} of this stock)'
    await ctx.send(msg)

@bot.command(help = 'reset the balance') 
async def reset(ctx):
    # delete data from this user from the DB
    collection.delete_one({"_id" : ctx.message.author.id})
    await ctx.channel.send('Balance and operations were reset')

@bot.command(help = 'Lists some suggested stocks that you can buy')
async def listStocks(ctx):
    await ctx.send('AAPL, MSFT, GOOG, AMZN, TSLA, BRK.A, NVDA, FB, UNH, V, JNJ, WMT, JPM, PG, MA, XOM, BAC, CVX, HD, BABA')

@bot.command(help = 'Lists stocks that you bought along with your balance')
async def showPortfolio(ctx):
    user = get_user_db(ctx.message.author.id)
    embed = discord.Embed(title = 'Stock Portfolio')
    embed.add_field(name = 'User', value = ctx.message.author.name)
    balance = user['balance']
    embed.add_field(name = 'Balance', value = balance)
    s = ''
    portfolio = user['portfolio']
    for stock in portfolio:
        s += str(stock['stock_qty']) + ' ' + stock['stock_symbol'] + ', '
    embed.add_field(name = 'Stocks', value = s[:-2])
    await ctx.send(embed = embed)


bot.run(TOKEN)



