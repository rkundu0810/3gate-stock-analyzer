"""
3-Gate Stock Analysis Framework
Gate 1: Fundamental Quality (10-Point Checklist)
Gate 2: Valuation Filter (Intrinsic Value vs Market Price)
Gate 3: Technical Timing (Zerodha 7-Point Checklist)

Supports Indian (NSE/BSE) and US (NASDAQ/NYSE) markets.
Based on Dalal Street Integrated Framework + Zerodha Varsity.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import re
from typing import Dict, List, Optional, Tuple
import warnings
import logging

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_SCRAPING = True
except ImportError:
    HAS_SCRAPING = False

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)


def safe_get(info: dict, key: str, default=None):
    """Safely get a value, handling None and NaN."""
    val = info.get(key, default)
    if val is None:
        return default
    if isinstance(val, float) and (pd.isna(val) or np.isinf(val)):
        return default
    return val


class ZerodhaAnalyzer:
    """3-Gate Analysis: Fundamental + Valuation + Technical"""

    BANKING_KEYWORDS = ['bank', 'banking', 'banks—regional', 'banks—diversified']
    NBFC_KEYWORDS = [
        'credit services', 'financial conglomerates', 'mortgage finance',
        'housing finance', 'infrastructure finance', 'power finance',
        'financial data', 'capital markets',
    ]

    def __init__(self):
        self.results_dir = os.path.join(os.path.dirname(__file__), "analysis_results")
        os.makedirs(self.results_dir, exist_ok=True)

    # ------------------------------------------------------------------
    # SCREENER.IN DATA FETCHING
    # ------------------------------------------------------------------

    def _screener_symbol(self, symbol: str) -> Optional[str]:
        """Convert trading symbol to Screener.in company slug.
        LUPIN.NS -> LUPIN, HDFCBANK.BO -> HDFCBANK, AAPL -> None (US stock)."""
        s = symbol.strip().upper()
        if s.endswith('.NS') or s.endswith('.BO'):
            return s.rsplit('.', 1)[0]
        # No dot = could be Indian or US; skip Screener for US stocks
        if '.' not in s and not any(c in s for c in ['^']):
            return s  # Will try Screener, fall back gracefully
        return None

    def _parse_screener_number(self, text: str) -> Optional[float]:
        """Parse Screener.in formatted number: '1,01,378' -> 101378, '21.9 %' -> 21.9."""
        if not text:
            return None
        text = text.strip().replace('₹', '').replace('Cr.', '').replace('%', '').replace('\n', '').strip()
        text = text.replace(',', '')
        try:
            return float(text)
        except (ValueError, TypeError):
            return None

    def fetch_from_screener(self, symbol: str) -> Optional[Dict]:
        """Fetch fundamental data from Screener.in for Indian stocks.
        Returns dict with standardized keys or None on failure."""
        if not HAS_SCRAPING:
            logger.warning("requests/beautifulsoup4 not installed, skipping Screener.in")
            return None

        slug = self._screener_symbol(symbol)
        if not slug:
            return None

        url = f"https://www.screener.in/company/{slug}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code != 200:
                logger.warning(f"Screener.in returned {resp.status_code} for {slug}")
                return None
            soup = BeautifulSoup(resp.text, 'html.parser')
        except Exception as e:
            logger.warning(f"Screener.in fetch failed for {slug}: {e}")
            return None

        data = {}

        # --- TOP RATIOS (#top-ratios) ---
        top = soup.find(id='top-ratios')
        if top:
            for li in top.find_all('li'):
                name_el = li.find('span', class_='name')
                val_el = li.find('span', class_='value') or li.find('span', class_='nowrap')
                if not name_el or not val_el:
                    continue
                name = name_el.text.strip()
                val = self._parse_screener_number(val_el.text)

                if 'Market Cap' in name and val:
                    data['market_cap_cr'] = val
                elif name == 'Stock P/E' and val:
                    data['pe'] = val
                elif name == 'Book Value' and val:
                    data['book_value'] = val
                elif 'Dividend Yield' in name and val:
                    data['dividend_yield'] = val
                elif name == 'ROCE' and val:
                    data['roce'] = val
                elif name == 'ROE' and val:
                    data['roe'] = val
                elif 'Current Price' in name and val:
                    data['current_price'] = val
                elif 'High / Low' in name:
                    hl_text = val_el.text.strip().replace('₹', '').replace(',', '')
                    parts = hl_text.split('/')
                    if len(parts) == 2:
                        try:
                            data['52w_high'] = float(parts[0].strip())
                            data['52w_low'] = float(parts[1].strip())
                        except ValueError:
                            pass
                elif name == 'Face Value' and val:
                    data['face_value'] = val

        # --- P&L GROWTH TABLES (ranges-table inside #profit-loss) ---
        pl_section = soup.find(id='profit-loss')
        if pl_section:
            for table in pl_section.find_all('table', class_='ranges-table'):
                rows = table.find_all('tr')
                if not rows:
                    continue
                header = rows[0].text.strip()

                for tr in rows[1:]:
                    cells = [td.text.strip() for td in tr.find_all('td')]
                    if len(cells) != 2:
                        continue
                    period, value = cells[0].rstrip(':'), cells[1].rstrip('%')

                    if 'Compounded Sales Growth' in header:
                        if '3 Year' in period:
                            data['rev_cagr_3y'] = self._parse_screener_number(value)
                        elif '5 Year' in period:
                            data['rev_cagr_5y'] = self._parse_screener_number(value)
                    elif 'Compounded Profit Growth' in header:
                        if '3 Year' in period:
                            data['pat_cagr_3y'] = self._parse_screener_number(value)
                        elif '5 Year' in period:
                            data['pat_cagr_5y'] = self._parse_screener_number(value)
                    elif 'Return on Equity' in header:
                        if 'Last Year' in period:
                            data['roe_last_year'] = self._parse_screener_number(value)

            # P&L data table - extract OPM from latest year
            for table in pl_section.find_all('table', class_='data-table'):
                for tr in table.find_all('tr'):
                    cells = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                    if not cells:
                        continue
                    label = cells[0].replace('\xa0+', '').replace('\xa0', '').strip()

                    if label == 'OPM %' and len(cells) > 2:
                        # Get latest year (second to last = latest annual, last = TTM)
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['opm'] = self._parse_screener_number(latest.rstrip('%'))
                    elif label == 'Net Profit' and len(cells) > 2:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['net_profit_cr'] = self._parse_screener_number(latest)
                    elif label == 'EPS in Rs' and len(cells) > 2:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['eps'] = self._parse_screener_number(latest)
                    elif label == 'Dividend Payout %' and len(cells) > 2:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['payout_ratio'] = self._parse_screener_number(latest.rstrip('%'))
                break  # Only first data-table in P&L

        # --- QUARTERLY RESULTS (bank-specific: GNPA, NNPA, Financing Margin) ---
        q_section = soup.find(id='quarters')
        if q_section:
            for table in q_section.find_all('table', class_='data-table')[:1]:
                for tr in table.find_all('tr'):
                    cells = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                    if not cells:
                        continue
                    label = cells[0].replace('\xa0+', '').replace('\xa0', '').strip()

                    if label == 'Gross NPA %' and len(cells) > 1:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['gnpa'] = self._parse_screener_number(latest.rstrip('%'))
                    elif label == 'Net NPA %' and len(cells) > 1:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['nnpa'] = self._parse_screener_number(latest.rstrip('%'))
                    elif label == 'Financing Margin %' and len(cells) > 1:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['financing_margin'] = self._parse_screener_number(latest.rstrip('%'))

        # --- SHAREHOLDING (#shareholding) ---
        shp_section = soup.find(id='shareholding')
        if shp_section:
            # Use the first table (quarterly)
            for table in shp_section.find_all('table', class_='data-table')[:1]:
                for tr in table.find_all('tr'):
                    cells = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                    if not cells:
                        continue
                    label = cells[0].replace('\xa0+', '').replace('\xa0', '').strip()

                    if label == 'Promoters' and len(cells) > 1:
                        latest = cells[-1]
                        data['promoter_holding'] = self._parse_screener_number(latest.rstrip('%'))
                    elif label == 'FIIs' and len(cells) > 1:
                        latest = cells[-1]
                        data['fii_holding'] = self._parse_screener_number(latest.rstrip('%'))
                    elif label == 'DIIs' and len(cells) > 1:
                        latest = cells[-1]
                        data['dii_holding'] = self._parse_screener_number(latest.rstrip('%'))

        # --- CASH FLOW (#cash-flow) ---
        cf_section = soup.find(id='cash-flow')
        if cf_section:
            for table in cf_section.find_all('table', class_='data-table')[:1]:
                for tr in table.find_all('tr'):
                    cells = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                    if not cells:
                        continue
                    label = cells[0].replace('\xa0+', '').replace('\xa0', '').strip()

                    if 'Cash from Operating' in label and len(cells) > 1:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['ocf_cr'] = self._parse_screener_number(latest)

        # --- BALANCE SHEET (#balance-sheet) ---
        bs_section = soup.find(id='balance-sheet')
        if bs_section:
            borrowings = None
            equity_plus_reserves = None
            for table in bs_section.find_all('table', class_='data-table')[:1]:
                for tr in table.find_all('tr'):
                    cells = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                    if not cells:
                        continue
                    label = cells[0].replace('\xa0+', '').replace('\xa0', '').strip()

                    if label == 'Borrowings' and len(cells) > 1:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        borrowings = self._parse_screener_number(latest)
                        data['borrowings_cr'] = borrowings
                    elif label == 'Equity Capital' and len(cells) > 1:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        eq = self._parse_screener_number(latest)
                        data['equity_capital_cr'] = eq
                    elif label == 'Reserves' and len(cells) > 1:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        res = self._parse_screener_number(latest)
                        data['reserves_cr'] = res

            # Calculate D/E from balance sheet
            eq_cap = data.get('equity_capital_cr', 0) or 0
            reserves = data.get('reserves_cr', 0) or 0
            total_equity = eq_cap + reserves
            if total_equity > 0 and borrowings is not None:
                data['de_ratio'] = round(borrowings / total_equity, 2)

        # --- RATIOS (#ratios) ---
        ratios_section = soup.find(id='ratios')
        if ratios_section:
            for table in ratios_section.find_all('table', class_='data-table')[:1]:
                for tr in table.find_all('tr'):
                    cells = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                    if not cells:
                        continue
                    label = cells[0].replace('\xa0', '').strip()

                    if label == 'ROCE %' and len(cells) > 1:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['roce_annual'] = self._parse_screener_number(latest.rstrip('%'))
                    elif label == 'ROE %' and len(cells) > 1:
                        latest = cells[-1] if cells[-1] else cells[-2]
                        data['roe_annual'] = self._parse_screener_number(latest.rstrip('%'))

        # --- Compute P/B from price and book value ---
        if data.get('current_price') and data.get('book_value') and data['book_value'] > 0:
            data['pb'] = round(data['current_price'] / data['book_value'], 2)

        # --- Compute EV/EBITDA if we have OPM and Sales ---
        # (Not directly available, keep from yfinance)

        data['_source'] = 'screener.in'
        return data if data else None

    # ------------------------------------------------------------------
    # DATA FETCHING (yfinance + Screener.in merge)
    # ------------------------------------------------------------------

    def _resolve_ticker(self, symbol: str) -> Tuple[Optional[object], Optional[pd.DataFrame], str]:
        """Resolve symbol to yfinance Ticker + price data. Returns (ticker, data, resolved_symbol)."""
        symbol = symbol.strip()
        attempts = []

        if any(x in symbol.upper() for x in ['.NS', '.BO', '^']):
            attempts = [symbol]
        elif '.' in symbol:
            attempts = [symbol]
        else:
            attempts = [symbol, f"{symbol}.NS", f"{symbol}.BO"]

        for sym in attempts:
            try:
                ticker = yf.Ticker(sym)
                data = ticker.history(period="1y")
                if data is not None and not data.empty and len(data) >= 50:
                    return ticker, data, sym.upper()
            except Exception:
                continue

        return None, None, symbol.upper()

    def get_fundamentals(self, ticker, symbol: str = '') -> Dict:
        """Fetch fundamental data from yfinance + Screener.in (for Indian stocks).
        Screener.in data takes priority for: ROCE, promoter holding, growth CAGR, OCF, D/E."""
        try:
            info = ticker.info or {}
        except Exception:
            info = {}

        # Revenue and PAT CAGR from yfinance annual financials (fallback)
        rev_cagr, pat_cagr = self._calc_growth_cagr(ticker, years=3)

        # D/E from yfinance is in percentage form (e.g. 45 = 0.45 ratio)
        raw_de = safe_get(info, 'debtToEquity')
        de_ratio = round(raw_de / 100, 2) if raw_de is not None and raw_de > 10 else raw_de

        roe_raw = safe_get(info, 'returnOnEquity')
        roe_pct = round(roe_raw * 100, 2) if roe_raw is not None and abs(roe_raw) < 5 else roe_raw

        roa_raw = safe_get(info, 'returnOnAssets')
        roa_pct = round(roa_raw * 100, 2) if roa_raw is not None and abs(roa_raw) < 5 else roa_raw

        gm_raw = safe_get(info, 'grossMargins')
        gm_pct = round(gm_raw * 100, 2) if gm_raw is not None and abs(gm_raw) < 5 else gm_raw

        om_raw = safe_get(info, 'operatingMargins')
        om_pct = round(om_raw * 100, 2) if om_raw is not None and abs(om_raw) < 5 else om_raw

        pm_raw = safe_get(info, 'profitMargins')
        pm_pct = round(pm_raw * 100, 2) if pm_raw is not None and abs(pm_raw) < 5 else pm_raw

        dy_raw = safe_get(info, 'dividendYield')
        dy_pct = round(dy_raw * 100, 2) if dy_raw is not None and dy_raw < 0.20 else (
            round(dy_raw, 2) if dy_raw is not None and dy_raw < 20 else None)

        insider_hold = safe_get(info, 'heldPercentInsiders')
        insider_pct = round(insider_hold * 100, 2) if insider_hold is not None and insider_hold < 2 else insider_hold

        result = {
            'market_cap': safe_get(info, 'marketCap'),
            'sector': safe_get(info, 'sector', 'Unknown'),
            'industry': safe_get(info, 'industry', 'Unknown'),
            'pe': safe_get(info, 'trailingPE'),
            'forward_pe': safe_get(info, 'forwardPE'),
            'pb': safe_get(info, 'priceToBook'),
            'roe': roe_pct,
            'roce': None,  # yfinance doesn't provide ROCE
            'roa': roa_pct,
            'de_ratio': de_ratio,
            'current_ratio': safe_get(info, 'currentRatio'),
            'gross_margin': gm_pct,
            'operating_margin': om_pct,
            'profit_margin': pm_pct,
            'dividend_yield': dy_pct,
            'payout_ratio': safe_get(info, 'payoutRatio'),
            'revenue': safe_get(info, 'totalRevenue'),
            'total_debt': safe_get(info, 'totalDebt'),
            'total_cash': safe_get(info, 'totalCash'),
            'ocf': safe_get(info, 'operatingCashflow'),
            'fcf': safe_get(info, 'freeCashflow'),
            'earnings_growth_qoq': safe_get(info, 'earningsGrowth'),
            'revenue_growth_qoq': safe_get(info, 'revenueGrowth'),
            'rev_cagr_3y': rev_cagr,
            'pat_cagr_3y': pat_cagr,
            'book_value': safe_get(info, 'bookValue'),
            'eps': safe_get(info, 'trailingEps'),
            'insider_pct': insider_pct,
            'promoter_holding': None,
            'beta': safe_get(info, 'beta'),
            'enterprise_value': safe_get(info, 'enterpriseValue'),
            'ev_ebitda': safe_get(info, 'enterpriseToEbitda'),
            'ev_revenue': safe_get(info, 'enterpriseToRevenue'),
            # Banking-specific (populated by Screener.in)
            'gnpa': None,
            'nnpa': None,
            'financing_margin': None,
            'data_source': 'yfinance',
        }

        # --- Merge Screener.in data for Indian stocks ---
        screener = self.fetch_from_screener(symbol)
        if screener:
            result['data_source'] = 'screener.in + yfinance'

            # Screener.in values override yfinance where available and more reliable
            if screener.get('pe'):
                result['pe'] = screener['pe']
            if screener.get('pb'):
                result['pb'] = screener['pb']
            if screener.get('roe') is not None:
                result['roe'] = screener['roe']
            if screener.get('roce') is not None:
                result['roce'] = screener['roce']
            if screener.get('roce_annual') is not None:
                result['roce'] = screener['roce_annual']
            if screener.get('book_value'):
                result['book_value'] = screener['book_value']
            if screener.get('dividend_yield') is not None:
                result['dividend_yield'] = screener['dividend_yield']
            if screener.get('eps'):
                result['eps'] = screener['eps']
            if screener.get('market_cap_cr'):
                result['market_cap'] = screener['market_cap_cr'] * 1e7  # Cr to absolute

            # D/E from balance sheet (more reliable than yfinance for Indian stocks)
            if screener.get('de_ratio') is not None:
                result['de_ratio'] = screener['de_ratio']

            # Growth CAGR from Screener (always prefer over yfinance calculation)
            if screener.get('rev_cagr_3y') is not None:
                result['rev_cagr_3y'] = screener['rev_cagr_3y']
            if screener.get('pat_cagr_3y') is not None:
                result['pat_cagr_3y'] = screener['pat_cagr_3y']

            # Operating Profit Margin from P&L
            if screener.get('opm') is not None:
                result['operating_margin'] = screener['opm']

            # Promoter holding (much more accurate than yfinance insider %)
            if screener.get('promoter_holding') is not None:
                result['promoter_holding'] = screener['promoter_holding']
                result['insider_pct'] = screener['promoter_holding']

            # OCF from cash flow statement (in Cr, convert to absolute)
            if screener.get('ocf_cr') is not None:
                result['ocf'] = screener['ocf_cr'] * 1e7  # Cr to absolute

            # Banking-specific
            if screener.get('gnpa') is not None:
                result['gnpa'] = screener['gnpa']
            if screener.get('nnpa') is not None:
                result['nnpa'] = screener['nnpa']
            if screener.get('financing_margin') is not None:
                result['financing_margin'] = screener['financing_margin']

            # Institutional holding (for widely-held company detection)
            if screener.get('fii_holding') is not None:
                result['fii_holding'] = screener['fii_holding']
            if screener.get('dii_holding') is not None:
                result['dii_holding'] = screener['dii_holding']

        return result

    def _calc_growth_cagr(self, ticker, years: int = 3) -> Tuple[Optional[float], Optional[float]]:
        """Calculate revenue and PAT CAGR from annual financials."""
        try:
            fin = ticker.financials
            if fin is None or fin.empty:
                return None, None

            rev_cagr = None
            pat_cagr = None

            # Revenue
            for label in ['Total Revenue', 'Operating Revenue', 'Revenue']:
                if label in fin.index:
                    row = fin.loc[label].dropna().sort_index(ascending=False)
                    if len(row) >= 2:
                        n = min(years, len(row) - 1)
                        latest, past = row.iloc[0], row.iloc[n]
                        if past > 0 and latest > 0:
                            rev_cagr = round(((latest / past) ** (1 / n) - 1) * 100, 1)
                    break

            # PAT
            for label in ['Net Income', 'Net Income From Continuing Ops', 'Net Income Common Stockholders']:
                if label in fin.index:
                    row = fin.loc[label].dropna().sort_index(ascending=False)
                    if len(row) >= 2:
                        n = min(years, len(row) - 1)
                        latest, past = row.iloc[0], row.iloc[n]
                        if past > 0 and latest > 0:
                            pat_cagr = round(((latest / past) ** (1 / n) - 1) * 100, 1)
                    break

            return rev_cagr, pat_cagr
        except Exception:
            return None, None

    # ------------------------------------------------------------------
    # SECTOR DETECTION
    # ------------------------------------------------------------------

    def detect_sector_type(self, fundamentals: Dict) -> str:
        """Detect sector type: 'banking', 'nbfc', or 'general'."""
        industry = (fundamentals.get('industry') or '').lower()
        sector = (fundamentals.get('sector') or '').lower()

        if any(kw in industry for kw in self.BANKING_KEYWORDS):
            return 'banking'
        if any(kw in industry for kw in self.NBFC_KEYWORDS):
            return 'nbfc'
        if 'financial' in sector and ('bank' in industry or 'credit' in industry):
            return 'nbfc'
        return 'general'

    # ------------------------------------------------------------------
    # GATE 1: FUNDAMENTAL CHECKLIST (10-Point)
    # ------------------------------------------------------------------

    def apply_fundamental_checklist(self, fund: Dict, sector_type: str) -> Dict:
        """Gate 1: 10-Point Fundamental Quality Checklist."""
        checklist = {}
        score = 0
        assessed = 0

        if sector_type in ('banking', 'nbfc'):
            return self._banking_fundamental_checklist(fund, sector_type)

        # 1. Gross/Operating Profit Margin > 20%
        margin = fund.get('gross_margin') or fund.get('operating_margin')
        if margin is not None:
            passed = margin > 20
            checklist['1_profit_margin'] = {'pass': passed, 'detail': f"Margin: {margin:.1f}% (need >20%)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['1_profit_margin'] = {'pass': None, 'detail': "Data N/A"}

        # 2. ROE > 15%
        roe = fund.get('roe')
        if roe is not None:
            passed = roe > 15
            checklist['2_roe'] = {'pass': passed, 'detail': f"ROE: {roe:.1f}% (need >15%)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['2_roe'] = {'pass': None, 'detail': "Data N/A"}

        # 3. ROCE > 15%
        roce = fund.get('roce')
        roa = fund.get('roa')
        if roce is not None:
            passed = roce > 15
            checklist['3_roce'] = {'pass': passed, 'detail': f"ROCE: {roce:.1f}% (need >15%)"}
            if passed: score += 1
            assessed += 1
        elif roa is not None:
            passed = roa > 5
            checklist['3_roce'] = {'pass': passed, 'detail': f"ROA: {roa:.1f}% (proxy, need >5%)"}
            if passed: score += 1
            assessed += 1
        elif roe is not None and roe > 20:
            checklist['3_roce'] = {'pass': True, 'detail': f"ROE {roe:.1f}% strong (ROCE likely >15%)"}
            score += 1
            assessed += 1
        else:
            checklist['3_roce'] = {'pass': None, 'detail': "Data N/A"}

        # 4. Debt/Equity < 1
        de = fund.get('de_ratio')
        if de is not None:
            passed = de < 1
            checklist['4_debt_equity'] = {'pass': passed, 'detail': f"D/E: {de:.2f} (need <1)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['4_debt_equity'] = {'pass': None, 'detail': "Data N/A"}

        # 5. Interest Coverage > 3x (use OCF/Debt as proxy)
        ocf = fund.get('ocf')
        debt = fund.get('total_debt')
        if de is not None and de < 0.05:
            checklist['5_interest_coverage'] = {'pass': True, 'detail': "Nearly debt-free"}
            score += 1
            assessed += 1
        elif ocf is not None and debt is not None and debt > 0:
            coverage = ocf / (debt * 0.08)  # Assume ~8% interest rate
            passed = coverage > 3
            checklist['5_interest_coverage'] = {'pass': passed, 'detail': f"Est. coverage: {coverage:.1f}x (need >3x)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['5_interest_coverage'] = {'pass': None, 'detail': "Data N/A"}

        # 6. Operating Cash Flow Positive
        if ocf is not None:
            passed = ocf > 0
            ocf_cr = ocf / 1e7  # Convert to Cr for Indian stocks
            checklist['6_ocf'] = {'pass': passed, 'detail': f"OCF: {ocf_cr:,.0f} Cr"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['6_ocf'] = {'pass': None, 'detail': "Data N/A"}

        # 7. Revenue Growth > 10% CAGR
        rev_cagr = fund.get('rev_cagr_3y')
        if rev_cagr is not None:
            passed = rev_cagr > 10
            checklist['7_rev_growth'] = {'pass': passed, 'detail': f"Rev CAGR 3Y: {rev_cagr:.1f}% (need >10%)"}
            if passed: score += 1
            assessed += 1
        else:
            # Fallback to QoQ
            rg = fund.get('revenue_growth_qoq')
            if rg is not None:
                rg_pct = rg * 100 if abs(rg) < 5 else rg
                passed = rg_pct > 10
                checklist['7_rev_growth'] = {'pass': passed, 'detail': f"Rev Growth QoQ: {rg_pct:.1f}% (need >10%)"}
                if passed: score += 1
                assessed += 1
            else:
                checklist['7_rev_growth'] = {'pass': None, 'detail': "Data N/A"}

        # 8. PAT Growth > 12% CAGR
        pat_cagr = fund.get('pat_cagr_3y')
        if pat_cagr is not None:
            passed = pat_cagr > 12
            checklist['8_pat_growth'] = {'pass': passed, 'detail': f"PAT CAGR 3Y: {pat_cagr:.1f}% (need >12%)"}
            if passed: score += 1
            assessed += 1
        else:
            eg = fund.get('earnings_growth_qoq')
            if eg is not None:
                eg_pct = eg * 100 if abs(eg) < 5 else eg
                passed = eg_pct > 12
                checklist['8_pat_growth'] = {'pass': passed, 'detail': f"Earnings Growth QoQ: {eg_pct:.1f}% (need >12%)"}
                if passed: score += 1
                assessed += 1
            else:
                checklist['8_pat_growth'] = {'pass': None, 'detail': "Data N/A"}

        # 9. Promoter Holding > 50% (use Screener promoter data, fallback to yfinance insider)
        promoter = fund.get('promoter_holding') or fund.get('insider_pct')
        is_screener_promoter = fund.get('promoter_holding') is not None
        if promoter is not None:
            passed = promoter > 50
            label = "Promoter" if is_screener_promoter else "Insider"
            checklist['9_promoter'] = {'pass': passed, 'detail': f"{label}: {promoter:.1f}% (need >50%)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['9_promoter'] = {'pass': None, 'detail': "Data N/A"}

        # 10. Free Cash Flow Positive
        fcf = fund.get('fcf')
        if fcf is not None:
            passed = fcf > 0
            fcf_cr = fcf / 1e7
            checklist['10_fcf'] = {'pass': passed, 'detail': f"FCF: {fcf_cr:,.0f} Cr"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['10_fcf'] = {'pass': None, 'detail': "Data N/A"}

        # Normalize score to /10 scale if some items are N/A
        if assessed > 0:
            normalized_score = round(score / assessed * 10, 1)
        else:
            normalized_score = 0

        gate_pass = (assessed >= 5 and score / assessed >= 0.7) or score >= 7

        return {
            'checklist': checklist,
            'score': score,
            'assessed': assessed,
            'total': 10,
            'normalized': normalized_score,
            'pass_rate': round(score / max(assessed, 1) * 100, 1),
            'gate_pass': gate_pass,
        }

    def _banking_fundamental_checklist(self, fund: Dict, sector_type: str) -> Dict:
        """Specialized fundamental checklist for Banking/NBFC.
        Uses banking-specific metrics from Screener.in (GNPA, NNPA, Financing Margin)."""
        checklist = {}
        score = 0
        assessed = 0

        # 1. ROE > 12% (banks typically have lower ROE)
        roe = fund.get('roe')
        if roe is not None:
            passed = roe > 12
            checklist['1_roe'] = {'pass': passed, 'detail': f"ROE: {roe:.1f}% (need >12%)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['1_roe'] = {'pass': None, 'detail': "Data N/A"}

        # 2. ROA > 1% (key banking metric)
        roa = fund.get('roa')
        if roa is not None:
            passed = roa > 1
            checklist['2_roa'] = {'pass': passed, 'detail': f"ROA: {roa:.1f}% (need >1%)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['2_roa'] = {'pass': None, 'detail': "Data N/A"}

        # 3. GNPA < 3% (from Screener.in quarterly, key asset quality metric)
        gnpa = fund.get('gnpa')
        if gnpa is not None:
            passed = gnpa < 3
            checklist['3_gnpa'] = {'pass': passed, 'detail': f"GNPA: {gnpa:.2f}% (need <3%)"}
            if passed: score += 1
            assessed += 1
        else:
            # Fallback: P/B < 3
            pb = fund.get('pb')
            if pb is not None:
                passed = pb < 3
                checklist['3_gnpa'] = {'pass': passed, 'detail': f"P/B: {pb:.2f} (proxy, need <3 for banks)"}
                if passed: score += 1
                assessed += 1
            else:
                checklist['3_gnpa'] = {'pass': None, 'detail': "GNPA data N/A"}

        # 4. NNPA < 1.5% (net non-performing assets)
        nnpa = fund.get('nnpa')
        if nnpa is not None:
            passed = nnpa < 1.5
            checklist['4_nnpa'] = {'pass': passed, 'detail': f"NNPA: {nnpa:.2f}% (need <1.5%)"}
            if passed: score += 1
            assessed += 1
        else:
            # Fallback: P/B assessment
            pb = fund.get('pb')
            if pb is not None:
                passed = pb < 3
                checklist['4_nnpa'] = {'pass': passed, 'detail': f"P/B: {pb:.2f} (NNPA data N/A, using P/B proxy)"}
                if passed: score += 1
                assessed += 1
            else:
                checklist['4_nnpa'] = {'pass': None, 'detail': "NNPA data N/A"}

        # 5. Revenue/NII Growth > 10%
        rev_cagr = fund.get('rev_cagr_3y')
        if rev_cagr is not None:
            passed = rev_cagr > 10
            checklist['5_rev_growth'] = {'pass': passed, 'detail': f"Rev CAGR 3Y: {rev_cagr:.1f}% (need >10%)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['5_rev_growth'] = {'pass': None, 'detail': "Data N/A"}

        # 6. PAT Growth > 12%
        pat_cagr = fund.get('pat_cagr_3y')
        if pat_cagr is not None:
            passed = pat_cagr > 12
            checklist['6_pat_growth'] = {'pass': passed, 'detail': f"PAT CAGR 3Y: {pat_cagr:.1f}% (need >12%)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['6_pat_growth'] = {'pass': None, 'detail': "Data N/A"}

        # 7. Promoter Holding (RBI cap for banks, so 20%+ is fine)
        promoter = fund.get('promoter_holding') or fund.get('insider_pct')
        is_screener = fund.get('promoter_holding') is not None
        if promoter is not None:
            threshold = 20 if sector_type == 'banking' else 50
            passed = promoter >= threshold
            note = " (RBI cap applies)" if sector_type == 'banking' else ""
            label = "Promoter" if is_screener else "Insider"
            checklist['7_promoter'] = {'pass': passed, 'detail': f"{label}: {promoter:.1f}% (need >{threshold}%{note})"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['7_promoter'] = {'pass': None, 'detail': "Data N/A"}

        # 8. Dividend Yield > 0.5% (banks should reward shareholders)
        dy = fund.get('dividend_yield')
        if dy is not None:
            passed = dy > 0.5
            checklist['8_dividend'] = {'pass': passed, 'detail': f"Div Yield: {dy:.2f}%"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['8_dividend'] = {'pass': None, 'detail': "Data N/A"}

        # 9. P/E reasonable (< 20 for banks)
        pe = fund.get('pe')
        if pe is not None:
            passed = pe < 20
            checklist['9_pe_value'] = {'pass': passed, 'detail': f"P/E: {pe:.1f} (need <20 for banks)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['9_pe_value'] = {'pass': None, 'detail': "Data N/A"}

        # 10. P/B reasonable (< 3 for banks, value indicator)
        pb = fund.get('pb')
        if pb is not None:
            passed = pb < 3
            checklist['10_pb_value'] = {'pass': passed, 'detail': f"P/B: {pb:.2f} (need <3 for banks)"}
            if passed: score += 1
            assessed += 1
        else:
            checklist['10_pb_value'] = {'pass': None, 'detail': "Data N/A"}

        if assessed > 0:
            normalized_score = round(score / assessed * 10, 1)
        else:
            normalized_score = 0

        gate_pass = (assessed >= 5 and score / assessed >= 0.7) or score >= 7

        return {
            'checklist': checklist,
            'score': score,
            'assessed': assessed,
            'total': 10,
            'normalized': normalized_score,
            'pass_rate': round(score / max(assessed, 1) * 100, 1),
            'gate_pass': gate_pass,
        }

    # ------------------------------------------------------------------
    # GATE 2: VALUATION FILTER
    # ------------------------------------------------------------------

    def assess_valuation(self, fund: Dict, sector_type: str) -> Dict:
        """Gate 2: Valuation assessment using PEG, P/B, earnings yield."""
        pe = fund.get('pe')
        pb = fund.get('pb')
        roe = fund.get('roe')
        pat_cagr = fund.get('pat_cagr_3y')
        rev_cagr = fund.get('rev_cagr_3y')
        dy = fund.get('dividend_yield') or 0
        ev_ebitda = fund.get('ev_ebitda')
        forward_pe = fund.get('forward_pe')

        details = []
        scores = []  # +1 for cheap signals, -1 for expensive signals

        # PEG Ratio
        peg = None
        growth = pat_cagr or (fund.get('earnings_growth_qoq') or 0) * 100
        if pe and growth and growth > 0:
            peg = round(pe / growth, 2)
            if peg < 0.5:
                details.append(f"PEG: {peg} (Very Cheap)")
                scores.append(2)
            elif peg < 1:
                details.append(f"PEG: {peg} (Cheap)")
                scores.append(1)
            elif peg <= 2:
                details.append(f"PEG: {peg} (Fair)")
                scores.append(0)
            elif peg <= 5:
                details.append(f"PEG: {peg} (Expensive)")
                scores.append(-1)
            else:
                details.append(f"PEG: {peg} (Extreme)")
                scores.append(-2)

        # P/E Assessment
        if pe is not None:
            if sector_type == 'banking':
                thresholds = (10, 15, 25)
            else:
                thresholds = (15, 25, 40)

            if pe < thresholds[0]:
                details.append(f"P/E: {pe:.1f} (Cheap)")
                scores.append(1)
            elif pe < thresholds[1]:
                details.append(f"P/E: {pe:.1f} (Fair)")
                scores.append(0)
            elif pe < thresholds[2]:
                details.append(f"P/E: {pe:.1f} (Expensive)")
                scores.append(-1)
            else:
                details.append(f"P/E: {pe:.1f} (Very Expensive)")
                scores.append(-2)

        # P/B vs ROE
        if pb is not None and roe is not None:
            if sector_type in ('banking', 'nbfc'):
                if pb < 1.5 and roe > 15:
                    details.append(f"P/B: {pb:.2f} with ROE {roe:.0f}% (Value)")
                    scores.append(2)
                elif pb < 2.5 and roe > 12:
                    details.append(f"P/B: {pb:.2f} with ROE {roe:.0f}% (Fair)")
                    scores.append(0)
                else:
                    details.append(f"P/B: {pb:.2f} with ROE {roe:.0f}% (Expensive)")
                    scores.append(-1)
            else:
                if pb < 3 and roe > 15:
                    details.append(f"P/B: {pb:.2f} with ROE {roe:.0f}% (Reasonable)")
                    scores.append(1)
                elif pb < 6 and roe > 20:
                    details.append(f"P/B: {pb:.2f} with ROE {roe:.0f}% (Fair for high-ROE)")
                    scores.append(0)
                elif pb < 8:
                    details.append(f"P/B: {pb:.2f} (Expensive)")
                    scores.append(-1)
                else:
                    details.append(f"P/B: {pb:.2f} (Very Expensive)")
                    scores.append(-2)
        elif pb is not None:
            details.append(f"P/B: {pb:.2f}")

        # Earnings Yield vs Bond Yield (~7% for India, ~4.5% for US)
        if pe and pe > 0:
            ey = round(100 / pe, 2)
            bond_yield = 7  # Approximate
            if ey > bond_yield * 1.5:
                details.append(f"Earnings Yield: {ey:.1f}% >> Bond {bond_yield}% (Attractive)")
                scores.append(1)
            elif ey > bond_yield:
                details.append(f"Earnings Yield: {ey:.1f}% > Bond {bond_yield}% (OK)")
                scores.append(0)
            else:
                details.append(f"Earnings Yield: {ey:.1f}% < Bond {bond_yield}% (Unattractive)")
                scores.append(-1)

        # Dividend Yield bonus
        if dy and dy > 3:
            details.append(f"Div Yield: {dy:.2f}% (Strong income)")
            scores.append(1)
        elif dy and dy > 1.5:
            details.append(f"Div Yield: {dy:.2f}%")

        # EV/EBITDA
        if ev_ebitda is not None:
            if ev_ebitda < 10:
                details.append(f"EV/EBITDA: {ev_ebitda:.1f} (Cheap)")
                scores.append(1)
            elif ev_ebitda < 20:
                details.append(f"EV/EBITDA: {ev_ebitda:.1f} (Fair)")
                scores.append(0)
            else:
                details.append(f"EV/EBITDA: {ev_ebitda:.1f} (Expensive)")
                scores.append(-1)

        # Determine verdict
        if not scores:
            return {
                'verdict': 'N/A',
                'details': ['Insufficient valuation data'],
                'score_sum': 0,
                'gate_pass': None,
                'peg': peg,
            }

        total = sum(scores)
        if total >= 3:
            val_verdict = 'CHEAP'
            gate_pass = True
        elif total >= 0:
            val_verdict = 'FAIR'
            gate_pass = True
        elif total >= -2:
            val_verdict = 'RICH'
            gate_pass = False
        else:
            val_verdict = 'EXTREME'
            gate_pass = False

        return {
            'verdict': val_verdict,
            'details': details,
            'score_sum': total,
            'gate_pass': gate_pass,
            'peg': peg,
        }

    # ------------------------------------------------------------------
    # RED FLAGS CHECK
    # ------------------------------------------------------------------

    def check_red_flags(self, fund: Dict, sector_type: str = 'general') -> Dict:
        """Check for instant disqualifiers."""
        flags = []

        # Negative OCF (skip for banking/NBFC where negative OCF = loan growth)
        ocf = fund.get('ocf')
        if ocf is not None and ocf < 0 and sector_type not in ('banking', 'nbfc'):
            flags.append(f"Negative Operating Cash Flow: {ocf / 1e7:,.0f} Cr")

        # Debt > 3x (skip for banking/NBFC where high leverage is the business model)
        de = fund.get('de_ratio')
        if de is not None and de > 3 and sector_type not in ('banking', 'nbfc'):
            flags.append(f"Extreme Debt/Equity: {de:.2f} (>3x)")

        # Negative ROE
        roe = fund.get('roe')
        if roe is not None and roe < 0:
            flags.append(f"Negative ROE: {roe:.1f}%")

        # Very low promoter holding (skip if widely-held: FII+DII > 70%)
        promoter = fund.get('promoter_holding') or fund.get('insider_pct')
        fii = fund.get('fii_holding', 0) or 0
        dii = fund.get('dii_holding', 0) or 0
        institutional = fii + dii
        if promoter is not None and promoter < 10 and institutional < 70:
            label = "promoter" if fund.get('promoter_holding') is not None else "insider"
            flags.append(f"Very low {label} holding: {promoter:.1f}%")

        has_critical = any('Extreme Debt' in f or 'Negative ROE' in f for f in flags)

        return {
            'flags': flags,
            'count': len(flags),
            'critical': has_critical,
        }

    # ------------------------------------------------------------------
    # TECHNICAL ANALYSIS METHODS (existing, unchanged)
    # ------------------------------------------------------------------

    def calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> float:
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi.iloc[-1], 2)

    def calculate_macd(self, data: pd.DataFrame) -> Dict:
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        return {
            'macd': round(macd.iloc[-1], 2),
            'signal': round(signal.iloc[-1], 2),
            'histogram': round(histogram.iloc[-1], 2),
            'bullish': macd.iloc[-1] > signal.iloc[-1],
        }

    def calculate_mfi(self, data: pd.DataFrame, period: int = 14) -> float:
        typical_price = (data['High'] + data['Low'] + data['Close']) / 3
        money_flow = typical_price * data['Volume']
        delta = typical_price.diff()
        positive_flow = money_flow.where(delta > 0, 0).rolling(window=period).sum()
        negative_flow = money_flow.where(delta < 0, 0).rolling(window=period).sum()
        mfi = 100 - (100 / (1 + positive_flow / negative_flow))
        return round(mfi.iloc[-1], 2)

    def calculate_moving_averages(self, data: pd.DataFrame) -> Dict:
        current_price = data['Close'].iloc[-1]
        ma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
        ma_200 = data['Close'].rolling(window=200).mean().iloc[-1] if len(data) >= 200 else None
        ma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
        return {
            'current_price': round(current_price, 2),
            'ma_20': round(ma_20, 2),
            'ma_50': round(ma_50, 2) if not pd.isna(ma_50) else None,
            'ma_200': round(ma_200, 2) if ma_200 and not pd.isna(ma_200) else None,
            'above_50_dma': current_price > ma_50 if not pd.isna(ma_50) else None,
            'above_200_dma': current_price > ma_200 if ma_200 and not pd.isna(ma_200) else None,
        }

    def find_support_resistance(self, data: pd.DataFrame) -> Dict:
        high_52w = data['High'].max()
        low_52w = data['Low'].min()
        current = data['Close'].iloc[-1]
        recent = data.tail(20)
        pivot = (recent['High'].max() + recent['Low'].min() + recent['Close'].iloc[-1]) / 3
        r1 = 2 * pivot - recent['Low'].min()
        s1 = 2 * pivot - recent['High'].max()
        r2 = pivot + (recent['High'].max() - recent['Low'].min())
        s2 = pivot - (recent['High'].max() - recent['Low'].min())
        return {
            '52w_high': round(high_52w, 2),
            '52w_low': round(low_52w, 2),
            'immediate_support': round(s1, 2),
            'immediate_resistance': round(r1, 2),
            'strong_support': round(s2, 2),
            'strong_resistance': round(r2, 2),
            'distance_from_high': round((high_52w - current) / current * 100, 2),
            'distance_from_low': round((current - low_52w) / low_52w * 100, 2),
        }

    def analyze_volume(self, data: pd.DataFrame) -> Dict:
        current_volume = data['Volume'].iloc[-1]
        avg_volume_10 = data['Volume'].tail(10).mean()
        avg_volume_20 = data['Volume'].tail(20).mean()
        return {
            'current_volume': int(current_volume),
            'avg_10_day': int(avg_volume_10),
            'avg_20_day': int(avg_volume_20),
            'volume_ratio': round(current_volume / avg_volume_10, 2) if avg_volume_10 > 0 else 0,
            'above_average': current_volume >= avg_volume_10,
        }

    def detect_candlestick_pattern(self, data: pd.DataFrame) -> Dict:
        recent = data.tail(5)
        patterns = []
        for i in range(-3, 0):
            candle = recent.iloc[i]
            body = abs(candle['Close'] - candle['Open'])
            upper_shadow = candle['High'] - max(candle['Close'], candle['Open'])
            lower_shadow = min(candle['Close'], candle['Open']) - candle['Low']
            total_range = candle['High'] - candle['Low']
            if total_range == 0:
                continue
            if body / total_range < 0.1:
                patterns.append('Doji')
            elif lower_shadow > 2 * body and upper_shadow < body * 0.5:
                if candle['Close'] > candle['Open']:
                    patterns.append('Hammer (Bullish)')
                else:
                    patterns.append('Inverted Hammer')
            elif body / total_range > 0.9:
                if candle['Close'] > candle['Open']:
                    patterns.append('Bullish Marubozu')
                else:
                    patterns.append('Bearish Marubozu')

        if len(recent) >= 2:
            prev, curr = recent.iloc[-2], recent.iloc[-1]
            if (prev['Close'] < prev['Open'] and curr['Close'] > curr['Open'] and
                    curr['Open'] < prev['Close'] and curr['Close'] > prev['Open']):
                patterns.append('Bullish Engulfing')
            if (prev['Close'] > prev['Open'] and curr['Close'] < curr['Open'] and
                    curr['Open'] > prev['Close'] and curr['Close'] < prev['Open']):
                patterns.append('Bearish Engulfing')

        if len(data) >= 20:
            prior_trend = 'Uptrend' if data['Close'].iloc[-1] > data['Close'].iloc[-20] else 'Downtrend'
        else:
            prior_trend = 'Unknown'

        return {
            'patterns': list(set(patterns)) if patterns else ['No clear pattern'],
            'prior_trend': prior_trend,
            'last_candle': 'Green' if recent.iloc[-1]['Close'] > recent.iloc[-1]['Open'] else 'Red',
        }

    def calculate_rrr(self, current: float, support: float, resistance: float) -> Dict:
        risk = current - support
        reward = resistance - current
        if risk <= 0:
            return {'rrr': 0, 'risk_pct': 0, 'reward_pct': 0, 'valid': False}
        rrr = reward / risk
        return {
            'rrr': round(rrr, 2),
            'risk_pct': round((risk / current) * 100, 2),
            'reward_pct': round((reward / current) * 100, 2),
            'valid': rrr >= 1.5,
        }

    # ------------------------------------------------------------------
    # GATE 3: TECHNICAL CHECKLIST (7-Point)
    # ------------------------------------------------------------------

    def apply_checklist(self, analysis: Dict) -> Dict:
        """Gate 3: Zerodha 7-Point Technical Checklist."""
        checklist = {}
        score = 0

        # 1. Candlestick Pattern
        patterns = analysis['candlestick']['patterns']
        has_pattern = patterns[0] != 'No clear pattern'
        checklist['1_candlestick'] = {'pass': has_pattern, 'detail': ', '.join(patterns)}
        if has_pattern: score += 1

        # 2. Prior Trend (only meaningful if a pattern was detected)
        prior_trend = analysis['candlestick']['prior_trend']
        if not has_pattern:
            # No pattern → trend alignment is meaningless
            trend_valid = False
            trend_detail = "No pattern to validate"
        else:
            bullish_p = ['Hammer', 'Bullish Engulfing', 'Bullish Marubozu',
                         'Morning Star', 'Inverted Hammer']
            bearish_p = ['Bearish Engulfing', 'Bearish Marubozu', 'Evening Star']
            trend_valid = True  # Default for neutral patterns (Doji)
            if any(p in str(patterns) for p in bullish_p):
                trend_valid = prior_trend == 'Downtrend'
            elif any(p in str(patterns) for p in bearish_p):
                trend_valid = prior_trend == 'Uptrend'
            trend_detail = f"Prior trend: {prior_trend}"
        checklist['2_prior_trend'] = {'pass': trend_valid, 'detail': trend_detail}
        if trend_valid: score += 1

        # 3. S&R within 4%
        sr = analysis['support_resistance']
        current = analysis['moving_averages']['current_price']
        support_dist = abs(current - sr['immediate_support']) / current * 100
        sr_valid = support_dist <= 4
        checklist['3_sr_alignment'] = {'pass': sr_valid, 'detail': f"Support {support_dist:.1f}% away (need <=4%)"}
        if sr_valid: score += 1

        # 4. Volume
        vol_valid = analysis['volume']['above_average']
        checklist['4_volume'] = {'pass': vol_valid, 'detail': f"Volume ratio: {analysis['volume']['volume_ratio']}x"}
        if vol_valid: score += 1

        # 5. RRR
        rrr = analysis['rrr']
        checklist['5_rrr'] = {'pass': rrr['valid'], 'detail': f"RRR: {rrr['rrr']}:1 (need >=1.5:1)"}
        if rrr['valid']: score += 1

        # 6. Indicator Confirmation (MACD must confirm direction + RSI not overbought)
        rsi = analysis['rsi']
        macd = analysis['macd']
        macd_ok = macd['bullish']
        rsi_not_overbought = rsi < 70
        indicators_ok = macd_ok and rsi_not_overbought
        rsi_status = "Oversold" if rsi < 30 else "Overbought" if rsi > 70 else "Neutral"
        checklist['6_indicators'] = {
            'pass': indicators_ok,
            'detail': f"RSI: {rsi} ({rsi_status}), MACD: {'Bullish' if macd_ok else 'Bearish'}",
        }
        if indicators_ok: score += 1

        # 7. Dow Theory
        ma = analysis['moving_averages']
        dow_valid = ma['above_50_dma'] and (ma['above_200_dma'] if ma['above_200_dma'] is not None else True)
        checklist['7_dow_theory'] = {
            'pass': dow_valid,
            'detail': f"Above 50-DMA: {ma['above_50_dma']}, Above 200-DMA: {ma['above_200_dma']}",
        }
        if dow_valid: score += 1

        gate_pass = score >= 5

        return {
            'checklist': checklist,
            'score': score,
            'total': 7,
            'pass_rate': round(score / 7 * 100, 1),
            'gate_pass': gate_pass,
        }

    # ------------------------------------------------------------------
    # COMBINED VERDICT (ALL 3 GATES)
    # ------------------------------------------------------------------

    def generate_verdict(self, fund_result: Dict, val_result: Dict, tech_result: Dict,
                         red_flags: Dict, analysis: Dict) -> Dict:
        """Generate final verdict using all 3 gates."""
        current = analysis['moving_averages']['current_price']
        sr = analysis['support_resistance']
        rsi = analysis['rsi']
        rrr = analysis['rrr']

        g1 = fund_result.get('gate_pass')
        g2 = val_result.get('gate_pass')
        g3 = tech_result.get('gate_pass')
        has_red = red_flags.get('critical', False)

        fund_score = fund_result.get('score', 0)
        fund_norm = fund_result.get('normalized', 0)
        tech_score = tech_result.get('score', 0)
        val_verdict = val_result.get('verdict', 'N/A')

        # Red flag override
        if has_red:
            verdict = "AVOID"
            confidence = "HIGH"
            action = f"Critical red flags: {'; '.join(red_flags['flags'][:2])}"
            position_pct = 0

        # All 3 gates pass
        elif g1 and g2 and g3:
            if fund_norm >= 8 and tech_score >= 6 and val_verdict in ('CHEAP', 'FAIR'):
                verdict = "BUY"
                confidence = "HIGH"
                action = f"Strong setup. Enter at {current:.2f}, SL at {sr['immediate_support']:.2f}"
                position_pct = 8
            else:
                verdict = "BUY"
                confidence = "MEDIUM"
                action = f"Enter on dip to {sr['immediate_support']:.2f}"
                position_pct = 5

        # Fund + Val pass, Tech borderline
        elif g1 and g2 and not g3:
            if tech_score >= 4:
                verdict = "ACCUMULATE"
                confidence = "MEDIUM"
                action = f"Fundamentally strong. Accumulate on dips near {sr['immediate_support']:.2f}"
                position_pct = 4
            else:
                verdict = "WAIT"
                confidence = "LOW"
                action = "Good business but poor timing. Wait for technical setup."
                position_pct = 0

        # Fund pass, Val fail (overvalued quality)
        elif g1 and not g2:
            verdict = "WAIT"
            confidence = "MEDIUM"
            action = f"Quality stock but {val_verdict} valuation. Wait for correction."
            position_pct = 0

        # Val pass, Fund fail (cheap but weak quality)
        elif g2 and not g1:
            if tech_score >= 5:
                verdict = "WAIT"
                confidence = "LOW"
                action = "Cheap valuation but weak fundamentals. Needs more research."
                position_pct = 0
            else:
                verdict = "AVOID"
                confidence = "MEDIUM"
                action = f"Weak fundamentals ({fund_score}/{fund_result['assessed']} criteria). Cheap for a reason."
                position_pct = 0

        # Only Tech passes
        elif g3 and not g1 and not g2:
            verdict = "SKIP"
            confidence = "HIGH"
            action = "Only technical signals, no fundamental/valuation support."
            position_pct = 0

        else:
            verdict = "AVOID"
            confidence = "HIGH"
            failed_gates = []
            if not g1: failed_gates.append("Quality")
            if not g2: failed_gates.append("Valuation")
            if not g3: failed_gates.append("Timing")
            action = f"Failed gates: {', '.join(failed_gates)}"
            position_pct = 0

        # Trade setup
        trade_setup = None
        if verdict in ("BUY", "ACCUMULATE"):
            entry = current if verdict == "BUY" and confidence == "HIGH" else sr['immediate_support']
            trade_setup = {
                'entry': entry,
                'stoploss': sr['strong_support'],
                'target_1': sr['immediate_resistance'],
                'target_2': sr['strong_resistance'],
                'target_3': sr['52w_high'],
                'position_pct': position_pct,
            }

        return {
            'verdict': verdict,
            'confidence': confidence,
            'action': action,
            'trade_setup': trade_setup,
            'gates': {
                'fundamental': 'PASS' if g1 else ('N/A' if g1 is None else 'FAIL'),
                'valuation': val_verdict,
                'technical': 'PASS' if g3 else 'FAIL',
            },
            'position_pct': position_pct,
        }

    # ------------------------------------------------------------------
    # MAIN ANALYSIS (3-GATE)
    # ------------------------------------------------------------------

    def analyze_stock(self, symbol: str) -> Optional[Dict]:
        """Complete 3-Gate stock analysis."""
        print(f"\nAnalyzing {symbol}...")

        # Resolve ticker and fetch price data
        ticker, data, resolved = self._resolve_ticker(symbol)
        if ticker is None or data is None:
            print(f"  Insufficient data for {symbol}")
            return None

        # Fetch fundamentals (yfinance + Screener.in for Indian stocks)
        print(f"  Fetching fundamentals for {resolved}...")
        fundamentals = self.get_fundamentals(ticker, symbol=resolved)
        sector_type = self.detect_sector_type(fundamentals)

        # Technical indicators
        technical = {
            'symbol': resolved,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'rsi': self.calculate_rsi(data),
            'macd': self.calculate_macd(data),
            'mfi': self.calculate_mfi(data),
            'moving_averages': self.calculate_moving_averages(data),
            'support_resistance': self.find_support_resistance(data),
            'volume': self.analyze_volume(data),
            'candlestick': self.detect_candlestick_pattern(data),
        }

        current = technical['moving_averages']['current_price']
        support = technical['support_resistance']['immediate_support']
        resistance = technical['support_resistance']['immediate_resistance']
        technical['rrr'] = self.calculate_rrr(current, support, resistance)

        # GATE 1: Fundamental Checklist
        fund_result = self.apply_fundamental_checklist(fundamentals, sector_type)

        # GATE 2: Valuation
        val_result = self.assess_valuation(fundamentals, sector_type)

        # Red Flags (sector-aware)
        red_flags = self.check_red_flags(fundamentals, sector_type)

        # GATE 3: Technical Checklist
        tech_result = self.apply_checklist(technical)

        # Combined Verdict
        verdict = self.generate_verdict(fund_result, val_result, tech_result, red_flags, technical)

        # Build backward-compatible result
        analysis = {
            'symbol': resolved,
            'date': technical['date'],
            'sector_type': sector_type,
            'fundamentals': fundamentals,
            'fund_result': fund_result,
            'val_result': val_result,
            'red_flags': red_flags,
            # Technical fields (backward compat)
            'rsi': technical['rsi'],
            'macd': technical['macd'],
            'mfi': technical['mfi'],
            'moving_averages': technical['moving_averages'],
            'support_resistance': technical['support_resistance'],
            'volume': technical['volume'],
            'candlestick': technical['candlestick'],
            'rrr': technical['rrr'],
            'checklist_result': tech_result,
            'verdict': verdict,
        }

        return analysis

    # ------------------------------------------------------------------
    # REPORT FORMATTING
    # ------------------------------------------------------------------

    def format_report(self, analysis: Dict) -> str:
        """Format 3-Gate analysis into readable report."""
        if analysis is None:
            return "Analysis failed - insufficient data"

        ma = analysis['moving_averages']
        sr = analysis['support_resistance']
        vol = analysis['volume']
        verdict = analysis['verdict']
        fund = analysis['fundamentals']
        fr = analysis['fund_result']
        vr = analysis['val_result']
        rf = analysis['red_flags']
        cl = analysis['checklist_result']

        mcap = fund.get('market_cap')
        mcap_str = f"{mcap / 1e9:,.1f}B" if mcap and mcap > 1e9 else (f"{mcap / 1e7:,.0f} Cr" if mcap else "N/A")

        src = fund.get('data_source', 'yfinance')
        report = f"""
{'='*70}
 {analysis['symbol']} - 3-GATE ANALYSIS
 {analysis['date']} | Sector: {fund.get('industry', 'Unknown')} ({analysis['sector_type'].upper()})
 Market Cap: {mcap_str} | Data: {src}
{'='*70}

GATE 1: FUNDAMENTAL QUALITY ({fr['score']}/{fr['assessed']} assessed = {fr['pass_rate']:.0f}%)
{'  >> PASS' if fr['gate_pass'] else '  >> FAIL' if fr['gate_pass'] is not None else '  >> N/A'}
{'-'*50}"""

        for key, item in fr['checklist'].items():
            if item['pass'] is None:
                status = " N/A"
            elif item['pass']:
                status = "PASS"
            else:
                status = "FAIL"
            report += f"\n  [{status}] {key}: {item['detail']}"

        report += f"""

GATE 2: VALUATION ({vr['verdict']})
{'  >> PASS' if vr['gate_pass'] else '  >> FAIL' if vr['gate_pass'] is not None else '  >> N/A'}
{'-'*50}"""

        for d in vr['details']:
            report += f"\n  {d}"

        pe_str = f"{fund['pe']:.1f}" if fund.get('pe') else "N/A"
        pb_str = f"{fund['pb']:.2f}" if fund.get('pb') else "N/A"
        roe_str = f"{fund['roe']:.1f}%" if fund.get('roe') else "N/A"
        roce_str = f"{fund['roce']:.1f}%" if fund.get('roce') else "N/A"
        dy_str = f"{fund['dividend_yield']:.2f}%" if fund.get('dividend_yield') else "N/A"
        promo_str = f"{fund['promoter_holding']:.1f}%" if fund.get('promoter_holding') is not None else "N/A"
        report += f"\n  Key: P/E={pe_str} | P/B={pb_str} | ROE={roe_str} | ROCE={roce_str} | DivYld={dy_str} | Promoter={promo_str}"

        if rf['flags']:
            report += f"""

RED FLAGS ({rf['count']} found) {'** CRITICAL **' if rf['critical'] else ''}
{'-'*50}"""
            for f in rf['flags']:
                report += f"\n  !! {f}"
        else:
            report += f"\n\n  RED FLAGS: None"

        report += f"""

GATE 3: TECHNICAL ({cl['score']}/{cl['total']} = {cl['pass_rate']}%)
{'  >> PASS' if cl['gate_pass'] else '  >> FAIL'}
{'-'*50}
  Price: {ma['current_price']} | 52W: {sr['52w_low']}-{sr['52w_high']}
  50-DMA: {ma['ma_50']} {'(Above)' if ma['above_50_dma'] else '(Below)'} | 200-DMA: {ma['ma_200']} {'(Above)' if ma['above_200_dma'] else '(Below)' if ma['above_200_dma'] is not None else 'N/A'}
  RSI: {analysis['rsi']} | MACD: {'Bullish' if analysis['macd']['bullish'] else 'Bearish'} | Vol: {vol['volume_ratio']}x
  Pattern: {', '.join(analysis['candlestick']['patterns'])} | Trend: {analysis['candlestick']['prior_trend']}
  S&R: {sr['strong_support']} / {sr['immediate_support']} <<< {ma['current_price']} >>> {sr['immediate_resistance']} / {sr['strong_resistance']}
  RRR: {analysis['rrr']['rrr']}:1 {'(Valid)' if analysis['rrr']['valid'] else '(Too Low)'}"""

        for key, item in cl['checklist'].items():
            status = "PASS" if item['pass'] else "FAIL"
            report += f"\n  [{status}] {key}: {item['detail']}"

        g = verdict['gates']
        report += f"""

{'='*70}
 VERDICT: {verdict['verdict']} (Confidence: {verdict['confidence']})
 Gates: Fundamental={g['fundamental']} | Valuation={g['valuation']} | Technical={g['technical']}
{'='*70}
 Action: {verdict['action']}"""

        if verdict.get('position_pct', 0) > 0:
            report += f"\n Position: {verdict['position_pct']}% of portfolio"

        if verdict['trade_setup']:
            ts = verdict['trade_setup']
            report += f"""

 TRADE SETUP
 Entry:    {ts['entry']:.2f}
 Stoploss: {ts['stoploss']:.2f}
 Target 1: {ts['target_1']:.2f} (book 40%)
 Target 2: {ts['target_2']:.2f} (book 40%)
 Target 3: {ts['target_3']:.2f} (trail SL)"""

        report += "\n" + "=" * 70 + "\n"
        return report

    # ------------------------------------------------------------------
    # BATCH ANALYSIS
    # ------------------------------------------------------------------

    def run_analysis(self, stocks: List[str]) -> str:
        """Run 3-Gate analysis on multiple stocks."""
        all_reports = []
        summary = []

        print(f"\nStarting 3-Gate analysis of {len(stocks)} stocks...")
        print("-" * 40)

        for symbol in stocks:
            analysis = self.analyze_stock(symbol.strip())
            if analysis:
                report = self.format_report(analysis)
                all_reports.append(report)

                fund = analysis['fundamentals']
                fr = analysis['fund_result']
                vr = analysis['val_result']
                v = analysis['verdict']

                summary.append({
                    'symbol': analysis['symbol'],
                    'price': analysis['moving_averages']['current_price'],
                    'rsi': analysis['rsi'],
                    'pe': fund.get('pe'),
                    'roe': fund.get('roe'),
                    'fund_score': f"{fr['score']}/{fr['assessed']}",
                    'valuation': vr['verdict'],
                    'tech_score': f"{analysis['checklist_result']['score']}/7",
                    'verdict': v['verdict'],
                    'confidence': v['confidence'],
                    'score': f"{analysis['checklist_result']['score']}/7",
                })

        # Summary header
        header = f"""
{'#'*80}
 3-GATE DAILY STOCK ANALYSIS | {datetime.now().strftime("%Y-%m-%d %H:%M")}
 Framework: Dalal Street Integrated + Zerodha Technical Analysis
 Profile: Positional (1-6 months) | Moderate Risk (8-10% max/position)
{'#'*80}

{'Symbol':<14} {'Price':<9} {'P/E':<7} {'ROE':<7} {'Fund':<7} {'Value':<8} {'Tech':<6} {'Verdict':<12} {'Conf':<8}
{'-'*80}
"""
        for s in summary:
            pe_str = f"{s['pe']:.1f}" if s['pe'] else "N/A"
            roe_str = f"{s['roe']:.0f}%" if s['roe'] else "N/A"
            header += (f"{s['symbol']:<14} {s['price']:<9} {pe_str:<7} {roe_str:<7} "
                       f"{s['fund_score']:<7} {s['valuation']:<8} {s['tech_score']:<6} "
                       f"{s['verdict']:<12} {s['confidence']:<8}\n")

        header += f"\n{'#'*80}\n"

        # Group by verdict
        for verdict_type, label in [("BUY", "BUY RECOMMENDATIONS"),
                                     ("ACCUMULATE", "ACCUMULATE (add on dips)"),
                                     ("WAIT", "WATCHLIST (WAIT)"),
                                     ("AVOID", "AVOID"),
                                     ("SKIP", "SKIP")]:
            group = [s for s in summary if s['verdict'] == verdict_type]
            if group:
                header += f"\n{label}:\n"
                for s in group:
                    header += f"  - {s['symbol']} @ {s['price']} (Fund: {s['fund_score']}, Val: {s['valuation']}, Tech: {s['tech_score']})\n"

        full_report = header + "\n\nDETAILED ANALYSIS\n" + "=" * 80 + "\n".join(all_reports)

        # Save
        filename = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        filepath = os.path.join(self.results_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_report)

        print(f"\nReport saved to: {filepath}")
        return full_report


def main():
    """Main function - interactive mode"""
    analyzer = ZerodhaAnalyzer()

    print("\n" + "=" * 60)
    print(" 3-GATE STOCK ANALYSIS")
    print(" Fundamental + Valuation + Technical")
    print("=" * 60)
    print("\nSupports: NSE, BSE, NASDAQ, NYSE")
    print("Examples: RELIANCE, TCS.NS, INFY.BO, AAPL, MSFT")
    print("-" * 60)

    print("\nEnter stocks to analyze (comma-separated):")
    user_input = input("\n> ").strip()

    if not user_input:
        print("No stocks entered. Exiting.")
        return

    stocks = [s.strip().upper() for s in user_input.split(',') if s.strip()]
    if not stocks:
        print("No valid stocks found. Exiting.")
        return

    report = analyzer.run_analysis(stocks)
    print("\n" + report)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
