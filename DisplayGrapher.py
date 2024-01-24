import random

import matplotlib.pyplot as plt
import mplcursors

from Tracker.tickerTrack import Tracker


def showGraphSing(tickerNames: list[str], timeTrack: str):
    """
    Shows all ticker data on one plot
    :param tickerNames: The list of tickers that will be graphed
    :param timeTrack: The time frame over which the data will be provided
    :return: Does not return anything
    """
    for i in range(0, len(tickerNames)):
        tempData = Tracker(tickerNames[i], timeTrack).getData()
        plt.plot(tempData['Low'], label = tickerNames[i] + ' LOW', color = _getRanColor())
        plt.plot(tempData['High'], label = tickerNames[i] + ' HIGH', color = _getRanColor())
        plt.plot(tempData['Open'], label = tickerNames[i] + ' OPEN', color = _getRanColor())
        plt.plot(tempData['Close'], label = tickerNames[i] + ' CLOSE', color = _getRanColor())
    setUpAndShow()


def showGraphMulti(tickerNames: list[str], timeTrack: str):
    """
    Shows several different plots in order to show different ticker data separately
    :param tickerNames: The list of tickers that will be graphed
    :param timeTrack: The time frame over which the data will be provided
    :return: Does not return anything
    """
    fig, axes = plt.subplots(nrows = 2, ncols = 2)
    count: int = 0
    for r in range(0, 2):
        for c in range(0, 2):
            if count < len(tickerNames):
                temp = (Tracker(tickerNames[count], timeTrack)
                        .getData()
                        .loc[:, ['Low', 'Open', 'High', 'Close']]
                        .plot(ax = axes[r, c]))
                count += 1
    setUpAndShow()


def setUpAndShow():
    mplcursors.cursor(hover = 1)
    plt.xlabel("Dates(MM-DD-YYYY HH:MM)")
    plt.xticks(rotation = 45)
    plt.ylabel("Prices($)")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()


def _getRanColor():
    return [random.random(), random.random(), random.random()]