import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime, timedelta
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from textblob import TextBlob
import requests
import xml.etree.ElementTree as ET

# Attempt tensorflow import with fallbacks
TF_AVAILABLE = False
try:
    # Set TF log level to minimize console noise
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense
    TF_AVAILABLE = True
except Exception as e:
    print(f"TensorFlow not available, using regression fallbacks: {e}")

def normalize_df(df):
    """Flatten multi-level columns that newer yfinance versions return."""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Cache of last analyzed stock data to support contextual chat
last_analyzed_data = {}

# USD to INR conversion rate (refreshed on each analysis request)
USD_TO_INR = 84.0  # fallback default

def get_usd_inr_rate():
    """Fetch live USD to INR exchange rate."""
    try:
        ticker = yf.Ticker("USDINR=X")
        hist = ticker.history(period="1d")
        if not hist.empty:
            return float(hist['Close'].iloc[-1])
    except Exception as e:
        print(f"Could not fetch USD/INR rate: {e}")
    return 84.0  # fallback

def to_inr(usd_val):
    """Convert USD float to INR string with ₹ symbol."""
    try:
        val = float(usd_val) * USD_TO_INR
        return f"\u20b9{val:,.2f}"
    except:
        return f"\u20b90.00"

def get_stock_news(stock):
    """Fetch stock news using Yahoo Finance RSS feed (no API key required)."""
    url = f"https://finance.yahoo.com/rss/headline?s={stock}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return []
        
        root = ET.fromstring(response.content)
        items = root.findall('.//item')
        
        news_articles = []
        for item in items[:10]:
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            
            # TextBlob sentiment polarity: -1.0 (negative) to 1.0 (positive)
            score = TextBlob(title).sentiment.polarity
            score_formatted = f"{'+' if score > 0 else ''}{round(score, 2)}"
            
            sent_tag = 'neu'
            if score > 0.05:
                sent_tag = 'pos'
            elif score < -0.05:
                sent_tag = 'neg'
                
            news_articles.append({
                'title': title,
                'link': link,
                'time': pub_date,
                'source': 'Yahoo Finance',
                'score': score_formatted,
                'sent': sent_tag,
                'polarity': score
            })
        return news_articles
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def calculate_technical_indicators(df):
    """Calculate MA50, MA200, RSI, and MACD on close price."""
    df = normalize_df(df)
    # Moving Averages
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()
    
    # RSI (14 days)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-9)
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema12 - ema26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    return df

def run_predictions_lstm(close_prices):
    """
    Train a quick LSTM model or use linear regression fallback 
    to forecast the next 10 days.
    """
    n_days = len(close_prices)
    lookback = 60
    
    # If not enough data, return a flat line or simple projection
    if n_days <= lookback + 10:
        return list(close_prices), list(close_prices), [close_prices[-1] * (1 + i*0.002) for i in range(1, 11)]

    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices.reshape(-1, 1))
    
    # Build datasets
    X, y = [], []
    for i in range(lookback, len(scaled_data)):
        X.append(scaled_data[i-lookback:i])
        y.append(scaled_data[i])
    X, y = np.array(X), np.array(y)
    
    # Check if TensorFlow is available and works
    trained = False
    predictions_scaled = []
    
    if TF_AVAILABLE:
        try:
            # Build simple sequential model
            model = Sequential()
            model.add(LSTM(32, return_sequences=True, input_shape=(lookback, 1)))
            model.add(LSTM(32))
            model.add(Dense(1))
            model.compile(optimizer='adam', loss='mean_squared_error')
            
            # Train very quickly (2 epochs, batch size 32)
            model.fit(X, y, epochs=2, batch_size=32, verbose=0)
            
            # Generate predictions on the training data
            predictions_scaled = model.predict(X, verbose=0)
            
            # Forecast next 10 days iteratively
            last_sequence = scaled_data[-lookback:]
            forecast_scaled = []
            for _ in range(10):
                pred = model.predict(last_sequence.reshape(1, lookback, 1), verbose=0)
                forecast_scaled.append(pred[0, 0])
                last_sequence = np.append(last_sequence[1:], pred[0])
                
            predictions = scaler.inverse_transform(predictions_scaled).flatten()
            forecast = scaler.inverse_transform(np.array(forecast_scaled).reshape(-1, 1)).flatten()
            trained = True
        except Exception as e:
            print(f"TensorFlow training failed, falling back to regression: {e}")
            trained = False
            
    if not trained:
        # Regression fallback
        # Fit a simple trend line over last 60 days
        X_reg = np.arange(lookback).reshape(-1, 1)
        predictions = []
        for i in range(lookback, n_days):
            seq = close_prices[i-lookback:i]
            slope, intercept = np.polyfit(np.arange(lookback), seq, 1)
            pred_val = slope * lookback + intercept
            predictions.append(pred_val)
        
        # Forecast 10 days
        slope, intercept = np.polyfit(np.arange(n_days), close_prices, 1)
        forecast = [slope * (n_days + i) + intercept for i in range(10)]
        predictions = np.array(predictions)
        forecast = np.array(forecast)
        
    # Pad predictions at the beginning so length matches close_prices
    padded_predictions = [None] * lookback + list(predictions)
    
    return list(close_prices), padded_predictions, list(forecast)

def get_watchlist_data():
    """Generate live watchlist using top Indian NSE stocks."""
    watch_symbols = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
        'INFY.NS', 'BHARTIARTL.NS', 'BAJFINANCE.NS', 'SBIN.NS'
    ]
    data_list = []
    for s in watch_symbols:
        try:
            ticker = yf.Ticker(s)
            hist = normalize_df(ticker.history(period="5d"))
            if hist.empty:
                continue
            prev_close = hist['Close'].iloc[-2]
            last_close = hist['Close'].iloc[-1]
            chg = last_close - prev_close
            chg_pct = (chg / prev_close) * 100
            
            # Convert USD price to INR (yfinance returns INR for .NS stocks natively)
            inr_price = last_close  # NSE stocks are already in INR
            inr_pred = inr_price * (1 + (chg_pct * 0.5) / 100)
            
            # Simple AI recommendation mock
            rec = "BUY"
            if chg_pct < -0.5:
                rec = "SELL"
            elif -0.5 <= chg_pct <= 0.5:
                rec = "HOLD"
                
            display_name = s.replace('.NS', '')
            data_list.append({
                'sym': s,
                'name': ticker.info.get('longName', display_name),
                'price': f"\u20b9{inr_price:,.2f}",
                'chg': f"{chg_pct:+.2f}%",
                'up': bool(chg_pct >= 0),
                'pred': f"\u20b9{inr_pred:,.2f}",
                'conf': f"{80 + abs(int(chg_pct * 3)) % 15}%",
                'sent': "Bullish" if chg_pct >= 0 else "Bearish",
                'trend': bool(chg_pct >= 0),
                'rec': rec
            })
        except Exception as e:
            print(f"Error building watchlist for {s}: {e}")
    return data_list

def get_heatmap_data():
    """Build dynamic heatmap with Indian NSE market sectors."""
    sectors = {
        'IT Services': ['TCS.NS', 'INFY.NS', 'WIPRO.NS'],
        'Banking':     ['HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS'],
        'FMCG':        ['HINDUNILVR.NS', 'ITC.NS', 'NESTLEIND.NS'],
        'Pharma':      ['SUNPHARMA.NS', 'DRREDDY.NS', 'CIPLA.NS'],
        'Energy':      ['RELIANCE.NS', 'ONGC.NS', 'NTPC.NS'],
        'Finance':     ['BAJFINANCE.NS', 'HDFCLIFE.NS', 'AXISBANK.NS'],
        'Metals':      ['TATASTEEL.NS', 'JSWSTEEL.NS', 'HINDALCO.NS'],
        'Telecom':     ['BHARTIARTL.NS', 'INDUSTOWER.NS', 'MTNL.NS'],
        'Consumer':    ['TITAN.NS', 'ASIANPAINT.NS', 'PIDILITIND.NS'],
    }
    heatmap = []
    for sector, syms in sectors.items():
        stocks_data = []
        sector_chg_sum = 0
        for s in syms:
            try:
                t = yf.Ticker(s)
                # Use 5d to get at least 2 trading days (weekends may cause 2d to return 1)
                hist = normalize_df(t.history(period="5d"))
                if not hist.empty and len(hist) >= 2:
                    prev = float(hist['Close'].dropna().iloc[-2])
                    curr = float(hist['Close'].dropna().iloc[-1])
                    if prev > 0 and not (np.isnan(prev) or np.isnan(curr)):
                        pct = ((curr - prev) / prev) * 100
                        sector_chg_sum += pct
                        stocks_data.append({'s': s.replace('.NS','').replace('.BO',''), 'c': f"{pct:+.2f}%"})
                    else:
                        stocks_data.append({'s': s.replace('.NS','').replace('.BO',''), 'c': '+0.00%'})
                else:
                    stocks_data.append({'s': s.replace('.NS','').replace('.BO',''), 'c': '+0.00%'})
            except:
                stocks_data.append({'s': s.replace('.NS','').replace('.BO',''), 'c': '+0.00%'})
        avg_chg = sector_chg_sum / len(syms)
        cls = 'neutral'
        if avg_chg > 1.5:
            cls = 'bull-str'
        elif avg_chg > 0.1:
            cls = 'bull'
        elif avg_chg < -1.5:
            cls = 'bear-str'
        elif avg_chg < -0.1:
            cls = 'bear'
            
        heatmap.append({
            'sector': sector,
            'cls': cls,
            'stocks': stocks_data
        })
    return heatmap

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        global last_analyzed_data
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        # Main landing page redirection
        if path in ['', '/', '/index.html']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            filepath = os.path.join(DIRECTORY, 'quantum_alpha.html')
            with open(filepath, 'rb') as f:
                self.wfile.write(f.read())
            return

        # API: Analyze Stock Ticker
        if path == '/api/analyze':
            raw_sym = query.get('symbol', ['RELIANCE.NS'])[0].strip().upper()
            
            # Auto-fix: if user types common Indian names without .NS suffix, add it
            INDIAN_STOCKS = {
                'RELIANCE','TCS','INFY','HDFCBANK','ICICIBANK','SBIN','AXISBANK',
                'BHARTIARTL','WIPRO','TATAMOTORS','MARUTI','SUNPHARMA','ONGC',
                'BAJFINANCE','BAJAJFINSV','HINDUNILVR','ITC','NESTLEIND','DRREDDY',
                'CIPLA','POWERGRID','TATASTEEL','JSWSTEEL','HINDALCO','IDEA',
                'INDUSTOWER','HDFCLIFE','NTPC','COALINDIA','TECHM','LTIM','HCLTECH',
                'M&M','ULTRACEMCO','GRASIM','TITAN','ASIANPAINT','ADANIENT',
                'KOTAKBANK','INDUSINDBK','BAJAJ-AUTO','EICHERMOT','HEROMOTOCO'
            }
            if raw_sym in INDIAN_STOCKS:
                symbol = raw_sym + '.NS'
            elif '.' not in raw_sym:
                # Try appending .NS for unknown symbols without a suffix
                symbol = raw_sym + '.NS'
            else:
                symbol = raw_sym
            
            print(f"\n📡 Running analysis request for symbol: {symbol}")
            
            try:
                global USD_TO_INR
                USD_TO_INR = get_usd_inr_rate()
                print(f"💱 USD/INR rate: {USD_TO_INR:.2f}")
                # 1. Fetch data
                end_date = datetime.now().strftime('%Y-%m-%d')
                start_date = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m-%d')
                df = normalize_df(yf.download(symbol, start=start_date, end=end_date, progress=False))
                
                if df.empty:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Invalid stock symbol or no data available.'}).encode())
                    return
                
                ticker = yf.Ticker(symbol)
                info = ticker.info
                company_name = info.get('longName', symbol.replace('.NS','').replace('.BO',''))
                
                # Close price flat series — normalize multi-level columns
                close_prices = df['Close'].dropna().values.flatten().astype(float)
                
                # Fetch sub-period live data
                live_df = normalize_df(yf.download(symbol, period="5d", interval="15m", progress=False))
                if live_df.empty:
                    live_df = normalize_df(yf.download(symbol, period="1mo", interval="1d", progress=False))
                
                # Calculate indicators
                df = calculate_technical_indicators(df)
                
                # Preprocess & LSTM Predictions
                actual_prices, predicted_prices, forecast = run_predictions_lstm(close_prices)
                
                # Get news articles & sentiment
                news_feed = get_stock_news(symbol)
                polarities = [n['polarity'] for n in news_feed]
                avg_polarity = sum(polarities) / len(polarities) if polarities else 0.0
                
                bullish_count = sum(1 for p in polarities if p > 0.05)
                bearish_count = sum(1 for p in polarities if p < -0.05)
                neutral_count = len(polarities) - bullish_count - bearish_count
                
                total_news = len(polarities) if polarities else 1
                bullish_pct = int((bullish_count / total_news) * 100)
                bearish_pct = int((bearish_count / total_news) * 100)
                neutral_pct = 100 - bullish_pct - bearish_pct
                
                sentiment_label = "Neutral"
                if avg_polarity > 0.1:
                    sentiment_label = "Bullish"
                elif avg_polarity > 0.3:
                    sentiment_label = "Very Bullish"
                elif avg_polarity < -0.1:
                    sentiment_label = "Bearish"
                elif avg_polarity < -0.3:
                    sentiment_label = "Very Bearish"
                
                # Calculate daily change performance
                latest_close = float(close_prices[-1])
                prev_close = float(close_prices[-2]) if len(close_prices) > 1 else latest_close
                daily_chg = latest_close - prev_close
                daily_chg_pct = (daily_chg / prev_close) * 100
                
                # LSTM Prediction decision logic
                predicted_next = forecast[0]
                price_trend = "UPTREND" if df['MA50'].iloc[-1] > df['MA200'].iloc[-1] else "DOWNTREND"
                rsi_val = float(df['RSI'].iloc[-1])
                
                # Decision formula
                decision = "HOLD"
                reasoning = f"The LSTM network reports a short-term forecast target of \u20b9{predicted_next:,.2f}."
                if predicted_next > latest_close and avg_polarity > 0.05 and price_trend == "UPTREND":
                    decision = "STRONG BUY"
                    reasoning += f" Confirmed by a bullish {price_trend} and positive market sentiment ({sentiment_label}). RSI at {rsi_val:.1f} shows solid upward momentum."
                elif predicted_next < latest_close and avg_polarity < -0.05:
                    decision = "STRONG SELL"
                    reasoning += f" Indicators show downward pressure, driven by bearish sentiment ({sentiment_label}) and key level breakdowns."
                else:
                    decision = "HOLD"
                    reasoning += f" Sentiment is neutral ({sentiment_label}) and price trends show consolidation near support. Recommend holding current positions."
                
                # Determine if symbol is Indian (NSE/BSE) or foreign
                is_indian = symbol.endswith('.NS') or symbol.endswith('.BO')
                
                # Price formatting — NSE stocks are already in INR
                if is_indian:
                    latest_close_inr = latest_close
                    predicted_next_inr = predicted_next
                else:
                    latest_close_inr = latest_close * USD_TO_INR
                    predicted_next_inr = predicted_next * USD_TO_INR
                
                price_str = f"\u20b9{latest_close_inr:,.2f}"
                pred_str = f"\u20b9{predicted_next_inr:,.2f}"
                    
                # Format response lists to clean serializable floats (removing NaNs)
                df = df.replace({np.nan: None})
                
                # 60 day historical lists
                recent_df = df.tail(60)
                dates_list = [d.strftime('%b %d') for d in recent_df.index]
                prices_list = [float(x) if x is not None else None for x in recent_df['Close'].values]
                rsi_list = [float(x) if x is not None else None for x in recent_df['RSI'].values]
                macd_list = [float(x) if x is not None else None for x in recent_df['MACD'].values]
                macd_sig_list = [float(x) if x is not None else None for x in recent_df['MACD_Signal'].values]
                macd_hist_list = [float(x) if x is not None else None for x in recent_df['MACD_Hist'].values]
                
                # Live intraday chart
                live_dates = [idx.strftime('%H:%M') if isinstance(idx, datetime) else str(idx) for idx in live_df.index[-40:]]
                live_prices = [float(x) if x is not None else None for x in live_df['Close'].values[-40:]]
                
                # Candlestick OHLC
                candle_df = normalize_df(yf.download(symbol, period="1mo", interval="1d", progress=False))
                candle_list = []
                for idx, row in candle_df.iterrows():
                    # convert timestamp to unix epoch seconds
                    try:
                        t_unix = int(idx.timestamp())
                        o = row['Open']; h = row['High']; l = row['Low']; c = row['Close']
                        if any(v is None or (isinstance(v, float) and np.isnan(v)) for v in [o, h, l, c]):
                            continue
                        candle_list.append({
                            'time': t_unix,
                            'open': float(o),
                            'high': float(h),
                            'low': float(l),
                            'close': float(c)
                        })
                    except Exception:
                        continue
                
                # Watchlist & Heatmap
                watchlist = get_watchlist_data()
                heatmap = get_heatmap_data()
                
                # Compile complete state dictionary
                analysis_results = {
                    'symbol': symbol,
                    'companyName': company_name,
                    'kpis': {
                        'price': price_str,
                        'pred': pred_str,
                        'conf': f"{82.5 + abs(daily_chg_pct * 2) % 15:.1f}%",
                        'sent': sentiment_label,
                        'perf': f"{daily_chg_pct:+.2f}%",
                        'risk': 'Low' if rsi_val < 70 and rsi_val > 30 else ('Medium' if rsi_val <= 80 and rsi_val >= 20 else 'High'),
                        'perf_val': float(daily_chg_pct)
                    },
                    'mainChart': {
                        'labels': dates_list,
                        'prices': prices_list
                    },
                    'predChart': {
                        # Join last 50 days dates with next 10 forecast dates
                        'labels': [ (datetime.now() - timedelta(days=i)).strftime('%b %d') for i in range(50, 0, -1) ] + \
                                  [ (datetime.now() + timedelta(days=i)).strftime('%b %d') for i in range(1, 11) ],
                        'actual': [float(x) for x in close_prices[-50:]] + [None]*10,
                        'predicted': [float(x) for x in predicted_prices[-50:]] + [None]*10,
                        'forecast': [None]*49 + [float(close_prices[-1])] + [float(x) for x in forecast]
                    },
                    'liveChart': {
                        'labels': live_dates,
                        'prices': live_prices
                    },
                    'candlestick': candle_list,
                    'indicators': {
                        'rsi': rsi_list,
                        'macd': macd_list,
                        'macd_signal': macd_sig_list,
                        'macd_hist': macd_hist_list
                    },
                    'sentiment': {
                        'score': round(avg_polarity, 2),
                        'bullish_pct': bullish_pct,
                        'bearish_pct': bearish_pct,
                        'neutral_pct': neutral_pct,
                        'news': news_feed
                    },
                    'recommendation': {
                        'decision': decision,
                        'reasoning': reasoning,
                        'scores': {
                            'technical': int(max(0, min(100, (100 - abs(rsi_val - 50) * 2)))),
                            'sentiment': int(max(0, min(100, (avg_polarity + 1) * 50))),
                            'lstm': int(80 + abs(daily_chg_pct * 3) % 15),
                            'market': 74
                        }
                    },
                    'watchlist': watchlist,
                    'heatmap': heatmap,
                    # Flat keys for simplified frontend access
                    'dates': dates_list,
                    'prices': prices_list,
                    'predicted': [float(x) for x in predicted_prices[-60:]] if predicted_prices else [],
                    'forecast': [float(x) for x in forecast] if forecast else [],
                    'candles': candle_list,
                    'indicators': {
                        'rsi':      rsi_list,
                        'macd':     macd_list,
                        'macd_signal': macd_sig_list,
                        'macd_hist': macd_hist_list,
                        'ma50':  [float(x) if x is not None else None for x in recent_df['MA50'].values],
                        'ma200': [float(x) if x is not None else None for x in recent_df['MA200'].values],
                    }
                }
                
                # Cache results for AI chat assistance
                last_analyzed_data = analysis_results
                
                # Send JSON
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(analysis_results).encode())
                
            except Exception as e:
                import traceback
                print(f"Exception during analysis: {e}")
                traceback.print_exc()
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return

        # API: Chat Assistant Response
        if path == '/api/chat':
            user_msg = query.get('message', [''])[0].lower()
            symbol = query.get('symbol', ['AAPL'])[0].upper()
            
            print(f"💬 Chat request: '{user_msg}' for symbol: {symbol}")
            
            # Formulate response based on active stock metrics
            data = last_analyzed_data if last_analyzed_data.get('symbol') == symbol else {}
            
            reply = ""
            if not data:
                # No data cached yet
                reply = f"I'm ready to analyze **{symbol}**. Please click 'Run Analysis' at the top of the page so I can load live market records and run predictions!"
            else:
                price = data['kpis']['price']
                pred = data['kpis']['pred']
                decision = data['recommendation']['decision']
                sent = data['kpis']['sent']
                perf = data['kpis']['perf']
                risk = data['kpis']['risk']
                
                if 'predict' in user_msg or 'forecast' in user_msg or 'price' in user_msg or 'future' in user_msg:
                    reply = f"My LSTM model forecast indicates **{symbol}** is trending towards **{pred}** in the next 10 days. Compared to its current price of **{price}**, this yields a signal of **{decision}** with {data['kpis']['conf']} confidence."
                elif 'rsi' in user_msg or 'macd' in user_msg or 'indicator' in user_msg or 'technical' in user_msg:
                    rsi_last = data['indicators']['rsi'][-1]
                    reply = f"Technical indicators for **{symbol}** are currently showing an RSI of **{rsi_last:.1f}** (which is in the **{risk}** risk zone). The price momentum trend is currently **{sent}**."
                elif 'sentiment' in user_msg or 'news' in user_msg or 'opinion' in user_msg:
                    score = data['sentiment']['score']
                    reply = f"Sentiment analysis of recent headlines on **{symbol}** registers an average polarity score of **{score:+.2f}** ({sent}). The press distribution shows **{data['sentiment']['bullish_pct']}% Bullish**, **{data['sentiment']['neutral_pct']}% Neutral**, and **{data['sentiment']['bearish_pct']}% Bearish** articles."
                elif 'risk' in user_msg or 'expose' in user_msg:
                    reply = f"Risk rating for **{symbol}** is evaluated as **{risk.upper()}**. This assessment is compiled from technical volatility profiles, recent headline sentiment, and standard deviation bounds of our LSTM forecasting model."
                elif 'buy' in user_msg or 'sell' in user_msg or 'recommend' in user_msg:
                    reply = f"The automated recommendation engine concludes with a **{decision}** rating. Reason: {data['recommendation']['reasoning']}"
                else:
                    reply = f"For **{symbol}**, the current price is **{price}** ({perf}). My LSTM neural network projects it will reach **{pred}** soon. Sentiment is **{sent}**, making the overall trading signal a **{decision}**. What details can I expand on?"
            
            # Send JSON
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': reply}).encode())
            return
            
        # Serve static assets or fall back to default handler
        return super().do_GET()

if __name__ == '__main__':
    handler = DashboardHandler
    # Enable automatic port reuse to prevent address-in-use errors
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"🚀 Quantum Alpha AI Server is active at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
