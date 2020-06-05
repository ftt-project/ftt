#from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.techindicators import TechIndicators

from spectator.strategy import StrategyAdviser

adviser = StrategyAdviser(symbol='GOOGL', enter_price='1390', sell_price='1400')
print(adviser.advised_to_sell())

#ts = TimeSeries(key='KHRYFWCSGMXTXR9U')
#data, meta_data = ts.get_intraday('GOOGL')
#data, meta_data = ts.get_quote_endpoint('GOOGL')
#print(meta_data)
#print(data)

#ti = TechIndicators(key='KHRYFWCSGMXTXR9U')
#data, meta_data = ti.get_sma('GOOGL', interval='5min', time_period='200', series_type='high')
#print(meta_data)
#print(data)
