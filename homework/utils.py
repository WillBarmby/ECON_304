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