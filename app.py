import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="MARKET INTEL v1.0", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .header { font-family: 'Roboto Mono', monospace; color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 20px; font-size: 24px; font-weight: bold; }
    .bull { color: #3fb950; border-left: 3px solid #3fb950; padding-left: 10px; margin-bottom: 10px; }
    .bear { color: #f85149; border-left: 3px solid #f85149; padding-left: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- LIVE DATA ENGINE ---
@st.cache_data(ttl=600) # Updates every 10 minutes
def get_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    # Get Live News Headlines
    news = stock.news[:4] # Get the 4 latest stories
    return info, news

st.markdown('<div class="header">█ MARKET INTEL // LIVE TERMINAL</div>', unsafe_allow_html=True)

user_input = st.text_input("ENTER TICKERS:", "AAPL, MSFT, NVDA").upper().replace(" ", "").split(",")

for t in user_input:
    try:
        info, news = get_data(t)
        st.markdown(f"### {t} : {info.get('longName', '')}")
        
        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        price = info.get('currentPrice', 0)
        change = info.get('regularMarketChangePercent', 0)
        m1.metric("PRICE", f"${price:.2f}", f"{change:+.2f}%")
        m2.metric("MKT CAP", f"${(info.get('marketCap', 0)/1e12):.2f}T")
        m3.metric("P/E RATIO", f"{info.get('trailingPE', 0):.1f}x")
        m4.metric("52W HIGH", f"${info.get('fiftyTwoWeekHigh', 0):.2f}")

        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.write("**AUTOMATED ANALYSIS**")
            # Simple logic to generate a "Case" based on data
            if change > 0:
                st.markdown(f'<div class="bull"><b>BULL CASE:</b> Momentum is positive. Stock is trading at {info.get("recommendationKey", "N/A").upper()} levels with strong buy-side volume.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bear"><b>BEAR CASE:</b> Short-term selling pressure detected. Watch support levels at ${info.get("twoHundredDayAverage", 0):.2f}.</div>', unsafe_allow_html=True)

        with col_right:
            st.write("**LIVE HEADLINES**")
            for article in news:
                st.markdown(f"• [{article['title']}]({article['link']})")
        
        st.divider()
    except:
        st.error(f"Could not fetch data for {t}")

st.markdown('<div style="text-align:center; color:#444;">[SYSTEM LIVE // DATA REFRESHED EVERY 10M]</div>', unsafe_allow_html=True)
