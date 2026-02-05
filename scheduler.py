"""
Daily Stock Analysis Scheduler
Runs at 9 AM daily and prompts for stock list
"""

import schedule
import time
from datetime import datetime
import subprocess
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from stock_analyzer import ZerodhaAnalyzer


def get_stocks_from_file() -> list:
    """Read stock list from watchlist file"""
    watchlist_path = os.path.join(os.path.dirname(__file__), "watchlist.txt")
    if os.path.exists(watchlist_path):
        with open(watchlist_path, 'r') as f:
            stocks = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return stocks
    return []


def prompt_for_stocks() -> list:
    """Interactive prompt for stock list"""
    print("\n" + "="*60)
    print(f" DAILY STOCK ANALYSIS - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)

    # Check for watchlist file first
    default_stocks = get_stocks_from_file()
    if default_stocks:
        print(f"\nFound watchlist with {len(default_stocks)} stocks:")
        print(f"  {', '.join(default_stocks[:10])}{'...' if len(default_stocks) > 10 else ''}")
        print("\nOptions:")
        print("  1. Press Enter to analyze watchlist")
        print("  2. Type stock symbols to analyze different stocks")
        print("  3. Type 'add:SYMBOL' to add to watchlist")
        print("  4. Type 'quit' to exit")

    else:
        print("\nNo watchlist found. Enter stocks to analyze.")
        print("Tip: Create 'watchlist.txt' with one stock per line for defaults")

    user_input = input("\n> ").strip()

    if user_input.lower() == 'quit':
        return []

    if user_input.lower().startswith('add:'):
        symbol = user_input[4:].strip().upper()
        if symbol:
            watchlist_path = os.path.join(os.path.dirname(__file__), "watchlist.txt")
            with open(watchlist_path, 'a') as f:
                f.write(f"\n{symbol}")
            print(f"Added {symbol} to watchlist")
            default_stocks.append(symbol)
        return default_stocks

    if not user_input and default_stocks:
        return default_stocks

    if user_input:
        return [s.strip().upper() for s in user_input.split(',') if s.strip()]

    return default_stocks


def run_daily_analysis():
    """Run the daily analysis routine"""
    print("\n" + "#"*60)
    print(f" 9 AM STOCK ANALYSIS TRIGGERED")
    print(f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("#"*60)

    stocks = prompt_for_stocks()

    if not stocks:
        print("No stocks to analyze. Skipping...")
        return

    analyzer = ZerodhaAnalyzer()
    report = analyzer.run_analysis(stocks)
    print(report)

    # Show notification on Windows
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
            "Stock Analysis Complete",
            f"Analyzed {len(stocks)} stocks. Check results folder.",
            duration=10
        )
    except ImportError:
        pass


def run_scheduler():
    """Run the scheduler in background mode"""
    print("\n" + "="*60)
    print(" STOCK ANALYSIS SCHEDULER - BACKGROUND MODE")
    print("="*60)
    print(f"\nScheduler started at {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("Analysis will run daily at 9:00 AM")
    print("Press Ctrl+C to stop\n")

    # Schedule daily at 9 AM
    schedule.every().day.at("09:00").do(run_daily_analysis)

    # Also run on market open times for different markets
    schedule.every().day.at("09:15").do(lambda: print("Indian market opened!"))
    schedule.every().day.at("19:00").do(lambda: print("US market pre-market!"))

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


def main():
    """Main entry point with options"""
    print("\n" + "="*60)
    print(" STOCK ANALYSIS SCHEDULER")
    print("="*60)
    print("\nOptions:")
    print("  1. Run analysis NOW (interactive)")
    print("  2. Start background scheduler (9 AM daily)")
    print("  3. Setup Windows Task Scheduler")
    print("  4. Edit watchlist")
    print("  5. Quit")

    choice = input("\nEnter choice (1-5): ").strip()

    if choice == '1':
        run_daily_analysis()

    elif choice == '2':
        run_scheduler()

    elif choice == '3':
        setup_windows_scheduler()

    elif choice == '4':
        edit_watchlist()

    elif choice == '5':
        print("Goodbye!")
        sys.exit(0)

    else:
        print("Invalid choice")


def edit_watchlist():
    """Edit the watchlist file"""
    watchlist_path = os.path.join(os.path.dirname(__file__), "watchlist.txt")

    print("\n" + "="*60)
    print(" WATCHLIST EDITOR")
    print("="*60)

    if os.path.exists(watchlist_path):
        with open(watchlist_path, 'r') as f:
            current = f.read()
        print("\nCurrent watchlist:")
        print(current)
    else:
        print("\nNo watchlist found. Creating new one...")

    print("\nOptions:")
    print("  add SYMBOL    - Add a stock")
    print("  remove SYMBOL - Remove a stock")
    print("  clear         - Clear all")
    print("  done          - Finish editing")

    stocks = get_stocks_from_file()

    while True:
        cmd = input("\n> ").strip().lower()

        if cmd == 'done':
            break
        elif cmd.startswith('add '):
            symbol = cmd[4:].strip().upper()
            if symbol and symbol not in stocks:
                stocks.append(symbol)
                print(f"Added {symbol}")
        elif cmd.startswith('remove '):
            symbol = cmd[7:].strip().upper()
            if symbol in stocks:
                stocks.remove(symbol)
                print(f"Removed {symbol}")
        elif cmd == 'clear':
            stocks = []
            print("Cleared watchlist")
        elif cmd == 'list':
            print(f"Current: {', '.join(stocks)}")

    # Save
    with open(watchlist_path, 'w') as f:
        f.write("# Stock Watchlist - One symbol per line\n")
        f.write("# Examples: RELIANCE, TCS.NS, INFY.BO, AAPL, MSFT\n\n")
        for s in stocks:
            f.write(f"{s}\n")

    print(f"\nSaved {len(stocks)} stocks to watchlist")


def setup_windows_scheduler():
    """Setup Windows Task Scheduler for daily 9 AM run"""
    print("\n" + "="*60)
    print(" WINDOWS TASK SCHEDULER SETUP")
    print("="*60)

    script_path = os.path.abspath(__file__)
    python_path = sys.executable

    # Create a batch file for the task
    batch_path = os.path.join(os.path.dirname(__file__), "run_analysis.bat")
    batch_content = f'''@echo off
cd /d "{os.path.dirname(script_path)}"
"{python_path}" "{script_path}" --run-now
pause
'''

    with open(batch_path, 'w') as f:
        f.write(batch_content)

    print(f"\nCreated batch file: {batch_path}")

    # Create PowerShell script to set up task
    ps_script = f'''
$action = New-ScheduledTaskAction -Execute "{batch_path}"
$trigger = New-ScheduledTaskTrigger -Daily -At 9:00AM
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "DailyStockAnalysis" -Action $action -Trigger $trigger -Settings $settings -Description "Daily stock analysis at 9 AM"
'''

    print("\nTo set up automatic scheduling, run PowerShell as Administrator and execute:")
    print("-"*60)
    print(ps_script)
    print("-"*60)

    print("\nAlternatively, run this command in CMD (as Administrator):")
    cmd = f'schtasks /create /tn "DailyStockAnalysis" /tr "{batch_path}" /sc daily /st 09:00'
    print(f"\n{cmd}")

    create_now = input("\nTry to create task now? (y/n): ").strip().lower()
    if create_now == 'y':
        try:
            result = subprocess.run(
                ['schtasks', '/create', '/tn', 'DailyStockAnalysis',
                 '/tr', batch_path, '/sc', 'daily', '/st', '09:00', '/f'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("\nTask created successfully!")
                print("Analysis will run daily at 9:00 AM")
            else:
                print(f"\nFailed: {result.stderr}")
                print("Try running as Administrator")
        except Exception as e:
            print(f"\nError: {e}")
            print("Please run the command manually as Administrator")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--run-now':
        run_daily_analysis()
    else:
        main()
