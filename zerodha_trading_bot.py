"""
Zerodha Trading Bot - Integrated with Technical Analysis Framework
Uses Kite Connect API for order placement

IMPORTANT: This bot requires Kite Connect API subscription (₹2000/month)
Get credentials from: https://developers.kite.trade/
"""

import os
import sys
import json
import logging
from datetime import datetime, time
from typing import Dict, List, Optional
import webbrowser

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from stock_analyzer import ZerodhaAnalyzer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'trading_bot.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class KiteConfig:
    """Kite Connect API configuration"""

    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), "kite_config.json")
        self.config = self.load_config()

    def load_config(self) -> dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

    def save_config(self, config: dict):
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        self.config = config

    def is_configured(self) -> bool:
        return bool(self.config.get('api_key')) and bool(self.config.get('api_secret'))


class ZerodhaTrader:
    """
    Trading bot integrated with Zerodha Kite Connect API
    Uses technical analysis framework for trade signals
    """

    def __init__(self, paper_trading: bool = True):
        self.paper_trading = paper_trading
        self.config = KiteConfig()
        self.analyzer = ZerodhaAnalyzer()
        self.kite = None
        self.positions = {}
        self.orders_placed = []

        # Trading parameters
        self.max_risk_per_trade = 0.02  # 2% of capital
        self.default_capital = 100000  # Default capital for position sizing

        # Order book for paper trading
        self.paper_orders = []
        self.paper_positions = {}

        logger.info(f"Trading Bot initialized - Paper Trading: {paper_trading}")

    def setup_kite_connect(self):
        """Setup Kite Connect API connection"""
        try:
            from kiteconnect import KiteConnect
        except ImportError:
            logger.error("kiteconnect not installed. Run: pip install kiteconnect")
            print("\nInstall Kite Connect: pip install kiteconnect")
            return False

        if not self.config.is_configured():
            logger.error("Kite API not configured")
            return False

        self.kite = KiteConnect(api_key=self.config.config['api_key'])

        # Check if we have access token
        if self.config.config.get('access_token'):
            self.kite.set_access_token(self.config.config['access_token'])
            logger.info("Kite Connect initialized with existing token")
            return True

        # Need to generate new access token
        logger.info("Need to generate access token - opening login page")
        login_url = self.kite.login_url()
        print(f"\nOpen this URL to login: {login_url}")
        webbrowser.open(login_url)

        request_token = input("\nEnter the request_token from redirect URL: ").strip()

        try:
            data = self.kite.generate_session(
                request_token,
                api_secret=self.config.config['api_secret']
            )
            self.config.config['access_token'] = data['access_token']
            self.config.save_config(self.config.config)
            self.kite.set_access_token(data['access_token'])
            logger.info("Access token generated and saved")
            return True
        except Exception as e:
            logger.error(f"Failed to generate session: {e}")
            return False

    def get_instrument_token(self, symbol: str) -> Optional[int]:
        """Get instrument token for a symbol"""
        if self.kite is None:
            return None

        try:
            # Remove .NS or .BO suffix for Kite
            clean_symbol = symbol.replace('.NS', '').replace('.BO', '')

            instruments = self.kite.instruments('NSE')
            for inst in instruments:
                if inst['tradingsymbol'] == clean_symbol:
                    return inst['instrument_token']
            return None
        except Exception as e:
            logger.error(f"Error getting instrument token: {e}")
            return None

    def get_ltp(self, symbol: str) -> Optional[float]:
        """Get last traded price"""
        if self.paper_trading:
            # Use yfinance for paper trading
            import yfinance as yf
            try:
                data = yf.Ticker(symbol).history(period='1d')
                if not data.empty:
                    return data['Close'].iloc[-1]
            except:
                pass
            return None

        if self.kite is None:
            return None

        try:
            clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
            quote = self.kite.quote(f'NSE:{clean_symbol}')
            return quote[f'NSE:{clean_symbol}']['last_price']
        except Exception as e:
            logger.error(f"Error getting LTP: {e}")
            return None

    def calculate_position_size(self, entry: float, stoploss: float, capital: float = None) -> int:
        """Calculate position size based on risk management"""
        if capital is None:
            capital = self.default_capital

        risk_amount = capital * self.max_risk_per_trade
        risk_per_share = abs(entry - stoploss)

        if risk_per_share <= 0:
            return 0

        quantity = int(risk_amount / risk_per_share)
        return max(1, quantity)

    def place_order(self, symbol: str, transaction_type: str, quantity: int,
                    price: float = None, order_type: str = 'MARKET',
                    stoploss: float = None, target: float = None) -> Dict:
        """
        Place an order (paper or real)

        Args:
            symbol: Stock symbol (e.g., 'RELIANCE.NS')
            transaction_type: 'BUY' or 'SELL'
            quantity: Number of shares
            price: Limit price (for LIMIT orders)
            order_type: 'MARKET' or 'LIMIT'
            stoploss: Stoploss price (for bracket orders)
            target: Target price (for bracket orders)
        """
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')

        order = {
            'symbol': clean_symbol,
            'original_symbol': symbol,
            'transaction_type': transaction_type,
            'quantity': quantity,
            'price': price,
            'order_type': order_type,
            'stoploss': stoploss,
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'status': 'PENDING'
        }

        if self.paper_trading:
            return self._place_paper_order(order)
        else:
            return self._place_real_order(order)

    def _place_paper_order(self, order: Dict) -> Dict:
        """Place a paper (simulated) order"""
        ltp = self.get_ltp(order['original_symbol'])

        if ltp is None:
            order['status'] = 'REJECTED'
            order['message'] = 'Could not get current price'
            logger.warning(f"Paper order rejected: {order['symbol']} - no price data")
            return order

        order['executed_price'] = ltp if order['order_type'] == 'MARKET' else order['price']
        order['status'] = 'EXECUTED'
        order['order_id'] = f"PAPER_{len(self.paper_orders) + 1}_{datetime.now().strftime('%H%M%S')}"

        # Update paper positions
        symbol = order['symbol']
        if symbol not in self.paper_positions:
            self.paper_positions[symbol] = {'quantity': 0, 'avg_price': 0}

        pos = self.paper_positions[symbol]
        if order['transaction_type'] == 'BUY':
            total_value = (pos['quantity'] * pos['avg_price']) + (order['quantity'] * order['executed_price'])
            pos['quantity'] += order['quantity']
            pos['avg_price'] = total_value / pos['quantity'] if pos['quantity'] > 0 else 0
        else:  # SELL
            pos['quantity'] -= order['quantity']
            if pos['quantity'] <= 0:
                pos['quantity'] = 0
                pos['avg_price'] = 0

        self.paper_orders.append(order)

        logger.info(f"PAPER ORDER: {order['transaction_type']} {order['quantity']} {order['symbol']} @ {order['executed_price']}")

        return order

    def _place_real_order(self, order: Dict) -> Dict:
        """Place a real order via Kite Connect"""
        if self.kite is None:
            order['status'] = 'REJECTED'
            order['message'] = 'Kite not connected'
            return order

        try:
            from kiteconnect import KiteConnect

            params = {
                'tradingsymbol': order['symbol'],
                'exchange': 'NSE',
                'transaction_type': self.kite.TRANSACTION_TYPE_BUY if order['transaction_type'] == 'BUY' else self.kite.TRANSACTION_TYPE_SELL,
                'quantity': order['quantity'],
                'product': self.kite.PRODUCT_CNC,  # Delivery
                'order_type': self.kite.ORDER_TYPE_MARKET if order['order_type'] == 'MARKET' else self.kite.ORDER_TYPE_LIMIT,
            }

            if order['order_type'] == 'LIMIT':
                params['price'] = order['price']

            order_id = self.kite.place_order(variety=self.kite.VARIETY_REGULAR, **params)

            order['order_id'] = order_id
            order['status'] = 'PLACED'

            logger.info(f"REAL ORDER PLACED: {order['transaction_type']} {order['quantity']} {order['symbol']} - Order ID: {order_id}")

            self.orders_placed.append(order)
            return order

        except Exception as e:
            order['status'] = 'REJECTED'
            order['message'] = str(e)
            logger.error(f"Order failed: {e}")
            return order

    def analyze_and_suggest(self, symbols: List[str] = None) -> List[Dict]:
        """
        Analyze stocks and suggest trades based on 7-point checklist
        """
        if symbols is None:
            # Load from watchlist
            watchlist_path = os.path.join(os.path.dirname(__file__), "watchlist.txt")
            if os.path.exists(watchlist_path):
                with open(watchlist_path, 'r') as f:
                    symbols = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        suggestions = []

        for symbol in symbols:
            analysis = self.analyzer.analyze_stock(symbol)

            if analysis is None:
                continue

            verdict = analysis['verdict']
            checklist = analysis['checklist_result']

            if verdict['verdict'] == 'BUY' and checklist['score'] >= 5:
                sr = analysis['support_resistance']
                ma = analysis['moving_averages']

                entry = ma['current_price']
                stoploss = sr['immediate_support']
                target1 = sr['immediate_resistance']
                target2 = sr['strong_resistance']

                quantity = self.calculate_position_size(entry, stoploss)

                suggestion = {
                    'symbol': symbol,
                    'action': 'BUY',
                    'entry': round(entry, 2),
                    'stoploss': round(stoploss, 2),
                    'target1': round(target1, 2),
                    'target2': round(target2, 2),
                    'quantity': quantity,
                    'checklist_score': f"{checklist['score']}/7",
                    'confidence': verdict['confidence'],
                    'rsi': analysis['rsi'],
                    'analysis': analysis
                }
                suggestions.append(suggestion)

                logger.info(f"BUY Signal: {symbol} @ {entry} | SL: {stoploss} | Target: {target1}")

        return suggestions

    def execute_suggestions(self, suggestions: List[Dict], require_confirmation: bool = True) -> List[Dict]:
        """Execute trade suggestions"""
        executed = []

        for suggestion in suggestions:
            print(f"\n{'='*60}")
            print(f"TRADE SIGNAL: {suggestion['action']} {suggestion['symbol']}")
            print(f"{'='*60}")
            print(f"Entry:      ₹{suggestion['entry']}")
            print(f"Stoploss:   ₹{suggestion['stoploss']} ({((suggestion['entry']-suggestion['stoploss'])/suggestion['entry']*100):.1f}% risk)")
            print(f"Target 1:   ₹{suggestion['target1']} ({((suggestion['target1']-suggestion['entry'])/suggestion['entry']*100):.1f}% reward)")
            print(f"Target 2:   ₹{suggestion['target2']}")
            print(f"Quantity:   {suggestion['quantity']} shares")
            print(f"Investment: ₹{suggestion['quantity'] * suggestion['entry']:,.0f}")
            print(f"Checklist:  {suggestion['checklist_score']} | RSI: {suggestion['rsi']}")
            print(f"Confidence: {suggestion['confidence']}")

            if require_confirmation:
                confirm = input(f"\nExecute this trade? (y/n/skip all): ").strip().lower()

                if confirm == 'skip all':
                    print("Skipping all remaining trades.")
                    break
                elif confirm != 'y':
                    print("Skipped.")
                    continue

            # Place the order
            order = self.place_order(
                symbol=suggestion['symbol'],
                transaction_type='BUY',
                quantity=suggestion['quantity'],
                order_type='MARKET',
                stoploss=suggestion['stoploss'],
                target=suggestion['target1']
            )

            suggestion['order'] = order
            executed.append(suggestion)

            if order['status'] in ['EXECUTED', 'PLACED']:
                print(f"\n✓ Order {order['status']}: {order.get('order_id', 'N/A')}")
            else:
                print(f"\n✗ Order {order['status']}: {order.get('message', 'Unknown error')}")

        return executed

    def get_positions(self) -> Dict:
        """Get current positions"""
        if self.paper_trading:
            return self.paper_positions

        if self.kite is None:
            return {}

        try:
            positions = self.kite.positions()
            return positions
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return {}

    def get_portfolio_summary(self) -> str:
        """Get portfolio summary"""
        positions = self.get_positions()

        if not positions:
            return "No positions"

        summary = "\n" + "="*60 + "\n"
        summary += " PORTFOLIO SUMMARY\n"
        summary += "="*60 + "\n\n"

        total_investment = 0
        total_current = 0

        for symbol, pos in positions.items():
            if pos['quantity'] > 0:
                ltp = self.get_ltp(f"{symbol}.NS") or pos['avg_price']
                investment = pos['quantity'] * pos['avg_price']
                current = pos['quantity'] * ltp
                pnl = current - investment
                pnl_pct = (pnl / investment * 100) if investment > 0 else 0

                total_investment += investment
                total_current += current

                summary += f"{symbol}:\n"
                summary += f"  Qty: {pos['quantity']} | Avg: ₹{pos['avg_price']:.2f} | LTP: ₹{ltp:.2f}\n"
                summary += f"  P&L: ₹{pnl:,.2f} ({pnl_pct:+.1f}%)\n\n"

        total_pnl = total_current - total_investment
        total_pnl_pct = (total_pnl / total_investment * 100) if total_investment > 0 else 0

        summary += "-"*60 + "\n"
        summary += f"Total Investment: ₹{total_investment:,.2f}\n"
        summary += f"Current Value:    ₹{total_current:,.2f}\n"
        summary += f"Total P&L:        ₹{total_pnl:,.2f} ({total_pnl_pct:+.1f}%)\n"
        summary += "="*60 + "\n"

        return summary


def setup_kite_credentials():
    """Interactive setup for Kite Connect credentials"""
    print("\n" + "="*60)
    print(" KITE CONNECT API SETUP")
    print("="*60)

    print("\nTo use this bot with real trading, you need:")
    print("  1. Zerodha trading account")
    print("  2. Kite Connect API subscription (₹2000/month)")
    print("  3. API Key and Secret from https://developers.kite.trade/")

    config = KiteConfig()

    if config.is_configured():
        print(f"\nExisting configuration found:")
        print(f"  API Key: {config.config.get('api_key', 'N/A')[:8]}...")

        update = input("\nUpdate credentials? (y/n): ").strip().lower()
        if update != 'y':
            return

    print("\nEnter your Kite Connect credentials:")
    api_key = input("API Key: ").strip()
    api_secret = input("API Secret: ").strip()

    if api_key and api_secret:
        config.save_config({
            'api_key': api_key,
            'api_secret': api_secret
        })
        print("\nCredentials saved!")
    else:
        print("\nInvalid credentials. Setup cancelled.")


def main():
    """Main entry point"""
    print("\n" + "="*60)
    print(" ZERODHA TRADING BOT")
    print(" Technical Analysis + Order Execution")
    print("="*60)

    print("\nOptions:")
    print("  1. Analyze watchlist & suggest trades (Paper Trading)")
    print("  2. Analyze watchlist & suggest trades (Real Trading)")
    print("  3. View portfolio (Paper)")
    print("  4. View order history (Paper)")
    print("  5. Setup Kite Connect API")
    print("  6. Run automated scanner")
    print("  7. Quit")

    choice = input("\nEnter choice (1-7): ").strip()

    if choice == '1':
        # Paper trading mode
        bot = ZerodhaTrader(paper_trading=True)
        print("\n[PAPER TRADING MODE - No real orders will be placed]\n")

        print("Analyzing watchlist...")
        suggestions = bot.analyze_and_suggest()

        if suggestions:
            print(f"\nFound {len(suggestions)} BUY signals!")
            executed = bot.execute_suggestions(suggestions, require_confirmation=True)
            print(f"\nExecuted {len(executed)} paper trades")
            print(bot.get_portfolio_summary())
        else:
            print("\nNo strong BUY signals found based on 7-point checklist.")

    elif choice == '2':
        # Real trading mode
        config = KiteConfig()
        if not config.is_configured():
            print("\nKite Connect not configured. Run option 5 first.")
            return

        bot = ZerodhaTrader(paper_trading=False)

        if not bot.setup_kite_connect():
            print("\nFailed to connect to Kite. Check credentials.")
            return

        print("\n[REAL TRADING MODE - Orders will be placed on your Zerodha account]\n")

        confirm = input("Are you sure you want to proceed with REAL trading? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Cancelled.")
            return

        print("Analyzing watchlist...")
        suggestions = bot.analyze_and_suggest()

        if suggestions:
            print(f"\nFound {len(suggestions)} BUY signals!")
            executed = bot.execute_suggestions(suggestions, require_confirmation=True)
            print(f"\nPlaced {len(executed)} orders")
        else:
            print("\nNo strong BUY signals found.")

    elif choice == '3':
        bot = ZerodhaTrader(paper_trading=True)
        print(bot.get_portfolio_summary())

    elif choice == '4':
        bot = ZerodhaTrader(paper_trading=True)
        if bot.paper_orders:
            print("\n" + "="*60)
            print(" PAPER ORDER HISTORY")
            print("="*60)
            for order in bot.paper_orders:
                print(f"\n{order['timestamp']}")
                print(f"  {order['transaction_type']} {order['quantity']} {order['symbol']}")
                print(f"  Price: ₹{order.get('executed_price', 'N/A')} | Status: {order['status']}")
        else:
            print("\nNo paper orders yet.")

    elif choice == '5':
        setup_kite_credentials()

    elif choice == '6':
        print("\n[AUTOMATED SCANNER - Paper Trading Mode]")
        bot = ZerodhaTrader(paper_trading=True)

        print("\nScanning watchlist for opportunities...")
        suggestions = bot.analyze_and_suggest()

        if suggestions:
            print(f"\n{'='*60}")
            print(f" SCAN RESULTS - {len(suggestions)} BUY SIGNALS")
            print(f"{'='*60}")

            for i, s in enumerate(suggestions, 1):
                print(f"\n{i}. {s['symbol']}")
                print(f"   Entry: ₹{s['entry']} | SL: ₹{s['stoploss']} | Target: ₹{s['target1']}")
                print(f"   Score: {s['checklist_score']} | RSI: {s['rsi']} | {s['confidence']}")
        else:
            print("\nNo BUY signals found. Market conditions may not be favorable.")

    elif choice == '7':
        print("Goodbye!")
        sys.exit(0)

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
