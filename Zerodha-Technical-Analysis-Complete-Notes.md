# ZERODHA VARSITY: TECHNICAL ANALYSIS - COMPLETE STUDY NOTES
## All 22 Chapters Summarized

---

# PART 1: FOUNDATIONS (Chapters 1-3)

---

## Chapter 1: Background

### What is Technical Analysis?
Technical Analysis (TA) is a research methodology that identifies trading opportunities by analyzing market participant actions visualized through stock charts.

### TA vs Fundamental Analysis

| Aspect | Technical Analysis | Fundamental Analysis |
|--------|-------------------|---------------------|
| Focus | Price & Volume patterns | Company financials |
| Timeframe | Short-term (days to weeks) | Long-term (months to years) |
| Data Used | Charts, indicators | Balance sheet, P&L, ratios |
| Analogy | Following the crowd | Researching each vendor |

### Essential Components of a Trade Setup
Every trade must have:
1. **Direction** - Bullish or Bearish view
2. **Entry Price** - Exact price to buy/sell
3. **Exit Price** - Target price
4. **Stoploss** - Maximum loss acceptable
5. **Risk-Reward Ratio** - Reward should exceed risk
6. **Holding Period** - Expected duration

### Key Expectations
- TA works best for **short-term trades** (not investments)
- Expect **frequent small profits**, not big windfalls
- **Strict risk management** is non-negotiable
- "If the trade goes bad, cut the losses"

---

## Chapter 2: Introducing Technical Analysis

### The 4 Core Assumptions

#### 1. Markets Discount Everything
> All known and unknown information is already reflected in the price.

Even insider activity shows up in price movement before news becomes public.

#### 2. The "How" Matters More Than "Why"
Focus on **price reaction**, not the reason behind it. Technical analysts don't need to know WHY a stock moved, only HOW it moved.

#### 3. Price Moves in Trends
> "All major moves in the market are an outcome of a trend."

Prices don't jump randomly - they move in identifiable patterns over time.

#### 4. History Repeats Itself
Human psychology doesn't change. The same patterns of greed and fear repeat across generations, making chart patterns reliable.

### OHLC - The 4 Price Points

| Term | Meaning | Importance |
|------|---------|------------|
| **Open** | First trade of the day | Shows overnight sentiment |
| **High** | Highest price of the day | Shows buyer strength |
| **Low** | Lowest price of the day | Shows seller strength |
| **Close** | Last trade of the day | **MOST IMPORTANT** - shows final sentiment |

> The **Close** is the most critical price - it determines who won the day (buyers or sellers).

---

## Chapter 3: Chart Types

### 1. Line Chart
```
Characteristics: Plots only closing prices
Advantage: Simple, shows trend quickly
Disadvantage: Misses Open, High, Low data
Use: Quick trend overview only
```

### 2. Bar Chart (OHLC)
```
Structure:
    |  ← High
  ──|  ← Open (left tick)
    |
    |──  ← Close (right tick)
    |  ← Low

Blue = Bullish (Close > Open)
Red = Bearish (Close < Open)
```
**Disadvantage**: Difficult to read patterns

### 3. Japanese Candlestick (PREFERRED)
```
     ─┬─   Upper Shadow (High)
    █████
    █████  Real Body (Open to Close)
    █████
     ─┴─   Lower Shadow (Low)

Green/Blue = Bullish (Close > Open)
Red/Black = Bearish (Close < Open)
```
**Advantage**: Easy visual pattern recognition
**Use**: Default choice for all traders

### Timeframe Selection

| Trader Type | Timeframe | Chart |
|-------------|-----------|-------|
| Investor | Monthly/Weekly | Low noise |
| Swing Trader | Daily (EOD) | Medium noise |
| Day Trader | 5-15 minute | High noise |

---

# PART 2: CANDLESTICK PATTERNS (Chapters 4-10)

---

## Chapter 4: Getting Started with Candlesticks

### Candlestick Anatomy
```
BULLISH CANDLE          BEARISH CANDLE
     |                       |
     | Upper Shadow          | Upper Shadow
   ┌─┴─┐                   ┌─┴─┐
   │   │ ← Close           │   │ ← Open
   │ G │ Real Body         │ R │ Real Body
   │   │ ← Open            │   │ ← Close
   └─┬─┘                   └─┬─┘
     | Lower Shadow          | Lower Shadow
     |                       |
```

### Candle Psychology
- **Long body** = Strong conviction (buyers or sellers dominated)
- **Short body** = Indecision
- **Long upper shadow** = Sellers pushed price down from high
- **Long lower shadow** = Buyers pushed price up from low

---

## Chapters 5-7: Single Candlestick Patterns

### 1. MARUBOZU (Strong Momentum)

#### Bullish Marubozu
```
Structure: Full green body, NO shadows
    ┌───┐
    │   │
    │ G │  ← Open at Low, Close at High
    │   │
    └───┘
Signal: STRONG BULLISH
Action: Buy at close or next day open
Stoploss: Low of the Marubozu candle
```

#### Bearish Marubozu
```
Structure: Full red body, NO shadows
    ┌───┐
    │   │
    │ R │  ← Open at High, Close at Low
    │   │
    └───┘
Signal: STRONG BEARISH
Action: Sell/Short at close
Stoploss: High of the Marubozu candle
```

---

### 2. DOJI (Indecision)
```
Structure: Open ≈ Close (tiny or no body)

    |
    |
  ──┼──  ← Open = Close
    |
    |

Signal: INDECISION - neither buyers nor sellers won
Action: WAIT for next candle for confirmation
```

**Types of Doji:**
- **Standard Doji**: Equal shadows
- **Dragonfly Doji**: Long lower shadow (bullish at bottom)
- **Gravestone Doji**: Long upper shadow (bearish at top)

---

### 3. SPINNING TOP (Indecision)
```
Structure: Small body, long shadows both sides

      |
    ┌─┴─┐
    │   │  ← Small body
    └─┬─┘
      |

Signal: INDECISION
Action: WAIT - trend may reverse or continue
```

---

### 4. HAMMER (Bullish Reversal)
```
Structure: Small body at TOP, long LOWER shadow

    ┌─┐
    │ │  ← Small body (green or red)
    └┬┘
     |
     |   ← Lower shadow at least 2x body length
     |

Conditions:
- Must appear after a DOWNTREND
- Lower shadow ≥ 2x real body
- Little or no upper shadow

Signal: BULLISH REVERSAL
Action: Buy with confirmation (next green candle)
Stoploss: Low of the hammer
```

---

### 5. HANGING MAN (Bearish Warning)
```
Structure: SAME as Hammer

    ┌─┐
    │ │
    └┬┘
     |
     |
     |

Conditions:
- Must appear after an UPTREND
- Same structure as hammer

Signal: BEARISH WARNING (not as strong as hammer is bullish)
Action: Caution - consider reducing longs
```

---

### 6. SHOOTING STAR (Bearish Reversal)
```
Structure: Small body at BOTTOM, long UPPER shadow

     |
     |   ← Upper shadow at least 2x body
     |
    ┌┴┐
    │ │  ← Small body
    └─┘

Conditions:
- Must appear after an UPTREND
- Upper shadow ≥ 2x real body

Signal: BEARISH REVERSAL
Action: Sell/Short with confirmation
Stoploss: High of shooting star
```

---

## Chapters 8-10: Multiple Candlestick Patterns

### 1. ENGULFING PATTERNS (Strong Reversal)

#### Bullish Engulfing
```
Day 1        Day 2
  ┌─┐      ┌─────┐
  │R│      │     │
  │ │  →   │  G  │  ← Green candle ENGULFS red
  └─┘      │     │
           └─────┘

Conditions:
- Prior DOWNTREND must exist
- Day 2 green body completely covers Day 1 red body
- High volume on Day 2

Signal: STRONG BULLISH REVERSAL
Entry: Buy at Day 2 close
Stoploss: Low of Day 1 or Day 2 (whichever is lower)
```

#### Bearish Engulfing
```
Day 1        Day 2
  ┌─┐      ┌─────┐
  │G│      │     │
  │ │  →   │  R  │  ← Red candle ENGULFS green
  └─┘      │     │
           └─────┘

Conditions:
- Prior UPTREND must exist
- Day 2 red body completely covers Day 1 green body

Signal: STRONG BEARISH REVERSAL
Entry: Sell at Day 2 close
Stoploss: High of the pattern
```

---

### 2. HARAMI PATTERNS (Moderate Reversal)

#### Bullish Harami
```
Day 1        Day 2
┌─────┐      ┌─┐
│     │      │G│  ← Small green INSIDE large red
│  R  │  →   │ │
│     │      └─┘
└─────┘

Signal: MODERATE BULLISH (pregnant pattern - "harami" = pregnant in Japanese)
Entry: Buy with confirmation
```

#### Bearish Harami
```
Day 1        Day 2
┌─────┐      ┌─┐
│     │      │R│  ← Small red INSIDE large green
│  G  │  →   │ │
│     │      └─┘
└─────┘

Signal: MODERATE BEARISH
```

---

### 3. MORNING STAR (Strong Bullish Reversal - 3 Candles)
```
Day 1      Day 2      Day 3
┌───┐                 ┌───┐
│   │                 │   │
│ R │      ┌─┐        │ G │
│   │  →   │ │   →    │   │
│   │      └─┘        │   │
└───┘     (small)     └───┘

Structure:
- Day 1: Large red candle (downtrend continues)
- Day 2: Small body (star) - gaps down, shows indecision
- Day 3: Large green candle - closes above Day 1 midpoint

Signal: STRONG BULLISH REVERSAL
Entry: Buy at Day 3 close
Stoploss: Low of Day 2
```

---

### 4. EVENING STAR (Strong Bearish Reversal - 3 Candles)
```
Day 1      Day 2      Day 3
           ┌─┐
┌───┐      │ │        ┌───┐
│   │  →   └─┘   →    │   │
│ G │     (small)     │ R │
│   │                 │   │
└───┘                 └───┘

Structure: Opposite of Morning Star

Signal: STRONG BEARISH REVERSAL
Entry: Sell at Day 3 close
Stoploss: High of Day 2
```

---

# PART 3: SUPPORT & RESISTANCE (Chapter 11)

---

## Definitions

**SUPPORT**: Price level where demand is strong enough to prevent further decline
- "Floor" that holds the price up
- Buyers step in at this level

**RESISTANCE**: Price level where supply is strong enough to prevent further rise
- "Ceiling" that caps the price
- Sellers step in at this level

## How to Identify S&R Levels

1. **Load adequate data**: 3-6 months for short-term; 12-18 months for long-term
2. **Find reversal points**: Where did price bounce back multiple times?
3. **Draw horizontal lines**: At zones where price reversed 3+ times
4. **Create zones, not exact lines**: S&R are zones, not precise prices

```
RESISTANCE ════════════════════════  Price bounced DOWN from here 3+ times
                    ╱╲    ╱╲
                   ╱  ╲  ╱  ╲
                  ╱    ╲╱    ╲
                 ╱              ╲
SUPPORT    ════════════════════════  Price bounced UP from here 3+ times
```

## Key S&R Rules

| Rule | Application |
|------|-------------|
| **More touches = Stronger level** | S/R tested 5 times > tested 2 times |
| **Recent tests = More relevant** | Level tested last month > tested 2 years ago |
| **S&R flip** | Broken support becomes resistance (and vice versa) |
| **Round numbers** | ₹100, ₹500, ₹1000 act as psychological S&R |

## Trading Rule: The 4% Rule

> **If S&R is more than 4% away from your entry, SKIP the trade.**

S&R should align with your stoploss. If support is too far below your entry, the risk becomes too large.

---

# PART 4: VOLUME ANALYSIS (Chapter 12)

---

## Why Volume Matters

> Volume confirms price moves. Price tells you WHAT happened; Volume tells you HOW STRONG it was.

## Volume-Price Matrix

| Price | Volume | Interpretation | Action |
|-------|--------|----------------|--------|
| ↑ Up | ↑ High | **BULLISH** - Smart money buying | BUY signal |
| ↑ Up | ↓ Low | **CAUTION** - Weak rally, possible trap | AVOID |
| ↓ Down | ↑ High | **BEARISH** - Smart money selling | SELL signal |
| ↓ Down | ↓ Low | **CAUTION** - Weak decline | AVOID |

## Volume Benchmarks

- Compare today's volume to **10-day average volume**
- **Above average** = High volume = Conviction move
- **Below average** = Low volume = Suspect move

## Volume Signals

```
VALID BREAKOUT                    FALSE BREAKOUT
Price breaks resistance           Price breaks resistance
Volume: 2x average         vs     Volume: Below average
Result: Trend continues           Result: Price falls back
```

---

# PART 5: MOVING AVERAGES (Chapter 13)

---

## What is a Moving Average?

A Moving Average smooths price data to show the underlying trend by averaging prices over a specific period.

## Types of Moving Averages

### Simple Moving Average (SMA)
```
Formula: SMA = (Sum of closing prices for N days) / N

Example 5-day SMA:
Day 1: ₹100
Day 2: ₹102
Day 3: ₹104
Day 4: ₹103
Day 5: ₹105
SMA = (100+102+104+103+105) / 5 = ₹102.8
```

### Exponential Moving Average (EMA)
- Gives MORE weight to recent prices
- Reacts FASTER than SMA
- Preferred for short-term trading

## Key Moving Averages

| MA | Period | Use Case |
|----|--------|----------|
| 9 EMA | 9 days | Very short-term |
| 21 EMA | 21 days | Short-term |
| **50 DMA** | 50 days | **Medium-term trend** |
| **200 DMA** | 200 days | **Long-term trend** |

## MA Trading Rules

### Basic Rules
- **Price ABOVE MA** = Bullish
- **Price BELOW MA** = Bearish

### Crossover Signals

**Golden Cross** (Bullish):
```
50 DMA crosses ABOVE 200 DMA
Signal: Long-term uptrend beginning
Action: BUY
```

**Death Cross** (Bearish):
```
50 DMA crosses BELOW 200 DMA
Signal: Long-term downtrend beginning
Action: SELL
```

### MA as Support/Resistance
- In uptrends, MAs act as **support** (price bounces off MA)
- In downtrends, MAs act as **resistance** (price gets rejected at MA)

---

# PART 6: INDICATORS (Chapters 14-15)

---

## RSI - Relative Strength Index (Chapter 14)

### What is RSI?
RSI measures the speed and magnitude of recent price changes to identify overbought or oversold conditions.

**Range**: 0 to 100
**Default Period**: 14 days

### RSI Interpretation

| RSI Range | Condition | Signal |
|-----------|-----------|--------|
| **0-30** | OVERSOLD | Look to BUY |
| 30-70 | Neutral | No clear signal |
| **70-100** | OVERBOUGHT | Look to SELL |

### RSI Trading Rules

```
RSI crosses ABOVE 30 (from oversold)
→ Potential BOTTOM forming
→ Look for BUY opportunity

RSI crosses BELOW 70 (from overbought)
→ Potential TOP forming
→ Look for SELL opportunity
```

### Advanced RSI Usage

- **RSI stuck above 70** in strong uptrend = Don't short (momentum)
- **RSI stuck below 30** in strong downtrend = Don't buy (weakness)
- **RSI Divergence**: Price makes new high but RSI doesn't = Warning sign

---

## MACD - Moving Average Convergence Divergence (Chapter 15)

### Components
1. **MACD Line** = 12 EMA - 26 EMA
2. **Signal Line** = 9 EMA of MACD Line
3. **Histogram** = MACD Line - Signal Line

### MACD Signals

| Condition | Signal |
|-----------|--------|
| MACD crosses ABOVE Signal Line | **BULLISH** - Buy |
| MACD crosses BELOW Signal Line | **BEARISH** - Sell |
| MACD above Zero Line | Bullish bias |
| MACD below Zero Line | Bearish bias |

```
BULLISH CROSSOVER          BEARISH CROSSOVER

    MACD ──╱──              ──╲── MACD
          ╱                    ╲
Signal ──╱──                ──╲── Signal

Buy when MACD crosses      Sell when MACD crosses
ABOVE signal line          BELOW signal line
```

---

## Bollinger Bands (Chapter 15)

### Components
- **Middle Band** = 20-day SMA
- **Upper Band** = Middle Band + (2 × Standard Deviation)
- **Lower Band** = Middle Band - (2 × Standard Deviation)

### Bollinger Band Signals

| Condition | Interpretation |
|-----------|----------------|
| Price touches Upper Band | Overbought - potential reversal |
| Price touches Lower Band | Oversold - potential reversal |
| Bands contracting (squeeze) | Low volatility - big move coming |
| Bands expanding | High volatility - trend in progress |

---

# PART 7: FIBONACCI RETRACEMENTS (Chapter 16)

---

## The Fibonacci Sequence
```
0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...

Each number = Sum of previous two numbers
```

## The Golden Ratio
```
Any Fibonacci number / Next Fibonacci number ≈ 0.618 (61.8%)
```

## Key Fibonacci Retracement Levels

| Level | Significance |
|-------|--------------|
| **23.6%** | Shallow pullback |
| **38.2%** | Moderate pullback - first support |
| **50.0%** | Psychological midpoint |
| **61.8%** | Deep pullback - GOLDEN RATIO |
| **78.6%** | Very deep pullback |

## How to Use Fibonacci

### In an UPTREND:
```
1. Identify the swing LOW and swing HIGH
2. Draw Fibonacci from LOW to HIGH
3. Look for price to retrace to 38.2%, 50%, or 61.8%
4. These levels act as SUPPORT for buying

HIGH ────────────────── 0%
           ╲
            ╲
             ╲────────── 23.6%
              ╲
               ╲──────── 38.2% ← Good buy zone
                ╲
                 ╲────── 50.0% ← Better buy zone
                  ╲
                   ╲──── 61.8% ← Best buy zone (if holds)
LOW ─────────────────── 100%
```

### Trading with Fibonacci
- Buy at Fibonacci support levels with stoploss below the next level
- Combine with candlestick patterns for confirmation
- Example: Bullish engulfing at 61.8% retracement = Strong buy signal

---

# PART 8: DOW THEORY (Chapters 17-18)

---

## The Three Trend Types

| Trend | Duration | Description | Analogy |
|-------|----------|-------------|---------|
| **Primary** | 1-3+ years | Main market direction | The TIDE |
| **Secondary** | 3 weeks - 3 months | Corrections against primary | WAVES |
| **Minor** | < 3 weeks | Day-to-day fluctuations | RIPPLES |

> **Rule**: Always trade in the direction of the PRIMARY trend.

## The Three Market Phases

### 1. ACCUMULATION Phase
```
- Smart money (institutions) quietly BUYS
- Public sentiment: NEGATIVE
- News: Bad
- Price: At lows, moving sideways
- Volume: Low but increasing on up days
```

### 2. MARKUP Phase (Public Participation)
```
- Trend becomes VISIBLE
- Traders and public JOIN IN
- News: Improving
- Price: Rising steadily
- Volume: Increasing
```

### 3. DISTRIBUTION Phase
```
- Smart money quietly SELLS
- Public sentiment: EUPHORIC
- News: Excellent (everyone is bullish)
- Price: Making new highs but momentum slowing
- Volume: High on down days
```

## Dow Theory Principles

1. **The market discounts everything**
2. **The market has three trends** (Primary, Secondary, Minor)
3. **Primary trends have three phases** (Accumulation, Markup, Distribution)
4. **Indices must confirm each other** (Nifty and Bank Nifty should agree)
5. **Volume must confirm the trend**
6. **Trends persist until clear reversal signals**

---

# PART 9: THE TRADING CHECKLIST (Chapter 19)

---

## The 7-Point Checklist

Before ANY trade, verify ALL criteria:

| # | Criterion | Requirement | Pass/Fail |
|---|-----------|-------------|-----------|
| 1 | **Candlestick Pattern** | Recognizable pattern identified | |
| 2 | **Prior Trend** | Pattern appears after required trend | |
| 3 | **S&R Alignment** | S&R within 4% of stoploss | |
| 4 | **Volume** | ≥ 10-day average volume | |
| 5 | **Risk-Reward** | Minimum 1.5:1 (prefer 2:1+) | |
| 6 | **Indicators** | RSI and/or MACD confirm | |
| 7 | **Dow Theory** | Trade aligns with primary trend | |

> **If ANY criterion fails, SKIP the trade.**

---

## Daily Trading Routine

### Step 1: Quick Scan (10-15 minutes)
- Review your watchlist (Nifty 50, sectoral indices)
- Look at last 3-4 candles only
- Flag stocks showing recognizable patterns

### Step 2: Deep Analysis (15-20 minutes per stock)
- Apply full 7-point checklist
- Calculate exact entry, stoploss, target
- Verify RRR ≥ 1.5

### Expected Output
- Typically **1-2 qualifying trades** from 50 stocks
- Most days you may find NO trades - that's okay

> "Deciding not to trade is itself a big trading decision."

---

# PART 10: POSITION SIZING & RISK MANAGEMENT (Chapter 9)

---

## The 2% Rule

> **Never risk more than 2% of your capital on any single trade.**

### Position Size Calculation

```
Step 1: Calculate Max Risk Amount
Max Risk = Total Capital × 2%

Step 2: Calculate Risk Per Share
Risk Per Share = Entry Price - Stoploss Price

Step 3: Calculate Max Shares
Max Shares = Max Risk Amount ÷ Risk Per Share

Step 4: Calculate Position Size
Position Size = Max Shares × Entry Price
```

### Example

```
Capital: ₹5,00,000
Max Risk (2%): ₹10,000

Trade Setup:
Entry: ₹600
Stoploss: ₹550
Risk/Share: ₹50

Max Shares: ₹10,000 ÷ ₹50 = 200 shares
Position Size: 200 × ₹600 = ₹1,20,000 (24% of capital)
```

---

# TRADE SETUP TEMPLATE

```
═══════════════════════════════════════════════════════════
TRADE SETUP
═══════════════════════════════════════════════════════════

STOCK: ____________________    DATE: ____________________

CHECKLIST:
[ ] 1. Pattern: ____________________
[ ] 2. Prior Trend: ____________________
[ ] 3. S&R within 4%: Support _______ Resistance _______
[ ] 4. Volume vs 10-day avg: _______ (Above/Below)
[ ] 5. RSI: _______ (Oversold/Neutral/Overbought)
[ ] 6. MACD: _______ (Bullish/Bearish)
[ ] 7. Dow Theory: _______ (Aligned/Against)

TRADE DETAILS:
Entry Price: ₹_______
Stoploss: ₹_______ (_____% risk)
Target 1: ₹_______ (_____% reward)
Target 2: ₹_______ (_____% reward)
Target 3: ₹_______ (_____% reward)

Risk-Reward Ratio: _____:1
Position Size: _______ shares (₹_______)

═══════════════════════════════════════════════════════════
VERDICT: [ ] BUY  [ ] SELL  [ ] WAIT  [ ] SKIP
═══════════════════════════════════════════════════════════
```

---

# KEY PRINCIPLES TO REMEMBER

| Principle | Meaning |
|-----------|---------|
| "Buy strength, sell weakness" | Don't catch falling knives |
| "The trend is your friend" | Trade with primary trend |
| "Cut losses, let profits run" | Strict stoploss, flexible targets |
| "Plan the trade, trade the plan" | No impulsive decisions |
| "Risk management first" | Protect capital above all |
| "No trade is also a trade" | Patience is a strategy |

---

# QUICK REFERENCE CARDS

## Bullish Signals
- Hammer after downtrend
- Bullish Engulfing
- Morning Star
- Price bouncing off support
- RSI crossing above 30
- MACD bullish crossover
- Price above 50 & 200 DMA
- Golden Cross

## Bearish Signals
- Shooting Star after uptrend
- Bearish Engulfing
- Evening Star
- Price rejected at resistance
- RSI crossing below 70
- MACD bearish crossover
- Price below 50 & 200 DMA
- Death Cross

## When to SKIP a Trade
- No clear pattern
- S&R more than 4% away
- Volume below average
- RRR less than 1.5:1
- Against primary trend
- Indicators not confirming

---

*Study Notes compiled from Zerodha Varsity Technical Analysis Module*
*Source: https://zerodha.com/varsity/module/technical-analysis/*

