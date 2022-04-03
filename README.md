# StockBot

A DiscordBot that allows users to buy stocks of possible companies from an API. Every user has a starting balance, and it is up to the user to make sure that they are investing in stocks in companies that succeed in order to make profit that they can add in their balance; otherwise, they will lose money from their balance if companies fail. When a user invests in a company, they will receive a stock in return.

## How to run the Discord bot
1. Fork the repository or download the code in Github.
2. Open the folder of the code. 
3. Install all dependencies using (I'll get to that later)

## Features
- Database of User's portfolios
- Getting the user ID
- A user has a stock or not
    - Checking the user's portfolio if the user has a stock based on looking at the symbol.
- Setting a balance for the user.
    - If the user exists in the database, then set the user's balance to some fixed number. 
    - Else, create a new user, set it's balance, and add that user to the database.
- Getting the balance for the user.
- Buy the stock(s)
    - Add the stock(s) to the amount of stocks bought from a company that you bought the stock(s) from.
    - Subtract the money you paid to buy the stock(s) from balance. 
    - If you do not have enough money in your balance to buy the stock(s), then you can't buy. 
 - Sell the stock(s)
    - Removes the stocks from the amount of stocks.
    - Add the money paid from the stocks bought to the balance.
    - If you don't have any stocks or if the number of stocks you own is less than the number of stocks you wanna sell for that company, then
    the user is unable to sell the stock. 
    - If the user sells all of his shares for a company, remove that company from the user's portfolios. 
- List of possible stocks from the API
- Show portfolio
    - List of stocks the user bought along with the updated balance after buying the stocks.  
- Deposit money to user's balance
- Reset all operations that the user made as well as the user's balance. 
