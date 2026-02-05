# Dalal Street Integrated Analysis Framework
## Investment Banker's Approach to Technical + Fundamental Analysis

---

## EXECUTIVE PHILOSOPHY

> "The stock market is a device for transferring money from the impatient to the patient." — Warren Buffett

### The Investment Banker's Mindset

1. **Capital Preservation First**: Never lose more than you can afford
2. **Asymmetric Risk-Reward**: Only take bets where upside >> downside
3. **Conviction-Based Sizing**: Bet big on high-conviction ideas, small on speculative ones
4. **Know When to Walk Away**: The best trade is often no trade

### When to Be Aggressive vs Defensive

| Market Condition | Stance | Position Size | Stock Selection |
|------------------|--------|---------------|-----------------|
| Panic/Crash (VIX > 25) | **Aggressive** | Max conviction | Quality at discount |
| Euphoria (VIX < 12) | **Defensive** | Reduce exposure | Book profits |
| Normal Range | **Selective** | Standard sizing | Follow framework |
| Sector Rotation | **Tactical** | Reallocate | Emerging themes |

---

## PART 1: THE 3-GATE ANALYSIS SYSTEM

Every stock must pass through THREE gates before investment:

```
┌─────────────────────────────────────────────────────────────────┐
│                    INVESTMENT DECISION FLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   GATE 1: QUALITY          GATE 2: VALUATION      GATE 3: TIMING│
│   ┌─────────────┐          ┌─────────────┐        ┌────────────┐│
│   │ Business    │          │ Intrinsic   │        │ Technical  ││
│   │ Quality     │──PASS──► │ Value vs    │─PASS─► │ Entry      ││
│   │ Assessment  │          │ Market Price│        │ Signals    ││
│   └─────────────┘          └─────────────┘        └────────────┘│
│         │                        │                      │        │
│       FAIL                     FAIL                   FAIL       │
│         ▼                        ▼                      ▼        │
│      [SKIP]                 [WATCHLIST]             [WAIT]       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## PART 2: FUNDAMENTAL ANALYSIS FRAMEWORK

### The 10-Point Investment Checklist

Based on Zerodha Varsity Module 3 (Fundamental Analysis)

| # | Criterion | Threshold | Weight |
|---|-----------|-----------|--------|
| 1 | **Gross Profit Margin** | > 20% | High |
| 2 | **Return on Equity (ROE)** | > 15% (prefer > 20%) | High |
| 3 | **Return on Capital Employed (ROCE)** | > 15% | High |
| 4 | **Debt-to-Equity Ratio** | < 1 (prefer < 0.5) | High |
| 5 | **Interest Coverage Ratio** | > 3x | Medium |
| 6 | **Operating Cash Flow** | Positive & growing | High |
| 7 | **Revenue Growth (3Y CAGR)** | > 10% | Medium |
| 8 | **PAT Growth (3Y CAGR)** | > 12% | Medium |
| 9 | **Promoter Holding** | > 50%, no pledge | Medium |
| 10 | **Free Cash Flow** | Positive | High |

**Scoring**: Each criterion passed = 1 point. **Minimum 7/10 to proceed.**

---

### Financial Ratios Reference

#### Profitability Ratios

| Ratio | Formula | Good | Excellent | Red Flag |
|-------|---------|------|-----------|----------|
| **ROE** | Net Profit / Equity | > 15% | > 20% | < 10% |
| **ROCE** | EBIT / Capital Employed | > 15% | > 20% | < 12% |
| **ROA** | Net Profit / Total Assets | > 5% | > 8% | < 3% |
| **EBITDA Margin** | EBITDA / Revenue | > 15% | > 25% | < 10% |
| **PAT Margin** | Net Profit / Revenue | > 8% | > 15% | < 5% |
| **Gross Margin** | Gross Profit / Revenue | > 25% | > 40% | < 15% |

#### Leverage Ratios

| Ratio | Formula | Good | Caution | Danger |
|-------|---------|------|---------|--------|
| **Debt/Equity** | Total Debt / Equity | < 1 | 1-2 | > 2 |
| **Interest Coverage** | EBIT / Interest | > 3x | 2-3x | < 2x |
| **Current Ratio** | Current Assets / Liabilities | > 1.5 | 1-1.5 | < 1 |
| **Quick Ratio** | (CA - Inventory) / CL | > 1 | 0.8-1 | < 0.8 |
| **Debt/EBITDA** | Total Debt / EBITDA | < 2x | 2-3x | > 3x |

#### Valuation Ratios

| Ratio | Use Case | Cheap | Fair | Expensive |
|-------|----------|-------|------|-----------|
| **P/E Ratio** | Earnings based | < 15 | 15-25 | > 30 |
| **P/B Ratio** | Asset based (Banks) | < 1.5 | 1.5-3 | > 4 |
| **P/S Ratio** | Revenue based (Tech) | < 3 | 3-6 | > 8 |
| **EV/EBITDA** | Cash flow based | < 10 | 10-15 | > 20 |
| **PEG Ratio** | Growth adjusted | < 1 | 1-1.5 | > 2 |

---

### Moat Analysis Framework

#### Types of Economic Moats

| Moat Type | Description | Indian Examples |
|-----------|-------------|-----------------|
| **Brand Power** | Premium pricing ability | Asian Paints, Titan, Page Industries |
| **Network Effects** | Value increases with users | IRCTC, BSE, CDSL |
| **Switching Costs** | Painful to switch | TCS (enterprise), HDFC Bank |
| **Cost Advantage** | Lowest cost producer | Tata Steel, UltraTech |
| **Intangible Assets** | Patents, licenses, IP | Divi's Labs, Pidilite |
| **Efficient Scale** | Natural monopoly dynamics | Power Grid, IEX |

#### Moat Assessment Questions

1. Can competitors replicate this business in 3 years?
2. Has the company maintained margins despite competition?
3. Does pricing power exist (can they raise prices)?
4. Is customer retention high (> 85%)?
5. What would it cost to build this from scratch?

**Moat Score**: Strong (3+ Yes) | Moderate (2 Yes) | Weak (< 2 Yes)

---

### DCF Valuation Method

#### Step-by-Step Intrinsic Value Calculation

```
INTRINSIC VALUE CALCULATION

Step 1: Calculate Free Cash Flow (FCF)
   FCF = Operating Cash Flow - Capital Expenditure

Step 2: Project FCF for 5-10 years
   Use conservative growth rate (< historical average)
   Year 1-5: Growth at 12-15%
   Year 6-10: Taper to 8-10%

Step 3: Calculate Terminal Value
   Terminal Value = FCF(Year 10) × (1 + g) / (r - g)
   Where: g = perpetual growth (4-5%)
          r = discount rate (12-15% for India)

Step 4: Discount to Present Value
   PV = Σ [FCF(t) / (1 + r)^t] + Terminal Value / (1 + r)^10

Step 5: Calculate Per Share Value
   Intrinsic Value = Total PV / Shares Outstanding

Step 6: Apply Margin of Safety
   Buy Price = Intrinsic Value × (1 - MoS)
   MoS: 25% for quality, 35% for average, 50% for speculative
```

#### Simplified DCF Template

| Year | FCF (₹ Cr) | Growth | Discount Factor | Present Value |
|------|------------|--------|-----------------|---------------|
| 0 | 1,000 | - | 1.000 | 1,000 |
| 1 | 1,120 | 12% | 0.870 | 974 |
| 2 | 1,254 | 12% | 0.756 | 948 |
| 3 | 1,405 | 12% | 0.658 | 924 |
| 4 | 1,573 | 12% | 0.572 | 900 |
| 5 | 1,762 | 12% | 0.497 | 876 |
| TV | 22,025 | 5% | 0.497 | 10,946 |
| **Total PV** | | | | **16,568** |

---

## PART 3: TECHNICAL ANALYSIS INTEGRATION

> **Reference**: Full technical framework in `zerodha-technical-analysis-framework.md`

### Quick Technical Checklist (7 Points)

| # | Criterion | Pass/Fail |
|---|-----------|-----------|
| 1 | Recognizable candlestick pattern | [ ] |
| 2 | Prior trend supports the pattern | [ ] |
| 3 | S&R within 4% of stoploss | [ ] |
| 4 | Volume ≥ 10-day average | [ ] |
| 5 | RRR ≥ 1.5 | [ ] |
| 6 | RSI/MACD confirmation | [ ] |
| 7 | Dow Theory alignment | [ ] |

**Minimum 5/7 to proceed with trade timing.**

### Optimal Entry Zones

| Technical Condition | Entry Quality | Action |
|---------------------|---------------|--------|
| At support + RSI < 30 + bullish candle | **Excellent** | Full position |
| Above 200-DMA + Golden Cross forming | **Good** | 70% position |
| Breakout with volume | **Good** | 70% position |
| No clear setup | **Wait** | Add to watchlist |

---

## PART 4: SECTOR-SPECIFIC ANALYSIS TEMPLATES

### Banking & Financial Services (NBFCs, Banks)

#### Key Metrics Dashboard

| Metric | Threshold | Importance |
|--------|-----------|------------|
| **NIM (Net Interest Margin)** | > 3% | Critical |
| **GNPA (Gross NPA)** | < 3% | Critical |
| **NNPA (Net NPA)** | < 1.5% | Critical |
| **CASA Ratio** | > 40% | High |
| **Capital Adequacy (CAR)** | > 12% | Regulatory |
| **ROA** | > 1% | High |
| **ROE** | > 15% | High |
| **Credit Cost** | Declining trend | Medium |
| **P/B Ratio** | Primary valuation | - |
| **Provision Coverage Ratio (PCR)** | > 70% | High |

#### Banking-Specific Checklist

- [ ] Asset quality stable or improving (GNPA/NNPA trend)
- [ ] Deposit growth > Credit growth (funding stability)
- [ ] No lumpy corporate loan exposures
- [ ] Digital adoption metrics growing
- [ ] Management commentary on slippages
- [ ] Sector-specific NPAs (MFI, restructured book)

#### Valuation Framework for Banks

| Bank Type | P/B Range | ROE Expected |
|-----------|-----------|--------------|
| Large Private Banks | 2.5-4x | 15-18% |
| Mid Private Banks | 1.5-2.5x | 12-15% |
| PSU Banks | 0.8-1.5x | 10-14% |
| Small Finance Banks | 1.5-3x | 12-16% |
| NBFCs | 2-4x | 15-20% |

---

### IT & Technology Services

#### Key Metrics Dashboard

| Metric | Threshold | Importance |
|--------|-----------|------------|
| **Revenue per Employee** | Growing YoY | High |
| **Attrition Rate** | < 20% | Critical |
| **Deal Pipeline (TCV)** | Growing | High |
| **Digital Revenue %** | > 40% & growing | High |
| **Utilization Rate** | > 80% | High |
| **Offshore-Onsite Mix** | Improving offshore | Medium |
| **Operating Margin** | > 20% | High |
| **Cash Conversion** | > 100% | High |

#### IT-Specific Checklist

- [ ] Large deal wins in recent quarters
- [ ] Digital services growing faster than legacy
- [ ] Client concentration < 15% from top 5
- [ ] Wage hike cycle impact absorbed
- [ ] Currency hedging in place
- [ ] Fresher hiring pipeline strong

#### Valuation Framework for IT

| Company Size | P/E Range | Growth Expected |
|--------------|-----------|-----------------|
| Tier 1 (TCS, Infy, Wipro) | 20-30x | 8-12% |
| Tier 2 (LTI, Mindtree, Mphasis) | 25-35x | 12-18% |
| Midcap IT | 20-30x | 15-25% |
| Product Companies | 30-50x | 20-30% |

---

### 2026 Booming Sectors

#### 1. Defence & Aerospace

| Metric | What to Look For |
|--------|------------------|
| **Order Book** | > 3x annual revenue |
| **Order Book/Sales** | Growing ratio |
| **Execution Rate** | Improving YoY |
| **Indigenization %** | Higher = better margins |
| **Export Orders** | Diversification signal |
| **R&D Spend** | > 3% of revenue |

**Key Players**: HAL, BEL, Bharat Dynamics, MTAR, Data Patterns

#### 2. Renewables & Green Energy

| Metric | What to Look For |
|--------|------------------|
| **Capacity (MW/GW)** | Additions on track |
| **PPA Visibility** | Long-term contracts |
| **PLF (Plant Load Factor)** | > 22% for solar |
| **Tariff Trends** | Stability in auctions |
| **Debt Levels** | < 4x EBITDA |
| **EBITDA/MW** | Improving |

**Key Players**: Adani Green, NTPC Green, Tata Power, JSW Energy

#### 3. EMS (Electronics Manufacturing Services)

| Metric | What to Look For |
|--------|------------------|
| **Customer Wins** | New marquee clients |
| **Capex Plans** | Expansion underway |
| **PLI Benefits** | Receiving incentives |
| **Revenue per Sq Ft** | Asset efficiency |
| **Vertical Mix** | Diversification |
| **Working Capital** | < 60 days cycle |

**Key Players**: Dixon, Kaynes, Syrma SGS, Amber, Voltas (via venture)

#### 4. Railways & Infrastructure

| Metric | What to Look For |
|--------|------------------|
| **Order Book/Sales** | > 3x |
| **Execution Rate** | % of orders converted to revenue |
| **Receivables Days** | < 90 days |
| **Working Capital** | Manageable levels |
| **New Order Inflow** | YoY growth |
| **Margin Stability** | Despite input costs |

**Key Players**: RVNL, IRFC, Titagarh Rail, Jupiter Wagons, Texmaco

#### 5. Data Centers & Cloud

| Metric | What to Look For |
|--------|------------------|
| **MW Capacity** | Total and planned |
| **Utilization Rate** | > 70% |
| **Customer Stickiness** | Long-term contracts |
| **PUE (Power Efficiency)** | < 1.5 |
| **Revenue per MW** | Benchmark |
| **Capex Pipeline** | Funded & on track |

**Key Players**: Yotta (Adani), CtrlS, NxtGen, Pi Datacenters

#### 6. Specialty Chemicals

| Metric | What to Look For |
|--------|------------------|
| **EBITDA Margin** | > 18% |
| **China+1 Status** | Beneficiary evidence |
| **Customer Geography** | Export % growing |
| **R&D Pipeline** | New molecules |
| **Capacity Utilization** | > 75% |
| **Working Capital** | Efficient |

**Key Players**: Navin Fluorine, SRF, PI Industries, Aarti Industries, Clean Science

---

## PART 5: CONVICTION-BASED POSITION SIZING

### Position Sizing Matrix

Based on **Moderate Risk Profile** (8-10% max per position)

| Conviction Level | Fundamental Score | Technical Score | Position Size |
|------------------|-------------------|-----------------|---------------|
| **HIGH** | 8-10/10 | 6-7/7 | 8-10% of portfolio |
| **MEDIUM** | 6-7/10 | 4-5/7 | 4-6% of portfolio |
| **LOW** | 5-6/10 | 4+/7 | 2-3% of portfolio |
| **SPECULATIVE** | < 5/10 | Any | Max 1-2% |

### Risk Management Rules

```
POSITION SIZING FORMULA

Step 1: Determine Portfolio Risk per Trade
   Max Risk = 2% of total portfolio

Step 2: Calculate Risk per Share
   Risk/Share = Entry Price - Stoploss

Step 3: Calculate Position Size
   Max Shares = (Portfolio × 2%) / Risk per Share

Step 4: Apply Conviction Multiplier
   HIGH: Use full calculated size
   MEDIUM: Use 70% of calculated size
   LOW: Use 50% of calculated size

Example (₹10,00,000 portfolio):
   Max Risk: ₹20,000
   Entry: ₹500, SL: ₹450
   Risk/Share: ₹50
   Max Shares: 400
   Position: ₹2,00,000 (20% of portfolio)

   If MEDIUM conviction: 280 shares (₹1,40,000)
```

### Portfolio Allocation Guidelines

| Category | Allocation | Purpose |
|----------|------------|---------|
| Core Holdings | 60-70% | High-conviction, quality stocks |
| Tactical Bets | 20-30% | Momentum, sector themes |
| Cash Buffer | 10-15% | Dry powder for opportunities |

---

## PART 6: RED FLAGS CHECKLIST

### Instant Disqualifiers (Walk Away)

| Red Flag | Why It Matters |
|----------|----------------|
| **Promoter Pledge > 20%** | Potential forced selling |
| **Related Party Transactions > 5% of revenue** | Siphoning risk |
| **Auditor Resignation/Change** | Accounting concerns |
| **Negative Operating Cash Flow (2+ years)** | Business model broken |
| **Debt > 3x EBITDA** | Overleveraged |
| **Qualified Audit Opinion** | Serious accounting issues |
| **SEBI/ED Investigation** | Regulatory risk |
| **Promoter Selling > 5% in 6 months** | Lack of confidence |
| **Receivables > 120 days** | Collection issues |
| **Inventory > 90 days (non-seasonal)** | Demand concern |

### Warning Signs (Proceed with Caution)

| Warning | Action Required |
|---------|-----------------|
| Promoter pledge 10-20% | Monitor quarterly |
| Debt/Equity 1-2x | Check interest coverage |
| Declining margins (2 quarters) | Understand reasons |
| Key management exits | Assess impact |
| Customer concentration > 30% | Evaluate dependency |
| Capex delays | Check funding |

---

## PART 7: COMPLETE ANALYSIS REPORT TEMPLATE

### Stock Analysis: [COMPANY NAME]

```
═══════════════════════════════════════════════════════════════════
                    INVESTMENT ANALYSIS REPORT
                    [COMPANY NAME] | [TICKER]
                    Date: [DD-MMM-YYYY]
═══════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERDICT: [BUY / ACCUMULATE / HOLD / AVOID]
Conviction: [HIGH / MEDIUM / LOW]
Target Horizon: [1-6 months positional]

One-Line Summary: [What makes this stock attractive/unattractive]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. BUSINESS OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sector: [Sector]
Market Cap: ₹[X] Cr ([Large/Mid/Small Cap])
Business Description: [2-3 lines on what the company does]

MOAT ASSESSMENT:
├── Brand Power: [Strong/Moderate/Weak]
├── Network Effects: [Yes/No]
├── Switching Costs: [High/Medium/Low]
├── Cost Advantage: [Yes/No]
└── Moat Score: [Strong/Moderate/Weak]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. FUNDAMENTAL SCORECARD (Gate 1 & 2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

10-POINT CHECKLIST:
┌─────────────────────────────────────────────────────────────────┐
│ # │ Criterion                │ Value    │ Threshold │ Status   │
├───┼──────────────────────────┼──────────┼───────────┼──────────┤
│ 1 │ Gross Profit Margin      │ [X]%     │ > 20%     │ [✓/✗]    │
│ 2 │ ROE                      │ [X]%     │ > 15%     │ [✓/✗]    │
│ 3 │ ROCE                     │ [X]%     │ > 15%     │ [✓/✗]    │
│ 4 │ Debt/Equity              │ [X]      │ < 1       │ [✓/✗]    │
│ 5 │ Interest Coverage        │ [X]x     │ > 3x      │ [✓/✗]    │
│ 6 │ Operating Cash Flow      │ [+/-]    │ Positive  │ [✓/✗]    │
│ 7 │ Revenue Growth (3Y CAGR) │ [X]%     │ > 10%     │ [✓/✗]    │
│ 8 │ PAT Growth (3Y CAGR)     │ [X]%     │ > 12%     │ [✓/✗]    │
│ 9 │ Promoter Holding         │ [X]%     │ > 50%     │ [✓/✗]    │
│10 │ Free Cash Flow           │ [+/-]    │ Positive  │ [✓/✗]    │
└─────────────────────────────────────────────────────────────────┘
FUNDAMENTAL SCORE: [X]/10

VALUATION METRICS:
├── P/E Ratio: [X] (Sector Avg: [Y])
├── P/B Ratio: [X] (Sector Avg: [Y])
├── EV/EBITDA: [X] (Sector Avg: [Y])
├── PEG Ratio: [X]
└── Valuation: [Cheap / Fair / Expensive]

DCF INTRINSIC VALUE: ₹[X]
Current Price: ₹[Y]
Margin of Safety: [Z]%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. TECHNICAL ANALYSIS (Gate 3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PRICE DATA:
├── Current Price: ₹[X]
├── 52W High: ₹[X] ([Y]% away)
├── 52W Low: ₹[X] ([Y]% away)
├── 50-DMA: ₹[X] (Price [Above/Below])
└── 200-DMA: ₹[X] (Price [Above/Below])

7-POINT TECHNICAL CHECKLIST:
┌─────────────────────────────────────────────────────────────────┐
│ # │ Criterion                          │ Status     │ Pass/Fail │
├───┼────────────────────────────────────┼────────────┼───────────┤
│ 1 │ Candlestick Pattern               │ [Pattern]   │ [✓/✗]     │
│ 2 │ Prior Trend Exists                │ [Yes/No]    │ [✓/✗]     │
│ 3 │ S&R within 4% of SL               │ [Level]     │ [✓/✗]     │
│ 4 │ Volume ≥ 10-day avg               │ [X vs Y]    │ [✓/✗]     │
│ 5 │ RRR ≥ 1.5                         │ [X:1]       │ [✓/✗]     │
│ 6 │ RSI/MACD Confirmation             │ [Values]    │ [✓/✗]     │
│ 7 │ Dow Theory Alignment              │ [Trend]     │ [✓/✗]     │
└─────────────────────────────────────────────────────────────────┘
TECHNICAL SCORE: [X]/7

SUPPORT & RESISTANCE MAP:
                    [Major Resistance 2] ─── ₹[X]
                    [Resistance 1] ──────── ₹[X]
        ───────────► Current Price ◄────── ₹[X]
                    [Support 1] ─────────── ₹[X]
                    [Major Support 2] ───── ₹[X]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RED FLAGS CHECK:
├── Promoter Pledge: [X]% [OK/CAUTION/RED FLAG]
├── Related Party Txns: [X]% of revenue [OK/CAUTION]
├── Auditor Status: [Unchanged/Changed] [OK/CAUTION]
├── Operating Cash Flow: [Positive/Negative]
├── Debt/EBITDA: [X]x [OK/CAUTION/RED FLAG]
└── Regulatory Issues: [None/Pending]

KEY RISKS:
1. [Risk 1]
2. [Risk 2]
3. [Risk 3]

CATALYSTS (Positive & Negative):
[+] [Positive catalyst 1]
[+] [Positive catalyst 2]
[-] [Negative catalyst 1]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. TRADE RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTION: [BUY / ACCUMULATE / HOLD / AVOID]

TRADE SETUP:
┌─────────────────────────────────────────────────────────────────┐
│ Entry Zone:      ₹[X] - ₹[Y]                                    │
│ Stoploss:        ₹[Z] ([A]% risk)                               │
│ Target 1:        ₹[T1] ([B]% upside) - Book 40%                 │
│ Target 2:        ₹[T2] ([C]% upside) - Book 40%                 │
│ Target 3:        ₹[T3] ([D]% upside) - Trail rest               │
│ Risk-Reward:     [X:1]                                          │
└─────────────────────────────────────────────────────────────────┘

POSITION SIZING (₹10L Portfolio Example):
├── Conviction Level: [HIGH/MEDIUM/LOW]
├── Max Position: [X]% of portfolio = ₹[Y]
├── Shares to Buy: [Z] shares
└── Max Loss if SL Hit: ₹[A] ([B]% of portfolio)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. ACTION PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IF BUY:
□ Place limit order at ₹[Entry]
□ Set GTT stoploss at ₹[SL]
□ Set GTT target 1 at ₹[T1] for 40% qty
□ Review weekly for position management

IF WAIT:
□ Add to watchlist
□ Alert at ₹[Level] for entry opportunity
□ Re-analyze when [Condition] is met

IF AVOID:
□ Remove from consideration
□ Reason: [Why to skip]

═══════════════════════════════════════════════════════════════════
                         END OF REPORT
═══════════════════════════════════════════════════════════════════
```

---

## PART 8: DATA SOURCES

### Fundamental Data
| Source | URL | Data Available |
|--------|-----|----------------|
| Screener.in | screener.in | Financial statements, ratios, peer comparison |
| Trendlyne | trendlyne.com | Shareholding, scores, forecasts |
| BSE India | bseindia.com | Official filings, corporate actions |
| NSE India | nseindia.com | Official filings, FII/DII data |
| Tijori Finance | tijorifinance.com | Detailed financials, segments |

### Technical Data
| Source | Use |
|--------|-----|
| Zerodha Kite MCP | Real-time prices, historical OHLC |
| TradingView | Charts, patterns, indicators |
| Trendlyne | Technical scores, pivot points |
| Investing.com | International data, forex |

---

## PART 9: QUICK REFERENCE CHECKLISTS

### Pre-Trade Checklist

```
□ Fundamental Score ≥ 7/10?
□ No red flags present?
□ Valuation has margin of safety?
□ Technical Score ≥ 5/7?
□ RRR ≥ 1.5:1?
□ Position size within limits?
□ Entry/SL/Target defined?
□ GTT orders ready?
```

### Weekly Review Checklist

```
□ Open positions within SL range?
□ Any positions hit target 1?
□ Trailing SL updated for winners?
□ Fundamental news/results update?
□ Sector rotation check?
□ Cash allocation check?
```

---

## APPENDIX: KEY FORMULAS

```
═══════════════════════════════════════════════════════════════════
                       FORMULA QUICK REFERENCE
═══════════════════════════════════════════════════════════════════

VALUATION:
P/E Ratio = Market Price / EPS
P/B Ratio = Market Price / Book Value per Share
EV/EBITDA = (Market Cap + Debt - Cash) / EBITDA
PEG Ratio = P/E / Earnings Growth Rate

PROFITABILITY:
ROE = Net Profit / Shareholders' Equity × 100
ROCE = EBIT / (Total Assets - Current Liabilities) × 100
ROA = Net Profit / Total Assets × 100

LEVERAGE:
Debt/Equity = Total Debt / Shareholders' Equity
Interest Coverage = EBIT / Interest Expense
Current Ratio = Current Assets / Current Liabilities

CASH FLOW:
FCF = Operating Cash Flow - Capital Expenditure
Cash Conversion = Operating Cash Flow / Net Profit × 100

GROWTH:
CAGR = (Ending Value / Beginning Value)^(1/n) - 1

POSITION SIZING:
Max Shares = (Portfolio × Max Risk %) / (Entry - Stoploss)
Position Value = Max Shares × Entry Price

RISK-REWARD:
RRR = (Target - Entry) / (Entry - Stoploss)

═══════════════════════════════════════════════════════════════════
```

---

*Framework Version: 1.0*
*Created: February 2026*
*Based on: Zerodha Varsity (TA & FA Modules) + Investment Banking Best Practices*
*Designed for: Positional Trading (1-6 months) with Moderate Risk Appetite*
