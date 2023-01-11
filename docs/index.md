Welcome to Financial Trading Tools Project home page.

## What is FTT?

FTT is a set of tools for portfolio management.
FTT is a collection of tools that analyzes historical financial data, utilizes open-source algorithms, 
optimizes portfolio based on user input, and stores portfolio composition, and tracks changes in its performance.

### What does it do?

- organizes securities into portfolios.
- optimizes portfolio using historical financial data and known algorithms.
- provides a user-friendly interface for portfolio management.

### What is planned and on the roadmap?

- integration with Interactive Brokers API for operations performing.
- adding more portfolio optimization algorithms.
- power tools for portfolio comparing and analyzing.
- portfolio performance tracking.

### What does FTT not do?

- it does not perform day trading operations.
- it does not stocks contain research tools.
- it does not provide any financial advice use it on your own discretion.

## Introduction and history of the project 

FTT is a project that I started as a hobby.
The project at the beginning had different name and was a collection of simple python scripts. It was a playground for me to learning python,
trading algorithms and strategies.
Over time the application grew into a CLI application. I found a CLI not so user-friendly, oriented only for an advanced user, and it didn't support my vision.
At the moment FTT application is written using QT and PySide6 framework.

The main objective of FTT is to provide a set of tools to help calculate and optimize a portfolio that is easy and intuitive to use.

The future of the application is to be a tool that operates a collection of securities, and suggests financial operations such as hold, buy, sell, and optimize portfolio. Once mature, the application will autonomously perform financial operations on the live market via integration with a broker system.

# Vision

> Finance is hard. Programming is hard.

## Ideal solution
- In the perfect world, a person wants to invest a dedicated budget and receive the best possible dividends seamlessly, painlessly, and effortlessly.
- Having these expectations, an investor uses software that accepts desired securities and a budget as input. This solution creates a portfolio out of suggested securities, calculates weights using different algorithms, and provides multiple portfolio candidates. In addition, the solution improves portfolios by adding additional securities to make each portfolio candidate balanced.
- It is hard for a non-technical person to decide what portfolio will be the best and choose among multiple options because algorithms are complicated, and the logic behind them is complex to understand. The solution helps investors decide by running backtest with each generated portfolio candidate over the indicated historical period and provides results. The result is the best-performed portfolios categorized by risk, volatility, and dividends.
- The Investor chooses a portfolio out of the resulting list. The next step is to allocate calculated weights to the budget and buy securities. The solution is not a securities brokerage system but can easily communicate. The Investor initiates a securities purchase operation, and the solution communicates with a connected brokerage system and initiates securities purchase operations. The brokerage system completes operations and communicates back to the solution. The solution displays information to the Investor.
- Purchase of securities is the first step to achieving the best result. The Investor must follow market updates, set stop-loss operations on each security in the portfolio, and rebalance the portfolio occasionally. The solution monitors the latest security trends in the active portfolio and automatically prevents losses by automatically initiating selling and buying operations. The solution prompts rebalancing on time when it is reasonable. The Investor and user of the solution receive immediate notifications and observe the portfolio's performance in an easily digestible way.

## Current reality
There are a few options that a regular investor has.

### Option 1
An investor chooses a simple self-driving solution by choosing acceptable risks and scheduled or occasional financial investments. There is no control over portfolio, weights, and timing.

### Option 2
An investor chooses a more complicated system that controls securities and related operations. The investor must seek tools to build portfolios, backtest proposed portfolios, and initiate financial operations in the brokerage system.
Solutions that provide end-to-end experience are costly.

## Problems
- Calculation of portfolio using multiple algorithms.
- Backtest portfolios to choose one with given criteria.
- Complement portfolio with additional securities for better balancing.
- Initiate and control financial operations in the brokerage system.
- Monitor portfolio performance and automatically rebalance it.
- Take automated decisions on buy and sell operations to prevent losses.

## Goals
- Achieve automated trading on a provided asset.
    - Automated trading means that the system make a decisions on buy/sell/hold actions on their own.
- Automated assets management.
    - Assets management means that the system can calculate the ideal portfolio based on user input, historical data, and external events.
- Cohesive actions based on assets management and trading.
    - Actions like portfolio rebalancing, drawdown protection.

