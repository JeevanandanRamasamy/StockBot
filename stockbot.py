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

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
    if message.content == 'test':
        await message.channel.send('Testing 1 2 3!')
    await bot.process_commands(message)

@bot.command(help = 'Changes your current balance to the amount specified')
async def setBalance(ctx, bal):
    balance = bal
    await ctx.send(f'Balance changed to ${bal}')

@bot.command(help = 'Returns your current balance')
async def getBalance(ctx):
    await ctx.send(balance)

@bot.command(help = 'Adds the stock to your account and subtracts cost from balance if you have sufficient funds')
async def buy(ctx, num, stock):
    balance = 10000.0
    response = requests.get(f'https://api.twelvedata.com/price?symbol={stock}&apikey=a8b0b60da8d84235a0da19805b2552f3')
    price = float(json.loads(response.text)['price'])
    if balance >= int(num) * price:
        balance -= int(num) * price
    else:
        await ctx.send('Unable to buy stock (Not enough funds)')

@bot.command(help = 'Removes the stock from your account and adds current stock price to balance if you own the stock')
async def sell(ctx, num, stock):
    response = requests.get(f'https://api.twelvedata.com/price?symbol={stock}&apikey=a8b0b60da8d84235a0da19805b2552f3')
    if int(num) <= user.stock.amount:
        balance += int(num) * float(response.text)
    else:
        await ctx.send(f'Unable to sell stock (You do not own {num} of this stock)')

@bot.command(help = 'Lists some suggested stocks that you can buy')
async def listStocks(ctx):
    await ctx.send('AAPL, MSFT, GOOG, AMZN, TSLA, BRK.A, NVDA, FB, UNH, V, JNJ, WMT, JPM, PG, MA, XOM, BAC, CVX, HD, BABA')

@bot.command(help = 'Lists stocks that you bought along with your balance')
async def showPortfolio(ctx):
    embed = discord.Embed(title = 'Stock Portfolio')
    embed.add_field(name = 'User', value = ctx.message.author.name)
    balance = 10000
    embed.add_field(name = 'Balance', value = balance)
    s = ''
    stocks = [{'num': 2, 'symbol': 'AAPL'}, {'num': 3, 'symbol': 'TSLA'}, {'num': 1, 'symbol': 'FB'}]
    for stock in stocks:
        s += str(stock['num']) + ' ' + stock['symbol'] + ', '
    embed.add_field(name = 'Stocks', value = s[:-2])
    await ctx.send(embed = embed)

bot.run(TOKEN)
