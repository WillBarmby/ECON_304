from fredapi import Fred
import matplotlib as mpl
import matplotlib.pyplot as plt
from config import FRED_API_KEY
import pandas as pd


def unemp_graphs(
        title="Unemployment Rates",
        font="Georgia",
        xlabel="",
        ylabel="Percent",
        dpi=300,
):
    fred = Fred(api_key=FRED_API_KEY)
    # dictionary: {FRED_code: legend_label}
    series_dict = {
        "UNRATE": "U3",
        "U6RATE": "U6",
    }

    # fetch each series into a dictionary of DataFrames
    data_frames = {}
    for code, label in series_dict.items():
        s = fred.get_series(code).to_frame(name=label)
        s = s.loc["1994-01-01":"2025-07-31"]
        data_frames[label] = s

    # align into a single DataFrame
    data = pd.concat(data_frames.values(), axis=1)

    # plot
    fig, ax = plt.subplots(figsize=(6.5, 2.5), dpi=dpi)
    plt.rcParams["font.family"] = font
    for label in data.columns:
        ax.plot(data.index, data[label], label=label)

    ax.set_title(title, fontname=font)
    ax.set_xlabel(xlabel, fontname=font, fontsize = 12)
    ax.set_ylabel(ylabel, fontname=font, fontsize = 12)
    ax.yaxis.set_major_formatter("{x:,.0f}%")
    ax.grid()
    ax.legend(loc="best", frameon=True)

    return data, ax
def fred_pct_change_graph(
        data_series,
        data_start,
        data_end,
        title,
        xlabel,
        ylabel,
        api_key = FRED_API_KEY,
        pct_change_periods = 4,
        dpi = 300,
        font = 'Georgia'):
    
    fred = Fred(api_key=api_key)
    data = fred.get_series(data_series).to_frame(name=data_series)
    data = data.loc[data_start:data_end]
    data['pct_change_label'] = data[data_series].pct_change(periods=pct_change_periods) * 100
    # Setting up graph: 
    fig, ax = plt.subplots(figsize=(6.5,2.5), dpi=dpi)
    plt.rcParams["font.family"] = font
    ax.plot(data['pct_change_label'])
    ax.set_title(title, fontname = font)
    ax.set_xlabel(xlabel, fontname = font, fontsize = 12)
    ax.set_ylabel(ylabel, fontname = font, fontsize = 12)
    ax.yaxis.set_major_formatter('{x:,.0f}%')
    ax.grid()
    return data, ax
def LFPR_graph(
        title="Labor Force Participation Rate",
        font="Georgia",
        xlabel="",
        ylabel="Percent",
        dpi=300,
):
    fred = Fred(api_key=FRED_API_KEY)
    # dictionary: {FRED_code: legend_label}
    series_dict = {
        "CIVPART": "Civilian LFPR",
        "LNS11300002": "Women's LFPR",
    }

    # fetch each series into a dictionary of DataFrames
    data_frames = {}
    for code, label in series_dict.items():
        s = fred.get_series(code).to_frame(name=label)
        s = s.loc["1960-01-01":"2025-07-31"]
        data_frames[label] = s

    # align into a single DataFrame
    data = pd.concat(data_frames.values(), axis=1)

    # plot
    fig, ax = plt.subplots(figsize=(6.5, 2.5), dpi=dpi)
    plt.rcParams["font.family"] = font
    for label in data.columns:
        ax.plot(data.index, data[label], label=label)

    ax.set_title(title, fontname=font)
    ax.set_xlabel(xlabel, fontname=font, fontsize = 12)
    ax.set_ylabel(ylabel, fontname=font, fontsize = 12)
    ax.yaxis.set_major_formatter("{x:,.0f}%")
    ax.grid()
    ax.legend(loc="best", frameon=True)

    return data, ax
def add_fred_series_to_df(
    df,
    fred_series_key,
    fred_api_key=FRED_API_KEY,
    series_name=None,
    start_date=None,
    end_date=None,
    freq=None
):
    """
    Fetches a FRED series and adds it to the provided DataFrame.

    Args:
        df (pd.DataFrame): Existing DataFrame to add the series to.
        fred_api_key (str): Your FRED API key.
        fred_series_key (str): FRED series code.
        series_name (str, optional): Name for the new column. Defaults to fred_series_key.
        start_date (str, optional): Start date for the data (YYYY-MM-DD).
        end_date (str, optional): End date for the data (YYYY-MM-DD).
        freq (str, optional): Pandas offset alias for frequency conversion (e.g., 'Q' for quarterly).

    Returns:
        pd.DataFrame: DataFrame with the new series added.
    """
    fred = Fred(api_key=fred_api_key)
    data = fred.get_series(fred_series_key)
    data = data.to_frame(name=series_name or fred_series_key)
    if start_date or end_date:
        data = data.loc[start_date:end_date]
    if freq:
        data = data.resample(freq).mean()
    # Align index and join
    df = df.join(data, how='outer')
    return df

def fetch_fred_series(
    fred_api_key,
    fred_series_key,
    start_date=None,
    end_date=None,
    freq=None,
    series_name=None
):
    """
    Fetches a FRED series as a DataFrame.

    Args:
        fred_api_key (str): Your FRED API key.
        fred_series_key (str): FRED series code.
        start_date (str, optional): Start date for the data (YYYY-MM-DD).
        end_date (str, optional): End date for the data (YYYY-MM-DD).
        freq (str, optional): Pandas offset alias for frequency conversion.
        series_name (str, optional): Name for the DataFrame column.

    Returns:
        pd.DataFrame: DataFrame with the series.
    """
    fred = Fred(api_key=fred_api_key)
    data = fred.get_series(fred_series_key)
    data = data.to_frame(name=series_name or fred_series_key)
    if start_date or end_date:
        data = data.loc[start_date:end_date]
    if freq:
        data = data.resample(freq).mean()
    return data