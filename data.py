import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import plotly.graph_objects as go
from newsapi import NewsApiClient
from textblob import TextBlob

# ================= INPUT =================
stock = input("Enter ANY stock symbol (e.g., AAPL, RELIANCE.NS): ").upper()

# ================= DATA =================
data = yf.download(stock, start="2015-01-01", end="2024-01-01")

if data.empty:
    print("❌ Invalid stock symbol")
    exit()

# Company Info
ticker = yf.Ticker(stock)
info = ticker.info
print("\n🏢 Company Name:", info.get("longName", "Not Available"))

# ================= TECHNICAL INDICATORS =================

# Moving Averages
data['MA50'] = data['Close'].rolling(window=50).mean()
data['MA200'] = data['Close'].rolling(window=200).mean()

# RSI
delta = data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

print("\n📊 Technical Indicators (Latest):")
print(data[['Close', 'MA50', 'MA200', 'RSI']].tail())

# ================= PREPROCESSING =================
close_data = data[['Close']]

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(close_data)

X, y = [], []

for i in range(60, len(scaled_data)):
    X.append(scaled_data[i-60:i])
    y.append(scaled_data[i])

X, y = np.array(X), np.array(y)

# Split
train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# ================= MODEL =================
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)))
model.add(LSTM(50))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

print("\n🤖 Training AI Model...")
model.fit(X_train, y_train, epochs=5, batch_size=32)

# ================= PREDICTION =================
predictions = model.predict(X_test)

last_actual = y_test[-1][0]
last_predicted = predictions[-1][0]

# Convert back to original scale
predictions = scaler.inverse_transform(predictions)
y_test = scaler.inverse_transform(y_test)

print("\n================ ANALYSIS ================\n")
print("📈 Last Actual Price:", y_test[-1][0])
print("🤖 Last Predicted Price:", predictions[-1][0])

# ================= GRAPH =================
fig = go.Figure()

fig.add_trace(go.Scatter(
    y=y_test.flatten(),
    mode='lines',
    name="Actual Price",
    line=dict(color='blue', width=2)
))

fig.add_trace(go.Scatter(
    y=predictions.flatten(),
    mode='lines',
    name="Predicted Price",
    line=dict(color='red', dash='dash', width=2)
))

fig.update_layout(
    title=f"{stock} Stock Price Prediction",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark"
)

fig.show()
fig.write_html("stock_prediction.html")

# ================= NEWS + SENTIMENT =================
newsapi = NewsApiClient(api_key="76228afdf342440f83194805f7f71f42") 

articles = newsapi.get_everything(q=stock, language='en', page_size=5)

print("\n📰 Latest News:\n")

sentiments = []

for article in articles['articles']:
    title = article['title']
    print("-", title)

    score = TextBlob(title).sentiment.polarity
    sentiments.append(score)

avg_sentiment = sum(sentiments)/len(sentiments) if sentiments else 0

print("\n📊 Average News Sentiment:", avg_sentiment)

# ================= FINAL DECISION =================

# Trend
if data['MA50'].iloc[-1] > data['MA200'].iloc[-1]:
    trend = "UPTREND 📈"
else:
    trend = "DOWNTREND 📉"

# RSI
rsi = data['RSI'].iloc[-1]

print("\n🎯 FINAL DECISION\n")
print("Trend:", trend)
print("RSI:", round(rsi,2))
print("Sentiment:", avg_sentiment)

if (predictions[-1][0] > y_test[-1][0]) and (avg_sentiment > 0) and ("UPTREND" in trend):
    print("👉 STRONG BUY 🚀")
elif (predictions[-1][0] < y_test[-1][0]) and (avg_sentiment < 0):
    print("👉 STRONG SELL ⚠️")
else:
    print("👉 HOLD 🤝")

# ================= END =================
input("\nPress Enter to exit...")