import yaml, time

from src.trade.adviser.adviser import Adviser
from src.trade.market.qoute_portfolio import QoutePortfolio

with open('config/symbols.yml') as f:
    configuration = yaml.load(f, Loader=yaml.FullLoader)
    quote_portfolios = []
    for symbol, data in configuration['portfolio'].items():
        quote_portfolios.append(QoutePortfolio(
            symbol=symbol,
            enter_price=data['enter_price'],
            quit_price=data['quit_price'],
            sell_price=data['sell_price']
        ))
    for symbol in configuration['track']:
        quote_portfolios.append(QoutePortfolio(
            symbol=symbol
        ))

    while True:
        for symbol in quote_portfolios:
            adviser = Adviser(
                symbol=symbol,
                enter_price=1390,
                sell_price=1400,
                loss_threshold_percent=5
            )
            print(adviser.qoute)
        time.sleep(11)
