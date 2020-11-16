import time
import yaml

from src.trade.market.adapters import yfinance
from src.trade.market.adapters import alpha_vantage
from src.trade.market.market import Market
from src.trade.market.quote_portfolio import QuotePortfolio

with open('config/symbols.yml') as f:
    configuration = yaml.load(f, Loader=yaml.FullLoader)
    quote_portfolios = []
    for symbol, data in configuration['portfolio'].items():
        quote_portfolios.append(QuotePortfolio(
            symbol=symbol,
            enter_price=data['enter_price'],
            quit_price=data['quit_price'],
            sell_price=data['sell_price']
        ))
    for symbol in configuration['track']:
        quote_portfolios.append(QuotePortfolio(
            symbol=symbol
        ))

    quote_portfolios = set(quote_portfolios)
    quote_portfolios = sorted(quote_portfolios)

    while True:
        quotes = Market(adapter=yfinance.Adapter).get_quotes(quote_portfolios)
        for quote in quotes:
            print(quote)
        print('')
        time.sleep(11)
