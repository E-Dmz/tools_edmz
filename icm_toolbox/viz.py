import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FormatStrFormatter


def format_log_y(c_max=1_000):
    """
    formats ax as a log-scaled histogram with number of counts on top of each bar
    ax: Axes object
    c_max: maximum value on the y (count) axis.
    Because of log scale, should be at least 10 x the actual count max in the data
    """
    ax = plt.gca()
    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_ylim([0.4, c_max])
    for p in ax.patches:
        label = f'{p.get_height()}'
        width, height = p.get_width(), p.get_height()
        x_ = p.get_x() + 0.5 * width
        y_ = p.get_height() + 0.5 * height
        ax.annotate(label, (x_, y_), va='center', ha='center', fontsize=12)


def format_log_x(x_max=1_000):
    """
    formats ax as a log-scaled histogram with number of counts on top of each bar
    c_max: maximum value on the x (count) axis.
    Because of log scale, should be at least 10 x the actual count max in the data
    """
    ax = plt.gca()
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.set_xlim([0.4, x_max])


def plot_histo_log_y(x, c_max=None, binnumber=15, binwidth=None, binrange=None):
    """
    Plots side by side the distribution of x as a conventional histogram and a log histogram
    x: numerics in an iterable
    c_max: int or float
        max value on the y (count) axis in the log histogram.
        Because of log scale, should be at least 10 x the actual count max in the data
        Default is 1000
    binnumber: int;
    binwidth: tuple of int; by default, set to min and max values
    binrange: float; by default, determined by binwidth and binnumber
    """
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    if not binrange:
        binrange = (x.min(), x.max())
    if not binwidth:
        binwidth = (binrange[1] - binrange[0]) / binnumber
    sns.histplot(x=x, kde=True, ax=ax, binwidth=binwidth, binrange=binrange,
                 color='palevioletred')
    sns.histplot(x=x, kde=True, ax=ax2, binwidth=binwidth, binrange=binrange,
                 color='powderblue')
    format_log_y(c_max)


def plot_histo_log_xy(x, x_max=None, c_max=None, binnumber=15, binwidth=None, binrange=None):
    """
    Plots side by side the distribution of x as a conventional histogram and a log histogram
    x: numerics in an iterable
    c_max: int or float
        max value on the y (count) axis in the log histogram.
        Because of log scale, should be at least 10 x the actual count max in the data
        Default is 1000
    binnumber: int;
    binwidth: tuple of int; by default, set to min and max values
    binrange: float; by default, determined by binwidth and binnumber
    """
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    if not binrange:
        binrange = (x.min(), x.max())
    if not binwidth:
        binwidth = (binrange[1] - binrange[0]) / binnumber
    sns.histplot(x=x, kde=True, ax=ax, binwidth=binwidth, binrange=binrange,
                 color='palevioletred')
    sns.histplot(x=x, kde=True, ax=ax2, binwidth=binwidth, binrange=binrange,
                 color='powderblue')
    format_log_y(c_max)
    format_log_x(x_max)

def save_fig():
    pass