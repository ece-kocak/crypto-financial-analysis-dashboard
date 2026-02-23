import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Crypto Tracker", layout="wide")

st.title("Crypto Dashboard")



@st.cache_data(ttl=3600)
def get_top_20_coins():
    """Fetch top 20 cryptocurrencies by market cap."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {coin["name"]: coin["id"] for coin in data}
    except Exception as e:
        st.error(f"API Error: {e}")
    
    return {"Bitcoin": "bitcoin", "Ethereum": "ethereum"}


@st.cache_data(ttl=600)
def fetch_crypto_data(coin_id, days):
    """Fetch historical price data."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
    return None



coin_options = get_top_20_coins()
coin_names = list(coin_options.keys())

selected_coin_name = st.selectbox(
    "Select a Coin",
    ["Select..."] + coin_names + ["Other"]
)

selected_coin = None

if selected_coin_name == "Other":
    custom_coin = st.text_input("Enter coin name. (ex: dogecoin)")
    if custom_coin:
        selected_coin = custom_coin.lower()
elif selected_coin_name != "Select...":
    selected_coin = coin_options[selected_coin_name]



st.markdown("###  Time Range")

col1, col2, col3, col4 = st.columns(4)

if "selected_days" not in st.session_state:
    st.session_state.selected_days = None

with col1:
    if st.button("1D"):
        st.session_state.selected_days = "1"
with col2:
    if st.button("7D"):
        st.session_state.selected_days = "7"
with col3:
    if st.button("1M"):
        st.session_state.selected_days = "30"
with col4:
    if st.button("1Y"):
        st.session_state.selected_days = "365"

selected_days = st.session_state.selected_days




if selected_coin and selected_days:
    data = fetch_crypto_data(selected_coin, selected_days)

    if data and "prices" in data:
        df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
        df["date"] = pd.to_datetime(df["timestamp"], unit="ms")

# Moving Average ORT.LAR
        df["MA20"] = df["price"].rolling(window=20).mean()
        df["MA50"] = df["price"].rolling(window=50).mean()

        st.markdown("### 📊 Indicators")
        col_ma1, col_ma2 = st.columns(2)

        with col_ma1:
            show_ma20 = st.toggle("MA20")
        with col_ma2:
            show_ma50 = st.toggle("MA50")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["date"],
            y=df["price"],
            mode="lines",
            name="Price",
            line=dict(color="#00ff00")
        ))

        if show_ma20:
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df["MA20"],
                mode="lines",
                name="MA20",
                line=dict(color="#ff9900")
            ))

        if show_ma50:
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df["MA50"],
                mode="lines",
                name="MA50",
                line=dict(color="#F815F8")
            ))

        fig.update_layout(
            template="plotly_dark",
            height=600,
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            margin=dict(l=0, r=0, t=30, b=0)
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Unable to fetch data. The coin ID might be invalid or API rate limit exceeded.")

elif selected_coin is None and selected_coin_name == "Other":
    st.info("Please enter a coin.")
elif selected_days is None:
    st.info("Please select a time range.")
