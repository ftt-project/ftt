import yaml, time

from src.trade.adviser.adviser import Adviser
from src.trade.market.quote_portfolio import QuotePortfolio
from src.trade.market.market import Market

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
        for quote in quote_portfolios:
            result = Market().get_quote(quote)
            print(result)
        time.sleep(11)
