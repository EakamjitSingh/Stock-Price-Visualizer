# stock_toolkit.py
# A comprehensive, command-line-driven tool for stock analysis.

import argparse
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# ==============================================================================
# MODULE 1: DATA FETCHER
# Responsible for all interactions with the yfinance API.
# ==============================================================================

def fetch_stock_data(tickers, start_date, end_date):
    """
    Fetches historical stock data for given tickers from Yahoo Finance.
    
    Args:
        tickers (list): A list of stock ticker symbols.
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the OHLCV data for the tickers,
                          or an empty DataFrame if fetching fails.
    """
    print(f"\n[*] Fetching data for {', '.join(tickers)} from {start_date} to {end_date}...")
    try:
        # Download full OHLCV (Open, High, Low, Close, Volume) data
        # group_by='ticker' is essential for handling multiple tickers correctly.
        stock_data = yf.download(tickers, start=start_date, end=end_date, group_by='ticker', progress=False)
        
        if stock_data.empty:
            print("❌ Error: No data found. Please check tickers and date range.")
            return pd.DataFrame()

        # Drop tickers that have no data (all NaN columns)
        stock_data.dropna(axis=1, how='all', inplace=True)
        if stock_data.empty:
            print("❌ Error: All specified tickers were invalid or had no data for the period.")
            return pd.DataFrame()

        print("✅ Data fetched successfully.")
        return stock_data
    except Exception as e:
        print(f"❌ An unexpected error occurred during data fetching: {e}")
        return pd.DataFrame()

# ==============================================================================
# MODULE 2: ANALYSIS
# Contains all financial calculation logic.
# ==============================================================================

def calculate_moving_averages(data, ticker, windows):
    """Calculates Simple Moving Averages (SMA) for a given stock."""
    for window in windows:
        data[(ticker, f'SMA_{window}')] = data[(ticker, 'Close')].rolling(window=window).mean()
    return data

def calculate_rsi(data, ticker, window=14):
    """Calculates the Relative Strength Index (RSI)."""
    delta = data[(ticker, 'Close')].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data[(ticker, 'RSI')] = rsi
    return data

def calculate_performance(data):
    """Normalizes stock prices to 100 to compare performance."""
    # Using 'Adj Close' is better for performance comparison as it accounts for dividends/splits
    adj_close = data.xs('Adj Close', level=1, axis=1)
    return (adj_close / adj_close.iloc[0] * 100)

def calculate_correlation(data):
    """Calculates the correlation matrix for the closing prices of the stocks."""
    close_prices = data.xs('Close', level=1, axis=1)
    return close_prices.corr()

# ==============================================================================
# MODULE 3: PLOTTING
# Manages all matplotlib and seaborn visualizations.
# ==============================================================================

def plot_full_analysis(data, ticker, ma_windows):
    """
    Generates a comprehensive 3-panel plot: Price/MAs, Volume, and RSI.
    """
    print(f"[*] Generating full analysis plot for {ticker}...")
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 12), sharex=True, 
                                        gridspec_kw={'height_ratios': [3, 1, 1]})
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Panel 1: Price and Moving Averages
    ax1.plot(data.index, data[(ticker, 'Close')], label='Close Price', color='blue')
    for window in ma_windows:
        ax1.plot(data.index, data[(ticker, f'SMA_{window}')], label=f'SMA {window}', linestyle='--')
    ax1.set_title(f'Full Analysis for {ticker}', fontsize=16)
    ax1.set_ylabel('Price (USD)', fontsize=12)
    ax1.legend()
    ax1.grid(True)

    # Panel 2: Volume
    ax2.bar(data.index, data[(ticker, 'Volume')], color='gray', alpha=0.6)
    ax2.set_ylabel('Volume', fontsize=12)
    ax2.grid(True)

    # Panel 3: RSI
    ax3.plot(data.index, data[(ticker, 'RSI')], label='RSI', color='purple')
    ax3.axhline(70, color='red', linestyle='--', linewidth=1, label='Overbought (70)')
    ax3.axhline(30, color='green', linestyle='--', linewidth=1, label='Oversold (30)')
    ax3.set_ylabel('RSI', fontsize=12)
    ax3.set_xlabel('Date', fontsize=12)
    ax3.legend()
    ax3.grid(True)
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    print("✅ Plot generated.")
    plt.show()

def plot_performance_comparison(performance_data):
    """Plots the normalized performance of multiple stocks."""
    print("[*] Generating performance comparison plot...")
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(14, 7))
    
    performance_data.plot(ax=ax)
    
    ax.set_title('Stock Performance Comparison (Normalized to 100)', fontsize=16)
    ax.set_ylabel('Normalized Price', fontsize=12)
    ax.set_xlabel('Date', fontsize=12)
    ax.legend(title='Tickers')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    plt.tight_layout()
    print("✅ Plot generated.")
    plt.show()

def plot_correlation_heatmap(correlation_data):
    """Plots the correlation matrix as a heatmap."""
    print("[*] Generating correlation heatmap...")
    if correlation_data.shape[0] < 2:
        print("⚠️ Warning: Correlation requires at least 2 tickers. Skipping heatmap.")
        return
        
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(correlation_data, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5, ax=ax)
    
    ax.set_title('Stock Correlation Matrix', fontsize=16)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    print("✅ Plot generated.")
    plt.show()

# ==============================================================================
# MODULE 4: MAIN
# The main entry point, handling argument parsing and orchestrating calls.
# ==============================================================================

def main():
    """
    Main function to run the stock analysis toolkit.
    """
    parser = argparse.ArgumentParser(
        description="Advanced Stock Analysis Toolkit",
        formatter_class=argparse.RawTextHelpFormatter # For better help text formatting
    )
    
    # --- Define Command-Line Arguments ---
    parser.add_argument(
        'tickers', 
        metavar='TICKERS', 
        type=str, 
        help="Comma-separated stock ticker symbols (e.g., 'AAPL,MSFT,GOOGL')"
    )
    parser.add_argument(
        '-s', '--start', 
        dest='start_date', 
        type=str, 
        default=(datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d'),
        help="Start date in YYYY-MM-DD format. Defaults to one year ago."
    )
    parser.add_argument(
        '-e', '--end', 
        dest='end_date', 
        type=str, 
        default=datetime.now().strftime('%Y-%m-%d'),
        help="End date in YYYY-MM-DD format. Defaults to today."
    )
    parser.add_argument(
        '--analysis', 
        type=str, 
        choices=['full', 'compare', 'corr'], 
        default='full',
        help="Type of analysis to perform:\n"
             "  'full'    - Detailed plot with Price, MAs, Volume, and RSI for each stock. (default)\n"
             "  'compare' - Compare the performance of all tickers.\n"
             "  'corr'    - Generate a correlation heatmap for all tickers."
    )
    parser.add_argument(
        '--ma',
        dest='ma_windows',
        type=str,
        default='50,200',
        help="Comma-separated list of moving average windows (e.g., '20,50'). Used with 'full' analysis."
    )

    args = parser.parse_args()
    
    # --- Process Arguments and Run Analysis ---
    tickers = [ticker.strip().upper() for ticker in args.tickers.split(',')]
    ma_windows = [int(w.strip()) for w in args.ma_windows.split(',')]
    
    # Fetch data once
    stock_data = fetch_stock_data(tickers, args.start_date, args.end_date)
    
    if stock_data.empty:
        print("\n--- Analysis Aborted ---")
        return

    # Execute the chosen analysis
    if args.analysis == 'full':
        if len(tickers) > 1:
             # For multiple tickers, data is multi-indexed. We need to process each one.
            for ticker in tickers:
                # Create a temporary DataFrame for a single ticker's data
                single_ticker_data = stock_data[ticker].to_frame().unstack(level=0)
                single_ticker_data.columns = single_ticker_data.columns.droplevel(0)
                
                # Perform analysis
                data_with_ma = calculate_moving_averages(single_ticker_data.copy(), '', ma_windows)
                data_with_rsi = calculate_rsi(data_with_ma, '')
                
                # Reconstruct column names for plotting
                data_with_rsi.columns = pd.MultiIndex.from_product([[ticker], data_with_rsi.columns])
                
                plot_full_analysis(data_with_rsi, ticker, ma_windows)
        else:
            # Single ticker case is simpler
            ticker = tickers[0]
            data_with_ma = calculate_moving_averages(stock_data.copy(), ticker, ma_windows)
            data_with_rsi = calculate_rsi(data_with_ma, ticker)
            plot_full_analysis(data_with_rsi, ticker, ma_windows)

    elif args.analysis == 'compare':
        performance_data = calculate_performance(stock_data)
        plot_performance_comparison(performance_data)
        
    elif args.analysis == 'corr':
        correlation_data = calculate_correlation(stock_data)
        plot_correlation_heatmap(correlation_data)

    print("\n--- Analysis Complete ---")

if __name__ == "__main__":
    main()
