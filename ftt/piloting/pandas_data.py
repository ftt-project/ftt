import backtrader as bt


class PandasData(bt.feeds.PandasData):
    linesoverride = True  # discard usual OHLC structure
    # datetime must be present and last
    lines = ("datetime", "open", "high", "low", "close", "adj_close", "volume")
    datafields = [
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]
    params = (
        ("datetime", "datetime"),
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("adj_close", "close"),
        ("pct", "pct"),
        ("pct2", "pct2"),
        ("pct3", "pct3"),
    )
