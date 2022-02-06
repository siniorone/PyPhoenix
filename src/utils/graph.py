import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger
from time import time


def graph_indicator(data, save=False):
    logger.info(f"Plotting indicator {data.ticker}")
    fig, axes = plt.subplots(nrows=2,
                             ncols=1,
                             figsize=(20, 16),
                             gridspec_kw={'height_ratios': [5, 2]})
    axes[0].set_facecolor("white")
    axes[1].set_facecolor("white")
    axes[0].grid(alpha=0.2)
    axes[1].grid(alpha=0.2)
    graph_bb_bands(data, axes[0])
    candlestick(data.close.index, data.open, data.high, data.low, data.close, axes[0])
    graph_Phoenix(data, axes[1])
    
    if save is True:
        path = f'src/data/{data.ticker}_{int(time())}.png'
        logger.info(f"Graph is Saving to the {path}...")
        plt.savefig(path, facecolor='w', dpi=300)
    plt.show()


def hline(y, color, linewidth, linestyle, axes, alpha=0.35):
    axes.axhline(y, color=color, linewidth=linewidth, ls=linestyle, alpha=alpha)


def candlestick(t, o, h, l, c, ax):
    # plt.figure(figsize=(12,4))
    color = ["green" if close_price > open_price else "red" for close_price, open_price in zip(c, o)]
    ax.bar(x=t, height=np.abs(o-c), bottom=np.min((o, c), axis=0), width=0.6, color=color)
    ax.bar(x=t, height=h-l, bottom=l, width=0.1, color=color)


def graph_bb_bands(data, ax):
    logger.info(f"Plotting Bad Ass BB bands for {data.ticker} using matplotlib...")
    sns.scatterplot(x=data.basis.index,
                    y=data.basis,
                    ax=ax,
                    color='#ffff00',
                    marker='o',
                    s=10,
                    alpha=0.5).set_title(f"{data.ticker} from {data.start_date} to {data.end_date}")

    D01U = sns.lineplot(x=data.upper01.index,
                        y=data.upper01,
                        color="gray",
                        linestyle="--",
                        linewidth=1,
                        ax=ax)
    D01L = sns.lineplot(x=data.lower01.index,
                        y=data.lower01,
                        color="gray",
                        linestyle="--",
                        linewidth=1,
                        ax=ax)

    D02U = sns.lineplot(x=data.upper02.index,
                        y=data.upper02,
                        color="#00ffff",
                        linewidth=1,
                        ax=ax)

    D02L = sns.lineplot(x=data.lower02.index,
                        y=data.lower02,
                        color="#00ffff",
                        linewidth=1,
                        ax=ax)

    D03U = sns.lineplot(x=data.upper03.index,
                        y=data.upper03,
                        color="#ff9800",
                        linewidth=1,
                        ax=ax)

    D03L = sns.lineplot(x=data.lower03.index,
                        y=data.lower03,
                        color="#ff9800",
                        linewidth=1,
                        ax=ax)

    D04U = sns.lineplot(x=data.upper04.index,
                        y=data.upper04,
                        color="#f44336",
                        linewidth=1,
                        ax=ax)

    D04L = sns.lineplot(x=data.lower04.index,
                        y=data.lower04,
                        color="#f44336",
                        linewidth=1,
                        ax=ax)

    D05U = sns.lineplot(x=data.upper05.index,
                        y=data.upper05,
                        color="#9815d4",
                        linewidth=1,
                        ax=ax)

    D05L = sns.lineplot(x=data.lower05.index,
                        y=data.lower05,
                        color="#9815d4",
                        linewidth=1,
                        ax=ax)
    for line in ax.lines:
        y = line.get_ydata()
        if len(y) > 0:
            ax.annotate(f'{y[-1]:.2f}', xy=(1, y[-1]), xycoords=('axes fraction', 'data'),
                        ha='left', va='center', color=line.get_color())


def graph_Phoenix(data, ax):
    logger.info(f"Plotting Phoenix for {data.ticker} using matplotlib...")
    sns.lineplot(x=data.wt1.index,
                 y=data.wt1,
                 ax=ax,
                 linewidth=2,
                 color='green')

    sns.lineplot(x=data.wt2.index,
                 y=data.wt2,
                 ax=ax,
                 linewidth=3,
                 color='red')

    sns.lineplot(x=data.wt3.index,
                 y=data.wt3,
                 ax=ax,
                 linewidth=3,
                 color='blue')

    ax.fill_between(data.wt4.index, data.wt4, 50,
                    where=((data.wt4 > 50) | (data.wt4 < 50)),
                    color='gray', alpha=0.40)

    sns.scatterplot(x=data.ext2.index,
                    y=data.ext2,
                    ax=ax,
                    color='gold',
                    marker='o',
                    s=35)
    for line in ax.lines:
        y = line.get_ydata()
        if len(y) > 0:
            ax.annotate(f'{y[-1]:.2f}', xy=(1, y[-1]), xycoords=('axes fraction', 'data'),
                        ha='left', va='center', color=line.get_color())

    hline(120, color="purple", linewidth=1, linestyle="-", axes=ax)
    hline(110, color="red", linewidth=1, linestyle="-", axes=ax)
    hline(100, color="orange", linewidth=2, linestyle="-", axes=ax)
    hline(100, color="blue", linewidth=2, linestyle="--", axes=ax)
    hline(90, color="blue", linewidth=1, linestyle="-", axes=ax)
    hline(80, color="white", linewidth=2, linestyle="-", axes=ax)
    hline(80, color="blue", linewidth=2, linestyle="--", axes=ax)
    hline(70, color="white", linewidth=1, linestyle="-", axes=ax)
    hline(60, color="gray", linewidth=2, linestyle="-", axes=ax)
    hline(60, color="yellow", linewidth=2, linestyle="--", axes=ax)
    hline(50, color="yellow", linewidth=2, linestyle="-", axes=ax)
    hline(40, color="gray", linewidth=2, linestyle="-", axes=ax)
    hline(40, color="yellow", linewidth=2, linestyle="--", axes=ax)
    hline(30, color="white", linewidth=1, linestyle="-", axes=ax)
    hline(20, color="white", linewidth=2, linestyle="-", axes=ax)
    hline(20, color="blue", linewidth=2, linestyle="--", axes=ax)
    hline(10, color="blue", linewidth=1, linestyle="-", axes=ax)
    hline(00, color="orange", linewidth=2, linestyle="-", axes=ax)
    hline(00, color="blue", linewidth=2, linestyle="--", axes=ax)
    hline(-10, color="red", linewidth=1, linestyle="-", axes=ax)
    hline(-20, color="purple", linewidth=1, linestyle="-", axes=ax)
