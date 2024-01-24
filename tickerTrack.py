import yfinance as yf


class Tracker:
    """
    This class is created to be able to provide to the program
    DataFrame for the specified stock ticker over the specified
    time period. It is used in order to provide data to display or to
    run simulations on.
    """

    def __init__(self, ticker: str, time: str):
        """
        Initializes the Tracker object
        :param ticker: the name of the stock
        :param time: the time period over which the data will be collected
        """
        self.time = time
        self.ticker = ticker
        self.data = yf.Ticker(self.ticker).history(period = self.time)

    def getData(self):
        """
        :return: returns the data property, which actually contains the DataFrame
        """
        return self.data

    def getName(self):
        return self.ticker

    def getTime(self):
        return self.time