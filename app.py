#from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.techindicators import TechIndicators

import yaml, time

from spectator.strategy import StrategyAdviser

#print(adviser.advised_to_sell())
#print(adviser.advised_to_exit())

#ts = TimeSeries(key='KHRYFWCSGMXTXR9U')
#data, meta_data = ts.get_intraday('GOOGL')
#data, meta_data = ts.get_quote_endpoint('GOOGL')
#print(meta_data)
#print(data)

#ti = TechIndicators(key='KHRYFWCSGMXTXR9U')
#data, meta_data = ti.get_sma('GOOGL', interval='5min', time_period='200', series_type='high')
#print(meta_data)
#print(data)

with open('config/symbols.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    while(True):
        for symbol in data['track']:
            adviser = StrategyAdviser(
                symbol=symbol,
                enter_price=1390,
                sell_price=1400,
                loss_threshold_percent=5
            )
            print(adviser.qoute)
        time.sleep(11)
