Stock Analysis Toolkit - Bash Launcher
This document provides instructions for run_analysis.sh, a user-friendly Bash script designed to launch the stock_toolkit.py Python application.

🚀 What is run_analysis.sh?
The run_analysis.sh script acts as an interactive wrapper for the main Python tool. Instead of requiring you to type complex commands with arguments, it provides a simple, numbered menu to guide you through the available analyses.

Key advantages:

User-Friendly: No need to remember specific command-line flags (--analysis, --start, etc.).

Guided Workflow: Prompts you for the exact information needed for each analysis type.

Environment Setup: Includes a built-in option to set up the necessary Python virtual environment and install dependencies automatically.

🛠️ How to Use
Follow these steps to use the launcher. These only need to be done once.

Step 1: Place Files Together
Ensure that run_analysis.sh, stock_toolkit.py, and requirements.txt are all in the same folder.

Step 2: Make the Script Executable
Before you can run the script for the first time, you must give it "execute" permissions. Open your terminal in the project folder and run the following command:

chmod +x run_analysis.sh

Step 3: Run the Launcher
Now, you can start the interactive menu at any time by running this command:

./run_analysis.sh

Step 4: Set Up the Environment
When you run the launcher for the first time, select Option 4: Setup Environment. This will create a local Python environment and install all the required libraries. You only need to do this once.

📈 Menu Options Explained
Once the launcher is running, you will see the main menu:

Full Analysis (Price, MAs, Volume, RSI)

What it does: Generates a detailed, 3-panel chart for each ticker you enter.

It will ask for: Tickers, start/end dates, and which moving averages to plot.

Performance Comparison

What it does: Creates a single line chart comparing the percentage growth of multiple stocks over time.

It will ask for: Tickers and the start/end dates for the comparison.

Correlation Heatmap

What it does: Generates a heatmap showing how closely the prices of different stocks move together.

It will ask for: Tickers and the start/end dates for the analysis.

Setup Environment (Run this first!)

What it does: Prepares your project by creating a Python virtual environment and installing the libraries from requirements.txt.

When to use: Run this once before performing any analysis.

Exit

What it does: Safely closes the launcher script.
