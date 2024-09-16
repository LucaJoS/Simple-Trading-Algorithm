
import pandas as pd
import numpy as np

def trading_algorithm(spx_order_book: pd.DataFrame, iei_order_book: pd.DataFrame, current_position: pd.DataFrame, transactions: pd.DataFrame) -> tuple:
    spx_order_book = spx_order_book.copy()
    iei_order_book = iei_order_book.copy()

    # Calculate 20-day moving average and standard deviation for SPX for Mean Reversion Strategy
    spx_order_book['20D_MA'] = spx_order_book['Close_Price'].rolling(window=20).mean()
    spx_order_book['20D_STD'] = spx_order_book['Close_Price'].rolling(window=20).std()
    spx_latest_close = spx_order_book['Close_Price'].iloc[-1]
    spx_latest_ma20 = spx_order_book['20D_MA'].iloc[-1]
    spx_latest_std20 = spx_order_book['20D_STD'].iloc[-1]

    # Mean Reversion Signal for SPX
    spx_signal = 0  # Hold
    spx_qty = 10
    if spx_latest_close > spx_latest_ma20 + 2 * spx_latest_std20:  # Sell if price is 2 standard deviations above the MA
        spx_signal = -1
    elif spx_latest_close < spx_latest_ma20 - 2 * spx_latest_std20:  # Buy if price is 2 standard deviations below the MA
        spx_signal = 1

    # Calculate 5-day moving average for IEI for Momentum Strategy
    iei_order_book['5D_MA'] = iei_order_book['Close_Price'].rolling(window=5).mean()
    iei_latest_close = iei_order_book['Close_Price'].iloc[-1]
    iei_latest_ma5 = iei_order_book['5D_MA'].iloc[-1]

    # Momentum Signal for IEI
    iei_signal = 0  # Hold
    iei_qty = 20
    if iei_latest_close > iei_latest_ma5:  # Buy if the price is above the 5-day MA
        iei_signal = 1
    elif iei_latest_close < iei_latest_ma5:  # Sell if the price is below the 5-day MA
        iei_signal = -1

    return (spx_signal, spx_latest_close, spx_qty, iei_signal, iei_latest_close, iei_qty)