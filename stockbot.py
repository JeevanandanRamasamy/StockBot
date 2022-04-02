import os
import discord
import pymongo
from dotenv import load_dotenv
from discord.ext import commands
from pymongo import MongoClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix = '$')
#cluster = MongoClient('CONNECTION_URL')

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
    if message.content == 'test':
        await message.channel.send('Testing 1 2 3!')
    await bot.process_commands(message)

@bot.command(help = 'Returns your current balance')
async def setBalance(ctx, bal):
    balance = bal
    await ctx.send(f'Balance changed to ${bal}')

@bot.command(help = 'Returns your current balance')
async def getBalance(ctx):
    await ctx.send(balance)

@bot.command(help = 'Adds the stock to your account and subtracts cost from balance if you have sufficient funds')
async def buy(ctx, num, stockName):
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

bot.run(TOKEN)
