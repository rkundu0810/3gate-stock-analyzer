"""
Stock Analysis Dashboard - Flask Web Application
3-Gate Analysis + Portfolio Tracking + Zerodha Integration (Read-Only)
"""

import os
import json
import uuid
import time
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from flask import (Flask, render_template, request, jsonify,
                   redirect, url_for, send_from_directory)

from stock_analyzer import ZerodhaAnalyzer
from email_scheduler import get_stocks_from_file

# ---------------------------------------------------------------------------
# APP SETUP
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.secret_key = os.urandom(24)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# BACKGROUND TASK SYSTEM
# ---------------------------------------------------------------------------
executor = ThreadPoolExecutor(max_workers=3)
tasks = {}
tasks_lock = Lock()

RESULTS_DIR = os.path.join(BASE_DIR, 'analysis_results')
os.makedirs(RESULTS_DIR, exist_ok=True)


def cleanup_old_tasks():
    """Remove tasks older than 1 hour."""
    cutoff = time.time() - 3600
    with tasks_lock:
        expired = [tid for tid, t in tasks.items() if t.get('started', 0) < cutoff]
        for tid in expired:
            del tasks[tid]

# ---------------------------------------------------------------------------
# LTP CACHE
# ---------------------------------------------------------------------------
ltp_cache = {}
LTP_CACHE_TTL = 30  # seconds


def get_cached_ltp(symbol):
    """Get last traded price with 30s cache."""
    now = time.time()
    if symbol in ltp_cache and (now - ltp_cache[symbol][1]) < LTP_CACHE_TTL:
        return ltp_cache[symbol][0]
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        data = ticker.history(period='1d')
        if data is not None and not data.empty:
            price = round(float(data['Close'].iloc[-1]), 2)
            ltp_cache[symbol] = (price, now)
            return price
    except Exception:
        pass
    return None

# ---------------------------------------------------------------------------
# KITE CLIENT
# ---------------------------------------------------------------------------
_kite_client = None
_kite_config = None


def load_kite_config():
    global _kite_config
    config_path = os.path.join(BASE_DIR, 'kite_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            _kite_config = json.load(f)
    else:
        _kite_config = {}
    return _kite_config


def save_kite_config(config):
    global _kite_config
    config_path = os.path.join(BASE_DIR, 'kite_config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    _kite_config = config


def get_kite_client():
    """Get or create Kite Connect client."""
    global _kite_client
    config = load_kite_config()
    if not config.get('api_key') or not config.get('access_token'):
        return None
    try:
        from kiteconnect import KiteConnect
        _kite_client = KiteConnect(api_key=config['api_key'])
        _kite_client.set_access_token(config['access_token'])
        return _kite_client
    except Exception:
        return None


def kite_is_connected():
    """Check if Kite client is authenticated."""
    kite = get_kite_client()
    if kite is None:
        return False
    try:
        kite.profile()
        return True
    except Exception:
        return False

# ---------------------------------------------------------------------------
# WATCHLIST HELPERS
# ---------------------------------------------------------------------------
WATCHLIST_PATH = os.path.join(BASE_DIR, 'watchlist.txt')


def read_watchlist():
    """Read watchlist, stripping inline comments."""
    return get_stocks_from_file()


def add_to_watchlist(symbol):
    """Add a stock to the end of watchlist.txt."""
    symbol = symbol.strip().upper()
    current = read_watchlist()
    if symbol in [s.upper() for s in current]:
        return False
    with open(WATCHLIST_PATH, 'a') as f:
        f.write(f"\n{symbol}")
    return True


def remove_from_watchlist(symbol):
    """Remove a stock from watchlist.txt while preserving comments."""
    symbol = symbol.strip().upper()
    if not os.path.exists(WATCHLIST_PATH):
        return False
    with open(WATCHLIST_PATH, 'r') as f:
        lines = f.readlines()
    new_lines = []
    removed = False
    for line in lines:
        clean = line.split('#')[0].strip().upper()
        if clean == symbol:
            removed = True
            continue
        new_lines.append(line)
    if removed:
        with open(WATCHLIST_PATH, 'w') as f:
            f.writelines(new_lines)
    return removed

# ---------------------------------------------------------------------------
# PORTFOLIO HELPERS
# ---------------------------------------------------------------------------
PAPER_PORTFOLIO_PATH = os.path.join(BASE_DIR, 'paper_portfolio.json')


def load_paper_portfolio():
    if os.path.exists(PAPER_PORTFOLIO_PATH):
        with open(PAPER_PORTFOLIO_PATH, 'r') as f:
            return json.load(f)
    return {'positions': {}, 'orders': [], 'capital': 500000, 'invested': 0}

# ---------------------------------------------------------------------------
# ANALYSIS HISTORY HELPERS
# ---------------------------------------------------------------------------


def list_analysis_files():
    """List analysis report files sorted by date (newest first)."""
    files = []
    for f in os.listdir(RESULTS_DIR):
        if f.endswith('.txt') or f.endswith('.html'):
            filepath = os.path.join(RESULTS_DIR, f)
            mtime = os.path.getmtime(filepath)
            files.append({
                'filename': f,
                'date': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M'),
                'size': os.path.getsize(filepath),
            })
    files.sort(key=lambda x: x['date'], reverse=True)
    return files

# ---------------------------------------------------------------------------
# BACKGROUND ANALYSIS WORKERS
# ---------------------------------------------------------------------------


def run_single_analysis(task_id, symbol):
    """Background worker for single stock analysis."""
    try:
        analyzer = ZerodhaAnalyzer()
        result = analyzer.analyze_stock(symbol)
        with tasks_lock:
            if result:
                tasks[task_id]['status'] = 'complete'
                tasks[task_id]['result'] = result
                tasks[task_id]['report'] = analyzer.format_report(result)
            else:
                tasks[task_id]['status'] = 'error'
                tasks[task_id]['error'] = f'Insufficient data for {symbol}'
    except Exception as e:
        with tasks_lock:
            tasks[task_id]['status'] = 'error'
            tasks[task_id]['error'] = str(e)


def run_batch_analysis(task_id, symbols):
    """Background worker for batch stock analysis."""
    analyzer = ZerodhaAnalyzer()
    results = []
    for i, symbol in enumerate(symbols):
        with tasks_lock:
            tasks[task_id]['current'] = symbol
            tasks[task_id]['completed'] = i
        try:
            result = analyzer.analyze_stock(symbol.strip())
            if result:
                results.append(result)
                with tasks_lock:
                    tasks[task_id]['results'] = results.copy()
        except Exception as e:
            logger.warning(f"Batch analysis failed for {symbol}: {e}")
        time.sleep(0.5)  # Rate limiting

    with tasks_lock:
        tasks[task_id]['status'] = 'complete'
        tasks[task_id]['completed'] = len(symbols)
        tasks[task_id]['results'] = results

    # Save batch report
    try:
        report = analyzer.run_analysis([r['symbol'] for r in results])
    except Exception:
        pass

# ===========================================================================
# PAGE ROUTES
# ===========================================================================


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/analyze')
def analyze_page():
    symbol = request.args.get('symbol', '')
    return render_template('analyze.html', symbol=symbol)


@app.route('/portfolio')
def portfolio_page():
    return render_template('portfolio.html')


@app.route('/watchlist')
def watchlist_page():
    return render_template('watchlist.html')


@app.route('/history')
def history_page():
    return render_template('history.html')


@app.route('/settings')
def settings_page():
    return render_template('settings.html')

# ===========================================================================
# API ROUTES: ANALYSIS
# ===========================================================================


@app.route('/api/analyze', methods=['POST'])
def start_analysis():
    data = request.get_json(force=True)
    symbol = data.get('symbol', '').strip().upper()
    if not symbol:
        return jsonify({'error': 'Symbol required'}), 400

    cleanup_old_tasks()
    task_id = str(uuid.uuid4())[:8]
    with tasks_lock:
        tasks[task_id] = {
            'type': 'single',
            'status': 'running',
            'symbol': symbol,
            'result': None,
            'started': time.time(),
        }
    executor.submit(run_single_analysis, task_id, symbol)
    return jsonify({'task_id': task_id, 'status': 'running'})


@app.route('/api/analyze/<task_id>')
def get_analysis(task_id):
    with tasks_lock:
        task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    response = {
        'task_id': task_id,
        'status': task['status'],
        'symbol': task.get('symbol', ''),
    }
    if task['status'] == 'complete' and task.get('result'):
        response['result'] = _serialize_analysis(task['result'])
        response['report'] = task.get('report', '')
    elif task['status'] == 'error':
        response['error'] = task.get('error', 'Unknown error')
    return jsonify(response)


@app.route('/api/analyze/batch', methods=['POST'])
def start_batch_analysis():
    data = request.get_json(force=True)
    symbols = data.get('symbols', [])
    if not symbols:
        symbols = read_watchlist()
    if not symbols:
        return jsonify({'error': 'No stocks to analyze'}), 400

    cleanup_old_tasks()
    task_id = str(uuid.uuid4())[:8]
    with tasks_lock:
        tasks[task_id] = {
            'type': 'batch',
            'status': 'running',
            'total': len(symbols),
            'completed': 0,
            'current': symbols[0] if symbols else '',
            'results': [],
            'started': time.time(),
        }
    executor.submit(run_batch_analysis, task_id, symbols)
    return jsonify({'task_id': task_id, 'status': 'running', 'total': len(symbols)})


@app.route('/api/analyze/batch/<task_id>')
def get_batch_analysis(task_id):
    with tasks_lock:
        task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    response = {
        'task_id': task_id,
        'status': task['status'],
        'total': task.get('total', 0),
        'completed': task.get('completed', 0),
        'current': task.get('current', ''),
    }
    if task.get('results'):
        response['results'] = [_serialize_analysis(r) for r in task['results']]
    return jsonify(response)


def _serialize_analysis(result):
    """Make analysis result JSON-safe."""
    if result is None:
        return None
    # Convert any non-serializable values
    serialized = {}
    for key, val in result.items():
        if isinstance(val, dict):
            serialized[key] = _serialize_dict(val)
        elif isinstance(val, (int, float, str, bool, type(None))):
            serialized[key] = val
        elif isinstance(val, list):
            serialized[key] = val
        else:
            serialized[key] = str(val)
    return serialized


def _serialize_dict(d):
    """Recursively serialize a dict."""
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            out[k] = _serialize_dict(v)
        elif isinstance(v, (int, float, str, bool, type(None), list)):
            out[k] = v
        else:
            out[k] = str(v)
    return out

# ===========================================================================
# API ROUTES: WATCHLIST
# ===========================================================================


@app.route('/api/watchlist')
def api_get_watchlist():
    stocks = read_watchlist()
    return jsonify({'stocks': stocks, 'count': len(stocks)})


@app.route('/api/watchlist', methods=['POST'])
def api_add_to_watchlist():
    data = request.get_json(force=True)
    symbol = data.get('symbol', '').strip().upper()
    if not symbol:
        return jsonify({'error': 'Symbol required'}), 400
    added = add_to_watchlist(symbol)
    if added:
        return jsonify({'message': f'{symbol} added', 'symbol': symbol})
    return jsonify({'error': f'{symbol} already in watchlist'}), 409


@app.route('/api/watchlist/<symbol>', methods=['DELETE'])
def api_remove_from_watchlist(symbol):
    removed = remove_from_watchlist(symbol)
    if removed:
        return jsonify({'message': f'{symbol} removed'})
    return jsonify({'error': f'{symbol} not found'}), 404

# ===========================================================================
# API ROUTES: PORTFOLIO
# ===========================================================================


@app.route('/api/portfolio/paper')
def api_paper_portfolio():
    portfolio = load_paper_portfolio()
    return jsonify(portfolio)


@app.route('/api/portfolio/zerodha')
def api_zerodha_portfolio():
    kite = get_kite_client()
    if kite is None:
        return jsonify({'error': 'kite_not_connected', 'message': 'Zerodha not connected'}), 401
    try:
        holdings = kite.holdings()
        positions = kite.positions()
        margins = kite.margins()
        profile = kite.profile()
        return jsonify({
            'holdings': holdings,
            'positions': positions,
            'margins': margins,
            'profile': profile,
        })
    except Exception as e:
        return jsonify({'error': 'kite_error', 'message': str(e)}), 401


@app.route('/api/portfolio/summary')
def api_portfolio_summary():
    portfolio = load_paper_portfolio()
    positions = portfolio.get('positions', {})
    capital = portfolio.get('capital', 500000)
    invested = portfolio.get('invested', 0)

    total_value = capital
    holdings_count = len(positions)

    return jsonify({
        'capital': capital,
        'invested': invested,
        'holdings_count': holdings_count,
        'kite_connected': kite_is_connected(),
    })

# ===========================================================================
# API ROUTES: MARKET DATA
# ===========================================================================


@app.route('/api/ltp')
def api_ltp():
    symbols_str = request.args.get('symbols', '')
    if not symbols_str:
        return jsonify({}), 400
    symbols = [s.strip() for s in symbols_str.split(',') if s.strip()]
    prices = {}

    # Try Kite first
    kite = get_kite_client()
    if kite:
        try:
            kite_syms = []
            for s in symbols:
                if '.NS' in s:
                    kite_syms.append(f"NSE:{s.replace('.NS', '')}")
                elif '.BO' in s:
                    kite_syms.append(f"BSE:{s.replace('.BO', '')}")
            if kite_syms:
                quotes = kite.ltp(kite_syms)
                for ks in kite_syms:
                    if ks in quotes:
                        # Map back to original symbol format
                        exchange, sym = ks.split(':')
                        suffix = '.NS' if exchange == 'NSE' else '.BO'
                        prices[sym + suffix] = quotes[ks]['last_price']
        except Exception:
            pass

    # Fallback to yfinance for missing
    for s in symbols:
        if s not in prices:
            p = get_cached_ltp(s)
            if p:
                prices[s] = p

    return jsonify(prices)

# ===========================================================================
# API ROUTES: HISTORY
# ===========================================================================


@app.route('/api/history')
def api_history():
    files = list_analysis_files()
    limit = request.args.get('limit', 20, type=int)
    return jsonify({'files': files[:limit]})


@app.route('/api/history/<filename>')
def api_history_file(filename):
    # Security: only allow files from the results directory
    safe_name = os.path.basename(filename)
    filepath = os.path.join(RESULTS_DIR, safe_name)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return jsonify({'filename': safe_name, 'content': content})

# ===========================================================================
# API ROUTES: KITE AUTH
# ===========================================================================


@app.route('/api/kite/status')
def api_kite_status():
    config = load_kite_config()
    connected = kite_is_connected()
    return jsonify({
        'configured': bool(config.get('api_key')),
        'connected': connected,
    })


@app.route('/api/kite/login')
def api_kite_login():
    config = load_kite_config()
    if not config.get('api_key'):
        return jsonify({'error': 'API key not configured. Go to Settings.'}), 400
    try:
        from kiteconnect import KiteConnect
        kite = KiteConnect(api_key=config['api_key'])
        login_url = kite.login_url()
        return jsonify({'login_url': login_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/kite/callback')
def api_kite_callback():
    request_token = request.args.get('request_token')
    status = request.args.get('status')
    if status != 'success' or not request_token:
        return redirect(url_for('settings_page') + '?error=auth_failed')
    config = load_kite_config()
    try:
        from kiteconnect import KiteConnect
        kite = KiteConnect(api_key=config['api_key'])
        data = kite.generate_session(request_token, api_secret=config['api_secret'])
        config['access_token'] = data['access_token']
        save_kite_config(config)
        return redirect(url_for('portfolio_page') + '?kite=connected')
    except Exception as e:
        return redirect(url_for('settings_page') + f'?error={str(e)}')


@app.route('/api/settings/kite', methods=['POST'])
def api_save_kite_config():
    data = request.get_json(force=True)
    config = load_kite_config()
    if data.get('api_key'):
        config['api_key'] = data['api_key'].strip()
    if data.get('api_secret'):
        config['api_secret'] = data['api_secret'].strip()
    save_kite_config(config)
    return jsonify({'message': 'Kite config saved'})


# ===========================================================================
# MAIN
# ===========================================================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "=" * 60)
    print("  Stock Analysis Dashboard")
    print(f"  http://127.0.0.1:{port}")
    print("=" * 60 + "\n")
    app.run(debug=True, host='0.0.0.0', port=port)
