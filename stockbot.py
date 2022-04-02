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
STARTINGBALANCE = 0

bot = commands.Bot(command_prefix = '$')

# Database setup
cluster = MongoClient("mongodb+srv://stockbot:XLoy90B9uUYMCkZf@stockbot.t61sf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["stockbot"]
collection = db["users"]

# helper functions
# function that returns a user from the database given its id 
def get_user_db(id):
    return collection.find_one({"_userID": id})

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
    # If user already exists, locate the user and change the balance
    userId = ctx.message.author.id;
    user = get_user_db(userId);
    if user:
        collection.update_one(user, {"$set": {"balance": float(bal)}})
    # If not create a new user
    else:
        user = {"_userID": userId, "balance": float(bal), "portfolio": {}}
        collection.insert_one(user);
    
    await ctx.send(f'Balance set to ${bal}')

@bot.command(help = 'Returns your current balance')
async def getBalance(ctx):
    userId = ctx.message.author.id
    userName = ctx.message.author.name
    # If the user exists, retrieve the user balance
    user = get_user_db(userId)
    if user:  # check if user exists
        balance = user['balance']
        msg = f'Your balance is: ${balance}'
    else: 
        msg = f'{userName}, set a balance first.'
    await ctx.send(msg)

@bot.command(help = 'Adds the stock to your account and subtracts cost from balance if you have sufficient funds')

async def buy(ctx, num, stock):
    userId = ctx.message.author.id
    user = collection.find_one({"_userID": userId})
    if user:
        balance = float(user['balance'])
    
    num = int(num)

    response = requests.get(f'https://api.twelvedata.com/price?symbol={stock}&apikey=a8b0b60da8d84235a0da19805b2552f3')
    price = float(json.loads(response.text)['price'])

    if balance >= num * price:
        collection.update_one(user, {"$set": {'balance': balance - (price*num)}})

        # add stock
        # add the stock to the portfolio of the user
        portfolio = user['portfolio']
        portfolio[f'{stock}'] = num

        collection.update_one(user, {"$set": {'portfolio': portfolio}})
        msg = f'Bought {num} shares of {stock}'

    else:
        msg = 'Unable to buy stock (Not enough funds)'
    await ctx.send(msg)

@bot.command(help = 'Removes the stock from your account and adds current stock price to balance if you own the stock')
async def sell(ctx, num, stock):
    #parsing num into an integer
    num = int(num)
    userId = ctx.message.author.id; 
    user = get_user_db(userId)
    portfolio = get_user_db(userId)['portfolio']
    stocks_qty = get_stocks_qty(stock, portfolio)
    balance = user['balance']

    response = requests.get(f'https://api.twelvedata.com/price?symbol={stock}&apikey=a8b0b60da8d84235a0da19805b2552f3')
    price = float(json.loads(response.text)['price'])

    if num <= 3:
        collection.update_one(user, {"$set": {"balance": balance + (num * price)}})
        msg = f'Sold {num} {stock}'
    else:
        msg = f'Unable to sell stock (You do not own {num} of this stock)'
    await ctx.send(msg)

@bot.command(help = 'reset the balance') 
async def reset(ctx):
    userId = ctx.message.author.id;
    # delete data from this user from the DB
    collection.delete_one({"_userID" : userId})
    await ctx.channel.send('Balance and operations were reset')

@bot.command(help = 'Lists some suggested stocks that you can buy')
async def listStocks(ctx):
    await ctx.send('AAPL, MSFT, GOOG, AMZN, TSLA, BRK.A, NVDA, FB, UNH, V, JNJ, WMT, JPM, PG, MA, XOM, BAC, CVX, HD, BABA')

@bot.command(help = 'Lists stocks that you bought along with your balance')
async def showPortfolio(ctx):
    user = get_user_db(ctx.messsage.author.id)
    embed = discord.Embed(title = 'Stock Portfolio')
    embed.add_field(name = 'User', value = ctx.message.author.name)
    balance = user['balance']
    embed.add_field(name = 'Balance', value = balance)
    s = ''
    stocks = [{'num': 2, 'symbol': 'AAPL'}, {'num': 3, 'symbol': 'TSLA'}, {'num': 1, 'symbol': 'FB'}]
    for stock in stocks:
        s += str(stock['num']) + ' ' + stock['symbol'] + ', '
    embed.add_field(name = 'Stocks', value = s[:-2])
    await ctx.send(embed = embed)

bot.run(TOKEN)



