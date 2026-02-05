# Zerodha Varsity Technical Analysis Framework
## Complete Trading Checklist & Strategy Guide

---

## THE 7-POINT TRADING CHECKLIST

Before ANY trade, ALL criteria must be checked:

| # | Criterion | Requirement | Source |
|---|-----------|-------------|--------|
| 1 | **Candlestick Pattern** | Must identify a specific recognizable pattern | Ch. 4-10 |
| 2 | **Prior Trend** | Bullish pattern needs prior downtrend (and vice versa) | Ch. 4 |
| 3 | **Support/Resistance** | S&R must align with stoploss; if >4% away, SKIP trade | Ch. 11 |
| 4 | **Volume** | Must be ≥ 10-day average on signal day | Ch. 12 |
| 5 | **Risk-Reward Ratio** | Minimum 1.5:1 (prefer 2:1 or higher) | Ch. 19 |
| 6 | **Indicator Confirmation** | RSI and/or MACD should support the trade | Ch. 14-15 |
| 7 | **Dow Theory** | Trade should align with primary trend direction | Ch. 17-18 |

> "If any criterion fails, skip the trade." — Zerodha Varsity

---

## CANDLESTICK PATTERNS TO IDENTIFY

### Single Candle Patterns (Ch. 5-7)

| Pattern | Structure | Signal | Entry Rule |
|---------|-----------|--------|------------|
| **Bullish Marubozu** | Full green body, no shadows | Strong bullish | Buy at close |
| **Bearish Marubozu** | Full red body, no shadows | Strong bearish | Sell/Short |
| **Hammer** | Small body at top, long lower shadow | Bullish reversal (after downtrend) | Buy with confirmation |
| **Hanging Man** | Same as Hammer | Bearish warning (after uptrend) | Caution |
| **Doji** | Open ≈ Close, cross shape | Indecision | Wait for next candle |
| **Spinning Top** | Small body, long shadows both sides | Indecision | Wait |

### Multiple Candle Patterns (Ch. 8-10)

| Pattern | Structure | Signal |
|---------|-----------|--------|
| **Bullish Engulfing** | Green candle engulfs prior red | Strong bullish reversal |
| **Bearish Engulfing** | Red candle engulfs prior green | Strong bearish reversal |
| **Bullish Harami** | Small green inside large red | Moderate bullish |
| **Bearish Harami** | Small red inside large green | Moderate bearish |
| **Morning Star** | Red → Small body → Green | Bullish reversal (3-candle) |
| **Evening Star** | Green → Small body → Red | Bearish reversal (3-candle) |

---

## SUPPORT & RESISTANCE (Ch. 11)

### Identification Process

1. Load 3-6 months data for short-term trades; 12-18 months for long-term
2. Identify zones where price reversed 3+ times
3. Draw horizontal lines at those levels
4. Levels above current price = Resistance; below = Support

### Trading Rules

- S&R must be within 4% of entry for valid stoploss placement
- More tests of a level = stronger the level
- When support breaks, it becomes resistance (and vice versa)

---

## VOLUME ANALYSIS (Ch. 12)

### Volume-Price Matrix

| Price | Volume | Interpretation | Action |
|-------|--------|----------------|--------|
| ↑ Up | ↑ High | **Bullish** — Smart money buying | Buy signal |
| ↑ Up | ↓ Low | **Caution** — Weak rally, possible trap | Avoid |
| ↓ Down | ↑ High | **Bearish** — Smart money selling | Sell signal |
| ↓ Down | ↓ Low | **Caution** — Weak decline, possible trap | Avoid |

### Measurement

- Compare today's volume to **10-day average**
- Above average = High volume
- Below average = Low volume

---

## RSI - RELATIVE STRENGTH INDEX (Ch. 14)

### Standard Levels

| RSI Range | Condition | Action |
|-----------|-----------|--------|
| 0-30 | **Oversold** | Look for buying opportunities |
| 30-70 | Neutral | No clear signal |
| 70-100 | **Overbought** | Look for selling opportunities |

### Advanced Interpretation

- RSI stuck above 70 in uptrend = Strong momentum, don't short
- RSI stuck below 30 in downtrend = Weak momentum, don't buy
- RSI crossing above 30 after being oversold = Potential bottom
- RSI crossing below 70 after being overbought = Potential top

---

## MACD (Ch. 15)

### Signals

| Condition | Signal |
|-----------|--------|
| MACD crosses ABOVE signal line | **Bullish** |
| MACD crosses BELOW signal line | **Bearish** |
| MACD above zero line | Bullish bias |
| MACD below zero line | Bearish bias |

---

## MOVING AVERAGES (Ch. 13)

### Basic Rules

- Price ABOVE MA = Bullish
- Price BELOW MA = Bearish

### Key MAs to Watch

| MA | Use |
|----|-----|
| 50-DMA | Short-term trend |
| 200-DMA | Long-term trend |
| 9/21 EMA | Short-term trades |
| 50/200 EMA | "Golden Cross" / "Death Cross" |

### Crossover Signals

- Short MA crosses ABOVE Long MA = Buy signal
- Short MA crosses BELOW Long MA = Sell signal

---

## FIBONACCI RETRACEMENTS (Ch. 16)

### Key Levels

| Level | Significance |
|-------|--------------|
| 23.6% | Shallow pullback |
| 38.2% | Moderate pullback |
| 50.0% | Psychological midpoint |
| 61.8% | Deep pullback (Golden Ratio) |

---

## DOW THEORY (Ch. 17-18)

### Three Trend Types

| Trend | Duration | Analogy |
|-------|----------|---------|
| **Primary** | 1-3+ years | The tide |
| **Secondary** | 3 weeks - 3 months | Waves |
| **Minor** | < 3 weeks | Ripples |

### Three Market Phases

1. **Accumulation**: Smart money buys at lows, sentiment negative
2. **Markup**: Trend visible, prices rise, traders join
3. **Distribution**: Smart money sells to retail, sentiment euphoric

> "Trade with the primary trend."

---

## DAILY SCANNING PROCESS (Ch. 19)

### Part 1: Quick Shortlisting
- Review watchlist (e.g., Nifty 50)
- Look at last 3-4 candles only
- Flag stocks showing recognizable patterns

### Part 2: Deep Analysis (15-20 min per stock)
- Apply full 7-point checklist
- Calculate exact entry, stoploss, target
- Verify RRR ≥ 1.5

### Expected Output
- Typically 1-2 qualifying trades from 50 stocks
- "Deciding not to trade is itself a big trading decision"

---

## POSITION SIZING

### Rule: Never risk more than 1-2% of capital per trade

### Calculation

```
Max Risk Amount = Capital × 2%
Risk Per Share = Entry Price - Stoploss
Max Shares = Max Risk Amount ÷ Risk Per Share
```

### Example (₹5,00,000 capital)

```
Max Risk: ₹10,000 (2%)
Entry: ₹600, Stoploss: ₹550
Risk/Share: ₹50
Max Shares: 200 shares
Position Size: ₹1,20,000 (24% of capital)
```

---

## TRADE SETUP TEMPLATE

```
STOCK: [Name]
DATE: [Date]

CHECKLIST:
[ ] 1. Pattern identified: ____________
[ ] 2. Prior trend exists: ____________
[ ] 3. S&R within 4%: Support _____ Resistance _____
[ ] 4. Volume above 10-day avg: Yes/No
[ ] 5. RSI: _____ (Oversold/Neutral/Overbought)
[ ] 6. MACD: Bullish/Bearish
[ ] 7. Dow Theory alignment: Yes/No

TRADE DETAILS:
Entry: ₹_____
Stoploss: ₹_____ (____% risk)
Target 1: ₹_____ (____% reward)
Target 2: ₹_____ (____% reward)
RRR: _____:1

VERDICT: BUY / SELL / WAIT / SKIP
```

---

## EXCELLENT BUY CONDITIONS

A high-probability buy setup has:

1. **Deep correction**: -25% to -40% from recent high
2. **Near major support**: 52-week low or strong historical support
3. **RSI oversold**: Below 30 (ideally below 25)
4. **Bullish reversal candle**: Hammer, Engulfing, Morning Star
5. **Volume confirmation**: High volume on reversal day
6. **RRR ≥ 2.5:1**: Risk small, reward large
7. **Fundamentals intact**: Business not broken, just sentiment

---

## KEY PRINCIPLES TO REMEMBER

| Principle | Application |
|-----------|-------------|
| "Buy strength, sell weakness" | Buy stocks showing relative strength |
| "Prior trend must exist" | No setup without preceding move |
| "S&R within 4% of stoploss" | Skip if support too far |
| "Volume must confirm" | Don't trust moves without volume |
| "RRR minimum 1.5" | Never take trades with poor RRR |
| "Deciding not to trade is a decision" | Patience is a strategy |
| "History repeats itself" | Patterns work because psychology doesn't change |

---

## DATA POINTS TO FETCH FOR ANALYSIS

When analyzing any stock, gather:

1. **Price Data**
   - Current price
   - 52-week high/low
   - Day change %

2. **Technical Indicators**
   - RSI (14-day)
   - MACD and signal line
   - MFI (Money Flow Index)

3. **Moving Averages**
   - 50-DMA
   - 200-DMA
   - Price position relative to MAs

4. **Support/Resistance**
   - Immediate support
   - Immediate resistance
   - Major support (52W low)
   - Major resistance (52W high)

5. **Volume**
   - Current volume
   - 10-day average volume
   - Volume trend

6. **Additional**
   - Beta (volatility)
   - Sector trend
   - Any news/events

---

## SOURCES

- Zerodha Varsity Technical Analysis Module: https://zerodha.com/varsity/module/technical-analysis/
- Trendlyne for technical data: https://trendlyne.com/
- TradingView for charts: https://tradingview.com/
- Investing.com for indicators: https://in.investing.com/

---

## HOW TO USE THIS FRAMEWORK

1. **Start analysis** by gathering all data points listed above
2. **Apply the 7-point checklist** systematically
3. **Fill out the trade setup template** for any potential trade
4. **Only execute** if ALL criteria pass
5. **Position size** using the 2% rule
6. **Maintain discipline** — skip trades that don't qualify

---

*Framework based on Zerodha Varsity Technical Analysis Module*
*Created: January 2026*
