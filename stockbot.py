import os
import discord
import pymongo
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

#cluster = MongoClient('CONNECTION_URL')

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
    userId = ctx.message.author.id;
    # If user already exists, locate the user and change the balance
    user = collection.find_one({"_userID": userId})
    if user:
        collection.update_one({"_userID": userId}, {"$set": {"balance": bal}})
    # If not create a post
    else:
        post = {"_userID": userId, "balance": bal}
        await collection.insert_one(post);
    
    await ctx.send(f'Balance set to ${bal}')

@bot.command(help = 'Returns your current balance')
async def getBalance(ctx):
    userId = ctx.message.author.id
    userName = ctx.message.author.name
    # If the user exists, retrieve the user balance
    user = collection.find_one({'_userID': userId})
    if user:  # check if user exists
        balance = user['balance']
        msg = f'Your balance is: ${balance}'
    else: 
        msg = f'{userName}, set a balance first.'
    await ctx.send(msg)

@bot.command(help = 'Adds the stock to your account and subtracts cost from balance if you have sufficient funds')
async def buy(ctx, num, stockName):
    userId = ctx.message.author.id;
    balance = collection.find_one({'_userID:': userId})['balance']
    if (balance >= num * stockName.getPrice()):
        balance -= num * stockName.getPrice()
    else:
        await ctx.channel.send('Unable to buy stock (Not enough funds)')

@bot.command(help = 'Removes the stock from your account and adds current stock price to balance if you own the stock')
async def sell(ctx, num, stockName):
    if (num <= user.stock.amount):
        balance += num * stockName.getPrice()
    else:
        await ctx.channel.send(f'Unable to sell stock (You do not own {num} of this stock)')

@bot.command(help = 'reset the balance') 
async def reset(ctx):
    userId = ctx.message.author.id;
    # delete data from this user from the DB
    collection.delete_one({"_userID" : userId})
    await ctx.channel.send('Balance and operations were reset')

bot.run(TOKEN)
