from datetime import datetime

import pandas as pd


class SecurityPriceMapper:
    class Collection:
        def __init__(self, collection):
            self.__collection = collection

        def __iter__(self):
            for element in self.__collection:
                yield element

        def __len__(self):
            return len(self.__collection)

        def to_dicts(self):
            return [element.to_dict() for element in self]

    @classmethod
    def from_dataframe(cls, dataframe: pd.DataFrame):
        datas = []
        for index, row in dataframe.iterrows():
            data = {
                "datetime": datetime.fromtimestamp(index.timestamp()),
                "adj_close": row["Adj Close"],
                "close": row["Close"],
                "high": row["High"],
                "low": row["Low"],
                "open": row["Open"],
                "volume": row["Volume"],
            }
            datas.append(cls(data))
        return cls.Collection(datas)

    def __init__(self, data: dict):
        self.__data = data

    def to_dict(self) -> dict:
        return self.__data
