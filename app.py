import streamlit as st
import yfinance as yf
import pandas as pd

# 1. Page Setup
st.set_page_config(page_title="MARKET INTEL v1.0", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .header { font-family: 'Roboto Mono', monospace; color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 20px; font-size: 24px; font-weight: bold; }
    .bull { color: #3fb950; border-left: 3px solid #3fb950; padding-left: 10px; margin-bottom: 10px; }
    .bear { color: #f85149; border-left: 3px solid #f85149; padding-left: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">█ MARKET INTEL // LIVE TERMINAL</div>', unsafe_allow_html=True)

# 2. User Input
user_input = st.text_input("ENTER TICKERS (e.g. AAPL, TSLA, NVDA):", "AAPL, MSFT, NVDA").upper().replace(" ", "").split(",")

# 3. Data Processing
for t in user_input:
    if not t: continue
    
    try:
        stock = yf.Ticker(t)
        
        # Get Price Data (Using the most reliable method)
        hist = stock.history(period="2d")
        if hist.empty:
            st.error(f"Could not find data for {t}. Check the ticker symbol.")
            continue
            
        latest_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        change_pct = ((latest_price - prev_price) / prev_price) * 100
        
        st.markdown(f"### {t}")
        
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("LIVE PRICE", f"${latest_price:.2f}", f"{change_pct:+.2f}%")
        
        # Try to get extra info, but don't crash if it fails
        try:
            info = stock.info
            m2.metric("MKT CAP", f"${(info.get('marketCap', 0)/1e12):.2f}T")
            m3.metric("P/E RATIO", f"{info.get('trailingPE', 'N/A')}x")
        except:
            m2.metric("MKT CAP", "N/A")
            m3.metric("P/E RATIO", "N/A")

        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.write("**SENTIMENT ANALYSIS**")
            if change_pct > 0:
                st.markdown(f'<div class="bull"><b>BULLISH:</b> {t} is showing positive momentum today. Buying pressure is outweighing supply.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bear"><b>BEARISH:</b> {t} is facing selling pressure. Technical indicators suggest short-term caution.</div>', unsafe_allow_html=True)

        with col_right:
            st.write("**LIVE HEADLINES**")
            try:
                news = stock.news[:4]
                if not news:
                    st.write("No recent headlines found.")
                for article in news:
                    st.markdown(f"• [{article['title']}]({article['link']})")
            except:
                st.write("News feed temporarily unavailable.")
        
        st.divider()
        
    except Exception as e:
        st.error(f"System error on {t}. Yahoo Finance may be throttling requests.")

st.markdown('<div style="text-align:center; color:#444;">[SYSTEM ONLINE // DATA REFRESHED ON LOAD]</div>', unsafe_allow_html=True)
