import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import plotly.graph_objects as go
from textblob import TextBlob
from newsapi import NewsApiClient
from datetime import datetime, timedelta

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

# ================= SIDEBAR =================
st.sidebar.title("⚙️ Settings")
stock = st.sidebar.text_input("Enter Stock Symbol", "AAPL")
analyze = st.sidebar.button("Analyze Stock")

# ================= MAIN TITLE =================
st.title("📊 AI Stock Market Dashboard")
st.markdown("### Smart Prediction • Sentiment • Decision System")

if analyze:

    with st.spinner("Fetching data and training model... ⏳"):

        # ================= DATA =================
        data = yf.download(stock, start="2015-01-01", end="2024-01-01")

        if data.empty:
            st.error("❌ Invalid stock symbol")
            st.stop()

        ticker = yf.Ticker(stock)
        info = ticker.info

        # ================= COMPANY =================
        st.subheader("🏢 Company Information")
        st.write(info.get("longName", "Not Available"))

        # ================= LIVE DATA =================
        st.subheader("📡 Live Market Data")

        try:
            live_data = yf.download(stock, period="5d", interval="15m")

            if live_data.empty:
                live_data = yf.download(stock, period="1mo", interval="1d")

        except:
            live_data = pd.DataFrame()

        if not live_data.empty:
            fig_live = go.Figure()

            fig_live.add_trace(go.Scatter(
                x=live_data.index,
                y=live_data['Close'],
                mode='lines',
                name="Live Price",
                line=dict(color='green')
            ))

            fig_live.update_layout(template="plotly_dark")
            st.plotly_chart(fig_live, use_container_width=True)
        else:
            st.warning("⚠️ Live data not available")

        # ================= CANDLESTICK =================
        st.subheader("🕯️ Candlestick Chart")

        try:
            candle_data = yf.download(stock, period="1mo", interval="1d")
        except:
            candle_data = pd.DataFrame()

        if not candle_data.empty:
            fig_candle = go.Figure(data=[go.Candlestick(
                x=candle_data.index,
                open=candle_data['Open'],
                high=candle_data['High'],
                low=candle_data['Low'],
                close=candle_data['Close']
            )])

            fig_candle.update_layout(template="plotly_dark")
            st.plotly_chart(fig_candle, use_container_width=True)
        else:
            st.warning("⚠️ Candlestick data not available")

        # ================= INDICATORS =================
        data['MA50'] = data['Close'].rolling(window=50).mean()
        data['MA200'] = data['Close'].rolling(window=200).mean()

        # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))

        # ================= PREPROCESS =================
        close_data = data[['Close']]
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(close_data)

        X, y = [], []
        for i in range(60, len(scaled_data)):
            X.append(scaled_data[i-60:i])
            y.append(scaled_data[i])

        X, y = np.array(X), np.array(y)

        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        # ================= MODEL =================
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)))
        model.add(LSTM(50))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X_train, y_train, epochs=3, batch_size=32, verbose=0)

        predictions = model.predict(X_test)

        predictions = scaler.inverse_transform(predictions)
        y_test = scaler.inverse_transform(y_test)

        last_actual = y_test[-1][0]
        last_predicted = predictions[-1][0]

    # ================= METRICS =================
    st.subheader("📊 Key Metrics")

    col1, col2 = st.columns(2)
    col1.metric("📈 Last Actual Price", f"{last_actual:.2f}")
    col2.metric("🤖 Predicted Price", f"{last_predicted:.2f}")

    # ================= PREDICTION GRAPH =================
    st.subheader("📉 Stock Prediction Chart")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=y_test.flatten(),
        name="Actual Price",
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        y=predictions.flatten(),
        name="Predicted Price",
        line=dict(color='red', dash='dash')
    ))

    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # ================= RSI GRAPH =================
    st.subheader("📊 RSI Indicator")

    fig_rsi = go.Figure()

    fig_rsi.add_trace(go.Scatter(
        y=data['RSI'],
        name="RSI",
        line=dict(color='orange')
    ))

    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")

    fig_rsi.update_layout(template="plotly_dark")
    st.plotly_chart(fig_rsi, use_container_width=True)

    # ================= NEWS (DAILY FIX) =================
    st.subheader("📰 Today's Market News")

    newsapi = NewsApiClient(api_key="pub_7371b21e388c47b291684ba5be5bd0e7")  

    today = datetime.now()
    yesterday = today - timedelta(days=1)

    query = f"{stock} stock market"

    articles = newsapi.get_everything(
        q=query,
        from_param=yesterday.strftime('%Y-%m-%d'),
        to=today.strftime('%Y-%m-%d'),
        language='en',
        sort_by='publishedAt',
        page_size=10
    )

    sentiments = []

    if not articles['articles']:
        st.warning("⚠️ No latest news available")
    else:
        for article in articles['articles']:

            title = article['title']
            source = article['source']['name']

            st.markdown(f"### 📰 {title}")
            st.write(f"Source: {source}")

            score = TextBlob(title).sentiment.polarity
            sentiments.append(score)

            if score > 0:
                st.success("Positive News 📈")
            elif score < 0:
                st.error("Negative News 📉")
            else:
                st.warning("Neutral News 🤝")

    avg_sentiment = sum(sentiments)/len(sentiments) if sentiments else 0
    st.write("📊 Average Sentiment:", round(avg_sentiment, 2))

    # ================= FINAL DECISION =================
    st.subheader("🎯 AI Recommendation")

    if last_predicted > last_actual and avg_sentiment > 0:
        st.success("🚀 STRONG BUY")
    elif last_predicted < last_actual and avg_sentiment < 0:
        st.error("⚠️ STRONG SELL")
    else:
        st.warning("🤝 HOLD")