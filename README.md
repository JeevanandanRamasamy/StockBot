# StockBot

**StockBot** is a Discord bot that allows users to simulate real-time investing in stocks. With a starting balance, users can buy stocks from a list of possible companies fetched from an API. The goal is to make profitable investments to grow their balance. If a company's stock fails, users will lose money. StockBot manages user portfolios, balances, and stock transactions, offering an engaging and educational stock market simulation experience.

---

## Features

### **Portfolio Management**
- **User Portfolios:**  
  Each user has a unique portfolio stored in the database.  
  - Check whether a user owns specific stocks based on symbols.
  - View a complete list of stocks the user owns.

### **Balance Management**
- **Set Balance:**  
  - If a user exists in the database, their balance is initialized to a fixed amount.  
  - If the user is new, they are added to the database with the starting balance.  
- **Get Balance:**  
  - Retrieve the user's current balance.  
- **Deposit Money:**  
  - Add funds to the user's balance.  

### **Stock Transactions**
- **Buy Stocks:**  
  - Purchase stocks from a list of available companies.  
  - Update the user's portfolio by adding the purchased stock(s).  
  - Deduct the purchase cost from the user's balance.  
  - Ensure sufficient funds before allowing the transaction.  

- **Sell Stocks:**  
  - Remove stocks from the user's portfolio and refund the sale price to their balance.  
  - Prevent selling more shares than owned or selling stocks that the user does not possess.  
  - If all shares of a stock are sold, remove the stock entry from the user's portfolio.  

### **Stock Information**
- **Available Stocks:**  
  - Fetch and display a list of possible stocks from the API.  

- **Show Portfolio:**  
  - Display all the stocks the user owns, including updated balances after transactions.

### **Reset Functionality**
- Reset all user operations and balance to the initial state, providing a clean slate for the user.

---

## How to Run StockBot

1. **Clone or Download the Repository:**  
   Fork this repository or download the code directly from GitHub.  

2. **Navigate to the Project Directory:**  
   Open the folder containing the downloaded code.  

3. **Install Required Dependencies:**  
   Use `pip` to install the following Python packages:  
   - `discord`  
   - `pymongo`  
   - `python-dotenv`  
   - `requests`  
   - `os`  
   - `json`  
   - `discord.commands`  

   Run:  
   ```bash
   pip install discord pymongo python-dotenv requests os json
   ```
4. **Set Up Environment Variables:**  
   Create a `.env` file in the project directory to securely store your bot token and stock API key.  
   Add the following lines to the file:  
   ```plaintext
   DISCORD_TOKEN=your_discord_bot_token
   API_KEY=your_stock_api_key
   ```
5. **Run the Bot:**
   Execute the bot script using Python:
   ```python
   python bot.py
   ```

---

## Example Commands

Below are some key commands to interact with StockBot:

- **View Portfolio:**  
  `!portfolio`  
  Displays a list of all stocks you own, including quantities and your updated balance.  

- **Buy Stocks:**  
  `!buy <symbol> <quantity>`  
  Purchases the specified number of shares for the given stock symbol.  
  - Example: `!buy AAPL 10` buys 10 shares of Apple.  

- **Sell Stocks:**  
  `!sell <symbol> <quantity>`  
  Sells the specified number of shares you own for a given stock symbol.  
  - Example: `!sell TSLA 5` sells 5 shares of Tesla.  
  - If you attempt to sell more shares than you own, the command will fail.  

- **Check Balance:**  
  `!balance`  
  Displays your current balance.  

- **Deposit Funds:**  
  `!deposit <amount>`  
  Adds the specified amount of money to your account balance.  
  - Example: `!deposit 500` adds $500 to your balance.  

- **Reset Account:**  
  `!reset`  
  Clears all your stock transactions and resets your balance to the starting amount.  

---

## Start Trading Today!

Test your investment strategies and see how well you can grow your virtual portfolio with **StockBot**. Happy trading!
