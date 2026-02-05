# Claude Code Instructions

## Stock Analysis Frameworks

When the user asks to analyze any stock, use BOTH frameworks:

### Framework Files

| Framework | File | Purpose |
|-----------|------|---------|
| **Integrated Framework** | `dalal-street-integrated-framework.md` | Fundamental analysis, valuation, sector templates |
| **Technical Framework** | `C:\Users\rohitkundu\zerodha-technical-analysis-framework.md` | 7-point TA checklist, patterns, entry timing |

---

## Analysis Process

### Step 1: Fetch Data

**Fundamental Data (via Screener.in, Trendlyne):**
- Market cap, sector classification
- ROE, ROCE, ROA
- Debt/Equity, Interest Coverage
- Revenue & PAT growth (3Y CAGR)
- Promoter holding & pledge %
- Operating & Free Cash Flow
- P/E, P/B, EV/EBITDA vs peers

**Technical Data (via Zerodha Kite MCP):**
- Current price, 52W high/low
- 50-DMA and 200-DMA
- RSI (14-day), MACD
- Volume vs 10-day average
- Support/Resistance levels
- Recent candlestick patterns

---

### Step 2: Apply the 3-Gate System

**GATE 1: Quality Filter (Fundamental)**
Apply the 10-Point Investment Checklist:
- [ ] GPM > 20%
- [ ] ROE > 15%
- [ ] ROCE > 15%
- [ ] Debt/Equity < 1
- [ ] Interest Coverage > 3x
- [ ] Operating Cash Flow positive
- [ ] Revenue Growth > 10% CAGR
- [ ] PAT Growth > 12% CAGR
- [ ] Promoter Holding > 50%, no pledge
- [ ] Free Cash Flow positive

**Minimum 7/10 to proceed.**

**GATE 2: Valuation Filter**
- Calculate intrinsic value (DCF or relative)
- Compare to current market price
- Assess margin of safety (25-50%)
- Check if valuation is reasonable vs peers

**GATE 3: Timing Filter (Technical)**
Apply the 7-Point Zerodha Checklist:
- [ ] Recognizable candlestick pattern
- [ ] Prior trend supports the pattern
- [ ] S&R within 4% of stoploss
- [ ] Volume ≥ 10-day average
- [ ] RRR ≥ 1.5
- [ ] RSI/MACD confirmation
- [ ] Dow Theory alignment

**Minimum 5/7 to proceed with entry.**

---

### Step 3: Check Red Flags

Instant disqualifiers (walk away):
- Promoter pledge > 20%
- Related party transactions > 5% of revenue
- Auditor resignation/change
- Negative operating cash flow (2+ years)
- Debt > 3x EBITDA
- SEBI/ED investigation

---

### Step 4: Determine Position Sizing

Based on conviction level (Moderate Risk Profile: 8-10% max):

| Conviction | Fundamental | Technical | Position Size |
|------------|-------------|-----------|---------------|
| HIGH | 8-10/10 | 6-7/7 | 8-10% |
| MEDIUM | 6-7/10 | 4-5/7 | 4-6% |
| LOW | 5-6/10 | 4+/7 | 2-3% |

---

### Step 5: Provide Trade Setup

If checklist passes, provide:
- Entry price/zone
- Stoploss level (based on S&R)
- Target 1 (book 40%), Target 2 (book 40%), Target 3 (trail)
- Risk-Reward Ratio
- Position sizing guidance
- GTT order setup instructions

---

### Step 6: Give Clear Verdict

- **BUY** (with specific conditions and entry zone)
- **ACCUMULATE** (add on dips to support)
- **HOLD** (for existing positions)
- **WAIT** (what to watch for before entry)
- **AVOID** (which criteria failed)

---

## Sector-Specific Analysis

For specific sectors, apply additional metrics from the integrated framework:

### Banking & Financials
Key metrics: NIM > 3%, GNPA < 3%, NNPA < 1.5%, CASA > 40%, ROA > 1%
Valuation: Use P/B ratio as primary metric

### IT & Technology
Key metrics: Attrition < 20%, Digital Revenue % growing, Operating Margin > 20%
Watch: Deal wins, utilization rates, offshore mix

### 2026 Booming Sectors
- **Defence**: Order book > 3x sales, indigenization %
- **Renewables**: Capacity additions, PPA visibility
- **EMS**: Customer wins, PLI benefits
- **Railways**: Order book/sales ratio, execution rate
- **Data Centers**: MW capacity, utilization
- **Specialty Chemicals**: EBITDA margins, China+1 status

---

## Output Format

Structure ALL stock analyses as:

```
1. EXECUTIVE SUMMARY (1-line verdict with conviction level)

2. BUSINESS OVERVIEW & MOAT
   - What the company does
   - Moat assessment (Strong/Moderate/Weak)

3. FUNDAMENTAL SCORECARD
   - 10-point checklist with actual values
   - Score: X/10
   - Valuation metrics vs peers
   - DCF intrinsic value (if applicable)

4. TECHNICAL ANALYSIS
   - Price data table
   - 7-point checklist with actual values
   - Score: X/7
   - Support/Resistance map

5. RISK ASSESSMENT
   - Red flags check
   - Key risks (3 points)
   - Catalysts (positive & negative)

6. TRADE RECOMMENDATION
   - Entry zone
   - Stoploss
   - Targets (T1, T2, T3)
   - RRR
   - Position sizing (for ₹10L portfolio)

7. ACTION PLAN
   - Specific next steps based on verdict
```

---

## Key Principles

- "Capital preservation first, then returns"
- "Buy strength, sell weakness"
- "Prior trend must exist for pattern validity"
- "S&R must be within 4% of stoploss"
- "Volume must confirm the move"
- "Minimum RRR of 1.5:1"
- "Deciding not to trade is itself a trading decision"
- "Character > Numbers" (Management quality matters)
- "Never analyze a stock in isolation" (Check sector context)

---

## Data Sources

**Fundamental:**
- Screener.in: Financial statements, ratios
- Trendlyne: Shareholding, scores
- BSE/NSE: Official filings

**Technical:**
- Zerodha Kite MCP: Real-time prices, historical data
- TradingView: Charts, patterns
- Trendlyne: Technical indicators

---

*User Profile: Positional (1-6 months) | Moderate Risk (8-10% max/position)*
