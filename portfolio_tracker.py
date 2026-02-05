"""
Portfolio Tracker & Trade Visualizer
Tracks paper/real trades and shows performance over time
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import yfinance as yf
import pandas as pd
import numpy as np

# Try to import plotting libraries
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Note: Install matplotlib for charts: pip install matplotlib")


class PortfolioTracker:
    """Track and visualize portfolio performance"""

    def __init__(self):
        self.portfolio_file = os.path.join(os.path.dirname(__file__), "paper_portfolio.json")
        self.trades_file = os.path.join(os.path.dirname(__file__), "trade_history.json")
        self.portfolio = self.load_portfolio()
        self.trade_history = self.load_trade_history()

    def load_portfolio(self) -> Dict:
        """Load portfolio from file"""
        if os.path.exists(self.portfolio_file):
            with open(self.portfolio_file, 'r') as f:
                return json.load(f)
        return {'positions': {}, 'orders': [], 'capital': 500000, 'invested': 0}

    def save_portfolio(self):
        """Save portfolio to file"""
        with open(self.portfolio_file, 'w') as f:
            json.dump(self.portfolio, f, indent=2, default=str)

    def load_trade_history(self) -> List:
        """Load trade history"""
        if os.path.exists(self.trades_file):
            with open(self.trades_file, 'r') as f:
                return json.load(f)
        return []

    def save_trade_history(self):
        """Save trade history"""
        with open(self.trades_file, 'w') as f:
            json.dump(self.trade_history, f, indent=2, default=str)

    def get_stock_data(self, symbol: str, period: str = "1mo") -> Optional[pd.DataFrame]:
        """Fetch stock data"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            return data if not data.empty else None
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None

    def check_trade_status(self, trade: Dict) -> Dict:
        """Check if trade hit target or stoploss"""
        symbol = trade.get('original_symbol') or f"{trade['symbol']}.NS"
        entry_price = trade['executed_price']
        stoploss = trade.get('stoploss', entry_price * 0.95)
        target = trade.get('target', entry_price * 1.10)
        entry_date = trade.get('timestamp', datetime.now().isoformat())

        # Get data since entry
        data = self.get_stock_data(symbol, period="1mo")
        if data is None:
            # Try without suffix
            data = self.get_stock_data(trade['symbol'], period="1mo")

        if data is None or data.empty:
            return {
                'status': 'UNKNOWN',
                'message': 'Could not fetch data',
                'current_price': None
            }

        current_price = data['Close'].iloc[-1]
        high_since_entry = data['High'].max()
        low_since_entry = data['Low'].min()

        # Check if stoploss was hit
        if low_since_entry <= stoploss:
            return {
                'status': 'STOPLOSS_HIT',
                'message': f'Stoploss hit at {stoploss:.2f}',
                'current_price': current_price,
                'exit_price': stoploss,
                'pnl_pct': ((stoploss - entry_price) / entry_price) * 100
            }

        # Check if target was hit
        if high_since_entry >= target:
            return {
                'status': 'TARGET_HIT',
                'message': f'Target hit at {target:.2f}',
                'current_price': current_price,
                'exit_price': target,
                'pnl_pct': ((target - entry_price) / entry_price) * 100
            }

        # Still open
        pnl_pct = ((current_price - entry_price) / entry_price) * 100
        return {
            'status': 'OPEN',
            'message': f'Trade still open',
            'current_price': current_price,
            'pnl_pct': pnl_pct,
            'distance_to_target': ((target - current_price) / current_price) * 100,
            'distance_to_sl': ((current_price - stoploss) / current_price) * 100
        }

    def get_portfolio_status(self) -> str:
        """Get current portfolio status with trade outcomes"""
        orders = self.portfolio.get('orders', [])

        if not orders:
            return "No trades in portfolio"

        report = []
        report.append("=" * 75)
        report.append(" PORTFOLIO STATUS & TRADE TRACKER")
        report.append(" " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        report.append("=" * 75)

        total_invested = 0
        total_current = 0
        total_pnl = 0

        for i, order in enumerate(orders, 1):
            if order.get('status') != 'EXECUTED':
                continue

            symbol = order['symbol']
            qty = order['quantity']
            entry = order['executed_price']
            stoploss = order.get('stoploss', entry * 0.95)
            target = order.get('target', entry * 1.10)

            # Check trade status
            status = self.check_trade_status(order)

            invested = qty * entry
            total_invested += invested

            report.append(f"\n{i}. {symbol}")
            report.append("-" * 70)
            report.append(f"   Entry: Rs.{entry:,.2f} x {qty} = Rs.{invested:,.0f}")
            report.append(f"   Stoploss: Rs.{stoploss:,.2f} | Target: Rs.{target:,.2f}")

            if status['status'] == 'OPEN':
                current = status['current_price']
                current_value = qty * current
                pnl = current_value - invested
                pnl_pct = status['pnl_pct']

                total_current += current_value
                total_pnl += pnl

                report.append(f"   Current: Rs.{current:,.2f}")
                report.append(f"   P&L: Rs.{pnl:+,.0f} ({pnl_pct:+.1f}%)")
                report.append(f"   Status: OPEN - {status['distance_to_target']:.1f}% to target, {status['distance_to_sl']:.1f}% above SL")

            elif status['status'] == 'TARGET_HIT':
                exit_value = qty * status['exit_price']
                pnl = exit_value - invested
                total_current += exit_value
                total_pnl += pnl
                report.append(f"   Status: TARGET HIT!")
                report.append(f"   P&L: Rs.{pnl:+,.0f} ({status['pnl_pct']:+.1f}%)")

            elif status['status'] == 'STOPLOSS_HIT':
                exit_value = qty * status['exit_price']
                pnl = exit_value - invested
                total_current += exit_value
                total_pnl += pnl
                report.append(f"   Status: STOPLOSS HIT")
                report.append(f"   P&L: Rs.{pnl:+,.0f} ({status['pnl_pct']:+.1f}%)")

            else:
                total_current += invested
                report.append(f"   Status: {status['message']}")

        # Summary
        total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0

        report.append("\n" + "=" * 75)
        report.append(" SUMMARY")
        report.append("=" * 75)
        report.append(f"   Total Invested:  Rs.{total_invested:,.0f}")
        report.append(f"   Current Value:   Rs.{total_current:,.0f}")
        report.append(f"   Total P&L:       Rs.{total_pnl:+,.0f} ({total_pnl_pct:+.1f}%)")
        report.append("=" * 75)

        return "\n".join(report)

    def plot_trade_chart(self, symbol: str, entry_price: float, stoploss: float,
                         target: float, period: str = "1mo"):
        """Plot trade chart with entry, SL, and target levels"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib not installed. Run: pip install matplotlib")
            return

        # Clean symbol for yfinance
        data = self.get_stock_data(symbol, period=period)
        if data is None:
            # Try with .NS suffix
            data = self.get_stock_data(f"{symbol}.NS", period=period)

        if data is None or data.empty:
            print(f"Could not fetch data for {symbol}")
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
        fig.suptitle(f'{symbol} - Trade Analysis', fontsize=14, fontweight='bold')

        # Price chart
        ax1.plot(data.index, data['Close'], label='Close Price', color='blue', linewidth=1.5)
        ax1.fill_between(data.index, data['Low'], data['High'], alpha=0.3, color='lightblue')

        # Entry, SL, Target lines
        ax1.axhline(y=entry_price, color='green', linestyle='--', linewidth=2, label=f'Entry: {entry_price:.2f}')
        ax1.axhline(y=stoploss, color='red', linestyle='--', linewidth=2, label=f'Stoploss: {stoploss:.2f}')
        ax1.axhline(y=target, color='orange', linestyle='--', linewidth=2, label=f'Target: {target:.2f}')

        # Shade zones
        ax1.fill_between(data.index, stoploss, entry_price, alpha=0.1, color='red', label='Risk Zone')
        ax1.fill_between(data.index, entry_price, target, alpha=0.1, color='green', label='Reward Zone')

        ax1.set_ylabel('Price')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)

        # Volume chart
        colors = ['green' if data['Close'].iloc[i] >= data['Open'].iloc[i] else 'red'
                  for i in range(len(data))]
        ax2.bar(data.index, data['Volume'], color=colors, alpha=0.7)
        ax2.set_ylabel('Volume')
        ax2.grid(True, alpha=0.3)

        # Format x-axis
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))

        plt.tight_layout()

        # Save chart
        charts_dir = os.path.join(os.path.dirname(__file__), "charts")
        os.makedirs(charts_dir, exist_ok=True)
        chart_path = os.path.join(charts_dir, f"{symbol.replace('.', '_')}_trade.png")
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        print(f"Chart saved: {chart_path}")

        plt.show()

    def plot_all_trades(self, period: str = "1mo"):
        """Plot charts for all trades in portfolio"""
        orders = self.portfolio.get('orders', [])

        for order in orders:
            if order.get('status') == 'EXECUTED':
                symbol = order.get('original_symbol') or order['symbol']
                entry = order['executed_price']
                stoploss = order.get('stoploss', entry * 0.95)
                target = order.get('target', entry * 1.10)

                print(f"\nGenerating chart for {symbol}...")
                self.plot_trade_chart(symbol, entry, stoploss, target, period)

    def get_recommended_holding_period(self) -> str:
        """Get recommended holding period based on trade type"""
        info = """
===============================================================================
 RECOMMENDED ANALYSIS & HOLDING PERIODS
===============================================================================

Based on Zerodha Varsity Technical Analysis Framework:

TRADE TYPE          HOLDING PERIOD      CHART TIMEFRAME     CHECK FREQUENCY
-------------------------------------------------------------------------------
Swing Trading       3-15 days           Daily candles       Daily
Positional          2-8 weeks           Daily/Weekly        Every 2-3 days
Short-term          1-3 months          Weekly candles      Weekly
Investment          6+ months           Weekly/Monthly      Monthly

FOR YOUR CURRENT TRADES:
-------------------------------------------------------------------------------
Since we're using daily candlestick patterns with:
- RSI (14-day)
- Moving Averages (50/200 DMA)
- Support/Resistance levels

RECOMMENDED:
- Holding Period:     5-15 trading days
- Check Frequency:    Daily (after market close)
- Chart Timeframe:    1 month history (for context)
- Exit Strategy:
  * Exit at Target 1 (50% position)
  * Trail stoploss to entry after Target 1
  * Exit remaining at Target 2 or trailed SL

WHEN TO EXIT:
-------------------------------------------------------------------------------
1. TARGET HIT        - Book profits (partial or full)
2. STOPLOSS HIT      - Exit immediately, no averaging
3. TIME STOP         - If no movement in 10-15 days, review
4. PATTERN FAILURE   - If opposite pattern forms, exit

MONITORING SCHEDULE:
-------------------------------------------------------------------------------
- 9:30 AM  - Daily email report (already scheduled)
- 3:30 PM  - Check closing prices
- Weekend  - Weekly review of all positions

===============================================================================
"""
        return info


def main():
    """Main entry point"""
    tracker = PortfolioTracker()

    print("\n" + "=" * 60)
    print(" PORTFOLIO TRACKER & VISUALIZER")
    print("=" * 60)

    print("\nOptions:")
    print("  1. View portfolio status & P&L")
    print("  2. Plot charts for all trades")
    print("  3. Plot chart for specific stock")
    print("  4. View recommended holding periods")
    print("  5. Export portfolio report")
    print("  6. Quit")

    choice = input("\nEnter choice (1-6): ").strip()

    if choice == '1':
        print(tracker.get_portfolio_status())

    elif choice == '2':
        period = input("Enter period (1d/5d/1mo/3mo) [1mo]: ").strip() or "1mo"
        tracker.plot_all_trades(period)

    elif choice == '3':
        symbol = input("Enter stock symbol (e.g., TRENT.NS): ").strip().upper()
        entry = float(input("Entry price: "))
        sl = float(input("Stoploss: "))
        target = float(input("Target: "))
        period = input("Period (1d/5d/1mo/3mo) [1mo]: ").strip() or "1mo"
        tracker.plot_trade_chart(symbol, entry, sl, target, period)

    elif choice == '4':
        print(tracker.get_recommended_holding_period())

    elif choice == '5':
        report = tracker.get_portfolio_status()
        report_file = os.path.join(os.path.dirname(__file__),
                                    f"portfolio_report_{datetime.now().strftime('%Y%m%d')}.txt")
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"Report saved: {report_file}")

    elif choice == '6':
        print("Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
