from time import time
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from loguru import logger


def graph_bb_bands(data, fig, row, col):
    """
    This function plots the Bad Ass bollinger bands and the price candlestick of the data
    """
    # Create the candlestick plot
    logger.info("Creating Bad ass BB and candlestick plot using Plotly...")
    price = go.Candlestick(x=data.date,
                           open=data.open,
                           high=data.high,
                           low=data.low,
                           close=data.close,
                           increasing_line_color='#26a699',
                           decreasing_line_color='#ef5350',
                           name="Candlestick")
    # Create the Bad Ass bollinger bands
    base = go.Scatter(x=data.basis.index, y=data.basis, name="BB-Basis",
                      line=dict(color='yellow', width=2, dash='dot'))
    D01U = go.Scatter(x=data.upper01.index, y=data.upper01, name="+1STD",
                      line=dict(color="white", width=1))
    D01L = go.Scatter(x=data.lower01.index, y=data.lower01, name="-1STD",
                      line=dict(color="white", width=1))
    D02U = go.Scatter(x=data.upper02.index, y=data.upper02, name="+1.618STD",
                      line=dict(color="#00ffff", width=1))
    D02L = go.Scatter(x=data.lower02.index, y=data.lower02, name="-1.618STD",
                      line=dict(color="#00ffff", width=1))
    D03U = go.Scatter(x=data.upper03.index, y=data.upper03, name="+2.618STD",
                      line=dict(color="#ff9800", width=1))
    D03L = go.Scatter(x=data.lower03.index, y=data.lower03, name="-2.618STD",
                      line=dict(color="#ff9800", width=1))
    D04U = go.Scatter(x=data.upper04.index, y=data.upper04, name="+3.618STD",
                      line=dict(color="#f44336", width=1))
    D04L = go.Scatter(x=data.lower04.index, y=data.lower04, name="-3.618STD",
                      line=dict(color="#f44336", width=1))
    # Add the candlestick plot and the bollinger bands to the figure
    fig.add_trace(price, row=row, col=col)
    fig.add_trace(base, row=row, col=col)
    fig.add_trace(D01U, row=row, col=col)
    fig.add_trace(D01L, row=row, col=col)
    fig.add_trace(D02U, row=row, col=col)
    fig.add_trace(D02L, row=row, col=col)
    fig.add_trace(D03U, row=row, col=col)
    fig.add_trace(D03L, row=row, col=col)
    fig.add_trace(D04U, row=row, col=col)
    fig.add_trace(D04L, row=row, col=col)


def graph_Phoenix(data, fig, row, col):
    logger.info("Plotting the Phoenix indicator using Plotly...")
    """
    This function plots the phoenix indicator
    """
    # Create the phoenix indicator Green/Red/Blue/Energy/base line
    green = go.Scatter(x=data.wt1.index,
                       y=data.wt1,
                       name="Green",
                       line=dict(width=2, color='#4caf4f'))
    red = go.Scatter(x=data.wt2.index,
                     y=data.wt2,
                     name="Red RSI",
                     line=dict(width=3, color='#e24b4b'))
    blue = go.Scatter(x=data.wt3.index,
                      y=data.wt3,
                      name="LSMA",
                      line=dict(width=3, color='#2194f2'))
    base = go.Scatter(x=data.wt4.dropna().index,
                      y=[50 for i in range(len(data.wt4))],
                      name="base",
                      line=dict(width=1, color='#676a71'))
    energy = go.Scatter(x=data.wt4.index,
                        y=data.wt4,
                        name="Energy",
                        fill='tonexty',
                        line=dict(width=1, color='#676a71'))

    # Set The Opacity for the horizontal lines in Phoenix indicator
    op = 0.1
    # Add the phoenix indicator Lines to the figure
    fig.add_trace(green, row=row, col=col)
    fig.add_trace(red, row=row, col=col)
    fig.add_trace(blue, row=row, col=col)
    fig.add_trace(base, row=row, col=col)
    fig.add_trace(energy, row=row, col=col)
    fig.add_hline(y=50, line_color="yellow", line_width=2, opacity=op)
    fig.add_hline(y=120, line_color="purple", line_width=1, opacity=op)
    fig.add_hline(y=110, line_color="red", line_width=1, opacity=op)
    fig.add_hline(y=100, line_color="orange", line_width=2, opacity=op)
    fig.add_hline(y=100, line_color="blue", line_width=2, line_dash='dash', opacity=op)
    fig.add_hline(y=90, line_color="blue", line_width=1, opacity=op)
    fig.add_hline(y=80, line_color="white", line_width=2, opacity=op)
    fig.add_hline(y=80, line_color="blue", line_width=2, line_dash='dash', opacity=op)
    fig.add_hline(y=70, line_color="white", line_width=1, opacity=op)
    fig.add_hline(y=60, line_color="gray", line_width=2, opacity=op)
    fig.add_hline(y=60, line_color="yellow", line_width=2, line_dash='dash', opacity=op)
    fig.add_hline(y=40, line_color="gray", line_width=2, opacity=op)
    fig.add_hline(y=40, line_color="yellow", line_width=2, line_dash='dash', opacity=op)
    fig.add_hline(y=30, line_color="white", line_width=1, opacity=op)
    fig.add_hline(y=20, line_color="white", line_width=2, opacity=op)
    fig.add_hline(y=20, line_color="blue", line_width=2, line_dash='dash', opacity=op)
    fig.add_hline(y=10, line_color="blue", line_width=1, opacity=op)
    fig.add_hline(y=00, line_color="orange", line_width=2, opacity=op)
    fig.add_hline(y=00, line_color="blue", line_width=2, line_dash='dash', opacity=op)
    fig.add_hline(y=-10, line_color="red", line_width=1, opacity=op)
    fig.add_hline(y=-20, line_color="purple", line_width=1, opacity=op)


def graphly_indicator(data, phoenix=True, chart=True, save=False):
    """
    This function is the main function to plot the data
    """
    number_of_subplot = int(phoenix) + int(chart)
    # Create the figure base on the inputs
    # Plot Both Phoenix and Chart
    if phoenix and chart:
        fig = make_subplots(rows=number_of_subplot, cols=1, shared_xaxes=True,
                            subplot_titles=(f"{data.ticker}", "Phoenix Indicator"),
                            row_heights=[0.7, 0.3], vertical_spacing=0.07)
        graph_bb_bands(data, fig, row=1, col=1)
        graph_Phoenix(data, fig, row=2, col=1)
        fig.update_layout(xaxis2_showticklabels=True)
    # Plot only Phoenix Indicator
    elif phoenix and not chart:
        fig = make_subplots(rows=number_of_subplot, cols=1)
        graph_Phoenix(data, fig, row=1, col=1)
        fig.update_layout(height=300)
    # Plot only Chart
    elif chart and not phoenix:
        fig = make_subplots(rows=number_of_subplot, cols=1)
        graph_bb_bands(data, fig, row=1, col=1)
    # If the user does not want to plot anything
    else:
        raise ValueError("No indicator to plot")

    # Add Layout to the figure
    fig.update_layout({'plot_bgcolor': "#171b26",
                       'paper_bgcolor': "#171b26",
                       'legend_orientation': "h"},
                      title=f'{data.ticker} from {data.start_date} to {data.end_date}',
                      xaxis_showticklabels=True,
                      legend=dict(y=1, x=0),
                      showlegend=False,
                      font=dict(color='#dedddc'),
                      dragmode='pan',
                      hovermode='x unified',
                      margin=dict(b=20, t=0, l=0, r=40),
                      title_y=0.98,
                      hoverlabel=dict(bgcolor='rgba(23,27,38,0.75)'))
    # Update the xaxis properties
    fig.update_xaxes(zeroline=False,
                     rangeslider_visible=False,
                     showspikes=True,
                     spikemode='across',
                     spikesnap='cursor',
                     showline=False,
                     spikedash='solid',
                     gridcolor='#232732'
                     )
    # Update the yaxis properties
    fig.update_yaxes(side="right",
                     zeroline=False,
                     spikesnap='cursor',
                     gridcolor='#232732'
                     )
    # Save the figure
    if save is True:
        path = f"src/data/{data.ticker}_{int(time())}.png"
        logger.info(f"Graph is Saving to the {path}...")
        fig.write_image(path)

    # Show the figure
    fig.show()
