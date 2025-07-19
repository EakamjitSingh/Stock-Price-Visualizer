# Advanced Stock Analysis Toolkit

`stock_toolkit.py` is a powerful command-line tool for fetching, analyzing, and visualizing historical stock market data. It leverages the `yfinance` library to pull data from Yahoo Finance and uses `pandas` for analysis and `matplotlib`/`seaborn` for plotting.

## Features

* **Comprehensive Single-Stock Analysis**: Generate a detailed chart for a single stock, including its closing price, multiple Simple Moving Averages (SMAs), trading volume, and the Relative Strength Index (RSI).
* **Multi-Stock Performance Comparison**: Normalize the prices of multiple stocks to a starting value of 100 and plot their performance over time to easily compare them.
* **Correlation Analysis**: Calculate and visualize the correlation between the closing prices of multiple stocks in an easy-to-read heatmap.
* **Customizable Timeframes**: Specify any start and end date for your analysis.
* **Flexible Inputs**: Pass tickers, timeframes, and analysis types directly through the command line.

## Prerequisites

Before running the script, you need to have Python 3 installed. You will also need to install several Python libraries.

## Installation

You can install all the necessary libraries using pip. Open your terminal and run the following command:

```bash
pip install pandas numpy yfinance matplotlib seaborn
```

## Usage

The script is run from the terminal. The basic structure of the command is:

```bash
python stock_toolkit.py <TICKERS> --analysis <ANALYSIS_TYPE> [OPTIONS]
```

Below are detailed examples for each type of analysis.

---

### 1. Full Analysis (Default)

This is the default mode. It generates a detailed 3-panel plot for each specified ticker, showing Price/SMAs, Volume, and RSI.

**Command:**

```bash
python stock_toolkit.py <TICKERS> --analysis full
```

**Examples:**

* **Analyze a single stock (e.g., Apple Inc.) for the past year:**

    ```bash
    python stock_toolkit.py AAPL
    ```

* **Analyze multiple stocks (e.g., Tesla, NVIDIA) with custom SMAs (20-day and 50-day):**

    ```bash
    python stock_toolkit.py TSLA,NVDA --ma 20,50
    ```

* **Analyze a stock for a specific timeframe (e.g., Microsoft during 2023):**

    ```bash
    python stock_toolkit.py MSFT --start 2023-01-01 --end 2023-12-31
    ```

---

### 2. Performance Comparison

This mode is used to compare the performance of multiple stocks over the same period. It normalizes their prices to a starting value of 100.

**Command:**

```bash
python stock_toolkit.py <TICKERS> --analysis compare
```

**Example:**

* **Compare the performance of major tech stocks (Meta, Amazon, Netflix, Google) over the last two years:**

    ```bash
    python stock_toolkit.py META,AMZN,NFLX,GOOGL --start 2023-07-19 --end 2025-07-19 --analysis compare
    ```

---

### 3. Correlation Heatmap

This mode calculates the correlation between the closing prices of two or more stocks and displays it as a heatmap. A value of 1 means perfect positive correlation, while -1 means perfect negative correlation.

**Command:**

```bash
python stock_toolkit.py <TICKERS> --analysis corr
```

**Example:**

* **Analyze the correlation between a tech company (AAPL), a financial institution (JPM), and an energy company (XOM):**

    ```bash
    python stock_toolkit.py AAPL,JPM,XOM --analysis corr
    ```

## Code Structure

The script is organized into four logical modules:

1.  **Data Fetcher (`fetch_stock_data`)**: Handles all API requests to Yahoo Finance. It is responsible for downloading the raw OHLCV (Open, High, Low, Close, Volume) data.
2.  **Analysis (`calculate_*` functions)**: Contains the logic for all financial calculations, such as Simple Moving Averages, RSI, performance normalization, and correlation matrices.
3.  **Plotting (`plot_*` functions)**: Manages the creation of all visualizations using Matplotlib and Seaborn, ensuring the output is clear and informative.
4.  **Main (`main`)**: The entry point of the script. It uses `argparse` to handle command-line arguments and orchestrates the calls to the other modules based on user input.
