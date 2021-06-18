class ExchangeNameNormalizer:
    def __init__(self, exchange_name):
        self.exchange_name = exchange_name

    def perform(self):
        switcher = {
            "TOR": "Toronto",
            "NCM": "NASDAQ",
            "NYQ": "NYSE",
        }
        return switcher.get(self.exchange_name, self.exchange_name)
