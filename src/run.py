from src.phoenix import Phoenix


btc = Phoenix("BTC-USD", "2021-02-06", "2022-02-06")
btc.graph(save=True)
