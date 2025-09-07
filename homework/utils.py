from fredapi import Fred
import matplotlib as mpl
import matplotlib.pyplot as plt
from config import FRED_API_KEY
import pandas as pd
# Read data

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
    ax.plot(data['pct_change_label'])
    ax.set_title(title, fontname = font)
    ax.set_xlabel(xlabel, fontname = font)
    ax.set_ylabel(ylabel, fontname = font)
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

def get_fred_series(series_id, api_key, start=None, end=None):
    return
def transform_series(series, *, op=None, periods=None, annualize=None, resample_to=None):
    return
def make_axes(figsize=(6.5, 2.5), dpi=300, font="Georgia", grid=True):
    return

def plot_lines(ax, df, *, styles=None, linewidth=2):
    return 
def add_legend(ax, loc="best", ncol=1):
    return
def fred_single(series_id, *, title="", ylabel="", start=None, end=None, transform=None, periods=None, annualize=None, resample_to=None, yformatter=None):
    return
def fred_multi(series_specs, *, title="", ylabel="", start=None, end=None, yformatter=None, legend_loc="best", styles=None, recessions=False):
    return

def fred_reg_graph(
        data_series,
        title,
        xlabel,
        ylabel,
        data_start = '1960-01-01',
        data_end = None,
        api_key = FRED_API_KEY,
        dpi = 300,
        font = 'Georgia',
        fig_width = 6.5,
        fig_height = 2.5,
        has_grid = True,):
    
    fred = Fred(api_key=api_key)
    data = fred.get_series(data_series).to_frame(name=data_series)
    if data_end is not None:
        data = data.loc[data_start:data_end]
    else:
        data = data.loc[data_start:]
    
    # Setting up graph: 
    fig, ax = plt.subplots(figsize=(fig_width,fig_height), dpi=dpi)
    ax.plot(data[data_series])

    ax.set_title(title, fontname = font)
    ax.set_xlabel(xlabel, fontname = font)
    ax.set_ylabel(ylabel, fontname = font)
    ax.yaxis.set_major_formatter('{x:,.0f}%')
    if has_grid:
        ax.grid()
    return data, ax
