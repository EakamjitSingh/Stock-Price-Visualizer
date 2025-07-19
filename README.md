#!/bin/bash

# ==============================================================================
# Bash Launcher for the Advanced Stock Analysis Toolkit
#
# This script provides a user-friendly menu to run the Python analysis tool
# without needing to remember command-line arguments.
# ==============================================================================

# --- Configuration ---
PYTHON_SCRIPT="stock_toolkit.py"
REQUIREMENTS_FILE="requirements.txt"
VENV_DIR="venv"

# --- Helper Functions ---

# Function to print a formatted header
print_header() {
    echo "==============================================="
    echo "    Advanced Stock Analysis Toolkit Launcher   "
    echo "==============================================="
    echo
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# --- Core Functions ---

# Function to set up the Python environment
setup_environment() {
    echo "[*] Setting up the environment..."

    # Check for Python
    if ! command_exists python; then
        echo "❌ Error: Python is not installed or not in the system's PATH."
        exit 1
    fi

    # Check for requirements file
    if [ ! -f "$REQUIREMENTS_FILE" ]; then
        echo "❌ Error: '$REQUIREMENTS_FILE' not found. Please create it first."
        exit 1
    fi

    # Create virtual environment
    if [ ! -d "$VENV_DIR" ]; then
        echo "[*] Creating Python virtual environment in './$VENV_DIR'..."
        python -m venv "$VENV_DIR"
    else
        echo "[*] Virtual environment already exists."
    fi

    # Activate virtual environment and install dependencies
    echo "[*] Installing dependencies from '$REQUIREMENTS_FILE'..."
    source "$VENV_DIR/bin/activate"
    pip install -r "$REQUIREMENTS_FILE"

    echo
    echo "✅ Setup complete. You can now run the analysis options."
    deactivate
    echo
}

# Function to run the Python script with the correct arguments
run_analysis() {
    if [ ! -d "$VENV_DIR" ]; then
        echo "⚠️ Warning: Environment not set up. Please run 'Setup Environment' first."
        return
    fi

    # Activate the virtual environment to run the script
    source "$VENV_DIR/bin/activate"
    echo "[*] Running: python $PYTHON_SCRIPT $@"
    echo "-----------------------------------------------"
    python "$PYTHON_SCRIPT" "$@"
    echo "-----------------------------------------------"
    deactivate
}

# --- Main Menu ---

main_menu() {
    while true; do
        print_header
        echo "Select an analysis to perform:"
        echo "  1) Full Analysis (Price, MAs, Volume, RSI)"
        echo "  2) Performance Comparison"
        echo "  3) Correlation Heatmap"
        echo "  4) Setup Environment (Run this first!)"
        echo "  5) Exit"
        echo
        read -p "Enter your choice [1-5]: " choice

        case $choice in
            1)
                read -p "Enter stock tickers (comma-separated, e.g., AAPL,MSFT): " tickers
                read -p "Enter start date (YYYY-MM-DD, press Enter for last year): " start_date
                read -p "Enter end date (YYYY-MM-DD, press Enter for today): " end_date
                read -p "Enter Moving Averages (comma-separated, e.g., 50,200): " ma_windows

                # Build arguments, handling empty inputs
                args=("$tickers" --analysis full)
                [ -n "$start_date" ] && args+=("--start" "$start_date")
                [ -n "$end_date" ] && args+=("--end" "$end_date")
                [ -n "$ma_windows" ] && args+=("--ma" "$ma_windows")
                
                run_analysis "${args[@]}"
                ;;
            2)
                read -p "Enter stock tickers (comma-separated, e.g., AAPL,MSFT): " tickers
                read -p "Enter start date (YYYY-MM-DD, press Enter for last year): " start_date
                read -p "Enter end date (YYYY-MM-DD, press Enter for today): " end_date

                args=("$tickers" --analysis compare)
                [ -n "$start_date" ] && args+=("--start" "$start_date")
                [ -n "$end_date" ] && args+=("--end" "$end_date")

                run_analysis "${args[@]}"
                ;;
            3)
                read -p "Enter stock tickers (comma-separated, e.g., AAPL,MSFT): " tickers
                read -p "Enter start date (YYYY-MM-DD, press Enter for last year): " start_date
                read -p "Enter end date (YYYY-MM-DD, press Enter for today): " end_date

                args=("$tickers" --analysis corr)
                [ -n "$start_date" ] && args+=("--start" "$start_date")
                [ -n "$end_date" ] && args+=("--end" "$end_date")

                run_analysis "${args[@]}"
                ;;
            4)
                setup_environment
                ;;
            5)
                echo "Exiting toolkit. Goodbye!"
                exit 0
                ;;
            *)
                echo "❌ Invalid choice. Please select a number from 1 to 5."
                ;;
        esac
        read -p "Press Enter to return to the menu..."
    done
}

# --- Script Entry Point ---
main_menu

