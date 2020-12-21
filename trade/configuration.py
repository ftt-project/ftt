import yaml

class Configuration:
    def tickers_to_track(self):
        tickers = set()
        with open('config/symbols.yml') as f:
            configuration = yaml.load(f, Loader=yaml.FullLoader)
            for symbol in configuration['track']:
                tickers.append(symbol)

        return tickers
