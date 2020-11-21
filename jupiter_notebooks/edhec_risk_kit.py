import pandas as pd
import scipy.stats

def drawdown(return_series: pd.Series):
    """Takes a time series of asset return.
    Returns a DataFrame with columns for the wealth index,
    the previous peaks, and the percentage drawdown
    """
    wealth_index = 1000*(1+return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdown = (wealth_index - previous_peaks)/previous_peaks
    return pd.DataFrame({
        "Wealth": wealth_index,
        "Peaks": previous_peaks,
        "Drawdown": drawdown
    })

def get_ffme_returns():
    """
    Load the Fama French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """
    me_m = pd.read_csv(
        "data/Portfolios_Formed_on_ME_monthly_EW.csv",
        header=0, index_col=0, na_values=-99.99
    )
    rets = me_m[["Lo 10", "Hi 10"]]
    rets.columns = ["SmallCap", "LargeCap"]
    rets = rets/100
    rets.index = pd.to_datetime(rets.index, format="%Y%m").to_period("M")
    return rets

def get_hfi_returns():
    """
    Load and format the EDHEC Hedge Fund Index Returns
    """
    rets = pd.read_csv(
        "data/edhec-hedgefundindices.csv",
        header=0, index_col=0, parse_dates=True
    )
    rets = rets/100
    rets.index = rets.index.to_period("M")
    return rets

def skewness(r):
    """
    Alternative to scipy.stats.skew()
    """
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp/sigma_r**3

def kurtosis(r):
    """
    Alternative to scipy.stats.kurtosis()
    """
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp/sigma_r**4

def is_normal(r, level=0.01):
    """
    Applies the Jarque-Bera test to determine if a Series is normal or not
    Test is applied at the 1% level by default
    Returns True if the hypthesis of normality is accepted, False otherwise
    """
    statistic, p_value = scipy.stats.jarque_bera(r)
    return p_value > level