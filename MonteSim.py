"""
    MONTE CARLO METHOD:
    Uses repeated random sampling from data pools to be able to
    solve deterministic problems that might not have
    another(deterministic) approach

    Used in optimization, numerical integration, and draws from
    probability distributions*. We generate
    repeated random solutions from a Markov chains, where each
    state/value is from the target distribution

    *IN FINANCE:
    The Monte Carlo Method is used to simulate the uncertainty
    when obtaining values in finance, and utilizes them to generate
    a likely outcome, shown in the form of a normal distribution.

    More specifically, the Method is used to generate likely price
    paths for a ticker or an equity, where the most probable price
    point within the given time period is provided.
"""
import mplcursors
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pandas import DataFrame
from scipy.stats import norm

from Tracker.tickerTrack import Tracker


def runSim(ticker: str, simCount: int, dayCount: int):
    """
        Brownian Method: Provides a possible path for the stock return.
            Involves drift, the direction that rates of
            returns have had in the past.
            Additionally, there is Volatility, which
            is the historical standard deviation multiplied by a random,
            Z-distribution(standard normal) variable.

        The calculations above are conducted above several
        times(often thousands of time) in order to find a likely outcome

        P(t) = P(t-1)(e^r)
        Drift Equation: μ - 0.5(𝜎^2)
        Volatility: 𝜎Z[Rand(0;1)]
        Thus, r ends up equalling drift + volatility
        r: (μ - 0.5(𝜎^2)) + (𝜎Z[Rand(0;1)])
        P(t) = P(t-1)(e^((μ - 0.5(𝜎^2)) + (𝜎Z[Rand(0;1)])))

        Possible Future updates to the file>>>
        Furthermore, we will automate and compartmentalize the process using various
        helper methods.
        After obtaining the daily return and price trajectory arrays, we can compute the
        Sharpe ratio for the stock to show additional metrics given the CAPM formula
    """
    # Pulling data from yfinance using the imported Tracker class
    data: DataFrame = Tracker(ticker, 'max').getData()['Close']
    # Obtaining log returns
    logRet = getLogReturn(data)
    # Obtaining daily return arrays
    dailyRet = getDailyReturn(logRet, dayCount, simCount)
    # PricePath stores an array of arrays containing possible stock values
    simPriceArr = getPrices(dailyRet, data, dayCount)
    simPriceData: DataFrame = pd.DataFrame(simPriceArr)
    # Plot Option
    x = simPriceData.iloc[dayCount - 1]
    fig, ax = plt.subplots(1, 2, figsize = (10, 4))
    sns.histplot(x, kde = True, ax = ax[0])
    sns.histplot(x, kde = True, cumulative = True, ax = ax[1])
    # sns.histplot(x, hist_kws = {'cumulative': True}, kde_kws = {'cumulative': True}, ax = ax[1])
    mplcursors.cursor(hover = True)
    plt.xlabel("Stock Price")
    plt.tight_layout()
    plt.show()

    # Printing information about stock
    print(ticker)
    print(f"Days: {dayCount - 1}")
    mean: int = simPriceData.iloc[dayCount - 1].mean()
    print(f"Expected Value on last: ${round(mean, 2)}")
    print(f"Return: {round(100 * (mean - simPriceArr[0, 1]) / mean, 2)}%")


def getLogReturn(tickerData: DataFrame):
    """
        :param tickerData: A DataFrame from yfinance providing stock data
        :return: provides logarithmic returns for the given dataframe
    """
    return np.log(1 + tickerData.pct_change())


def getDailyReturn(log_return, daysCount: int, simCount: int):
    """
        :param log_return: logarithmic returns for the stock
        :param daysCount: amount of days for which the simulation will predict
        :param simCount: amount of trials to run
        :return: provides an array of percentages by which the price will change each day

        This is the method that actually runs the simulations. Using the np.random.rand
        method, we can provide an array of size "dayCount", each containing
        "simCount" random numbers. This array is used as input into the ppf function,
        providing values for which the random variables are probabilities.

        According to The Law of Large Numbers, when the "simCount" is large enough,
        the distribution for these values begins to resemble normal distribution,
        as visible in the plot.

        Finally, we use the Brownian motion equation to return an array of possible daily
        return increases for our prices
    """
    u = log_return.mean()
    var = log_return.var()
    std = log_return.std()
    drift = u - (0.5 * var)
    # Finding percentiles for each random values in a 'daysCount' x 'simCount' array
    Z = norm.ppf(np.random.rand(daysCount, simCount))
    return np.exp(drift + (std * Z))


def getPrices(dailyRet, data, dayCount):
    """
        :param dailyRet: array storing the possible change factors for the price
        :param data: DataFrame containing all stock data for our ticker
        :param dayCount: Amount of days for which the sim will predict price
        :return: returns an array containing arrays of possible prices
    """
    pricePath = np.zeros_like(dailyRet)
    pricePath[0] = data.iloc[-1]
    for t in range(1, dayCount):
        pricePath[t] = pricePath[t - 1] * dailyRet[t]
    return pricePath