# ⚡ Quantum Alpha AI — Indian Stock Market Dashboard

An AI-powered Indian stock market intelligence platform with real-time NSE/BSE prices, LSTM neural network predictions, technical analysis, and sentiment analysis — all in ₹ INR.

![Dashboard](https://img.shields.io/badge/Market-NSE%20%2F%20BSE-blue) ![Currency](https://img.shields.io/badge/Currency-%E2%82%B9%20INR-green) ![AI](https://img.shields.io/badge/AI-LSTM%20Neural%20Network-purple)

## 🚀 Features

- **📊 Live Dashboard** — Real-time ₹ INR prices fetched from NSE/BSE via Yahoo Finance
- **🤖 AI Price Prediction** — LSTM neural network trained on 2 years of price history; forecasts next 10 days
- **📈 Technical Analysis** — RSI, MACD, 50-day & 200-day moving averages with interactive charts
- **💬 News Sentiment** — Real-time news sentiment scoring (bullish / bearish / neutral)
- **🎯 AI Recommendation** — Combined BUY / SELL / HOLD signal with reasoning
- **📋 Watchlist** — Live watchlist for top Indian stocks
- **🌡️ Sector Heatmap** — Color-coded sector performance across IT, Banking, FMCG, Pharma, Energy, Metals, Telecom
- **💬 AI Chat Assistant** — Ask anything about Indian stocks

## 🇮🇳 Supported Indian Stocks

Just type any stock name — no `.NS` suffix needed:

`RELIANCE` `TCS` `HDFCBANK` `ICICIBANK` `INFY` `BHARTIARTL` `TATAMOTORS` `SBIN` `BAJFINANCE` `SUNPHARMA` `WIPRO` `MARUTI` `AXISBANK` `ITC` `ONGC` `HINDUNILVR` `NTPC` `CIPLA` `DRREDDY` and many more...

Experience the website here - https://quantum-alpha-ai.vercel.app/ 

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python `http.server` |
| Data | `yfinance` (Yahoo Finance NSE/BSE) |
| ML Model | TensorFlow/Keras LSTM |
| Indicators | `numpy`, `scikit-learn` |
| Sentiment | `textblob` |
| Frontend | Vanilla HTML/CSS/JS |
| Charts | Chart.js 4 + LightweightCharts |

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Maadhava-Reddy/quantum-alpha-ai.git
cd quantum-alpha-ai
```

### 2. Install dependencies
```bash
pip install yfinance tensorflow scikit-learn textblob numpy pandas requests
```

### 3. Run the server
```bash
python server.py
```

### 4. Open in browser
```
http://localhost:8000
```

## 📸 Screenshots

### Dashboard — Live ₹ INR Prices
- Current price, AI forecast, confidence %, sentiment, daily change, risk level
- Full price history chart

### Technical Analysis
- RSI chart (0–100 with overbought/oversold zones)
- Candlestick chart (1 month)
- Moving averages

### Sector Heatmap
- 9 sectors: IT Services, Banking, FMCG, Pharma, Energy, Finance, Metals, Telecom, Consumer
- Color-coded: green = bullish, red = bearish

## ⚙️ Configuration

The server auto-converts Indian stock names to Yahoo Finance NSE tickers:
- `RELIANCE` → `RELIANCE.NS`
- `TCS` → `TCS.NS`
- etc.

USD/INR exchange rate is fetched live at analysis time.

## 📄 License

MIT License — free to use and modify.

---

Built with ❤️ for the Indian stock market
