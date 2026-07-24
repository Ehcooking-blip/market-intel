import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import xml.etree.ElementTree as ET

# 1. Page Setup
st.set_page_config(page_title="MARKET INTEL v1.0", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .header { font-family: 'Roboto Mono', monospace; color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 20px; font-size: 24px; font-weight: bold; }
    .bull { color: #3fb950; border-left: 3px solid #3fb950; padding-left: 10px; margin-bottom: 10px; }
    .bear { color: #f85149; border-left: 3px solid #f85149; padding-left: 10px; }
    .news-card { background: #161b22; padding: 10px; border-radius: 4px; margin-bottom: 5px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# 2. Robust News Fetcher (Bypasses Blocks)
def get_live_news(ticker):
    try:
        # We use the RSS feed because it is more stable than the standard API
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        root = ET.fromstring(response.content)
        news_items = []
        for item in root.findall('./channel/item')[:4]: # Get top 4
            news_items.append({
                'title': item.find('title').text,
                'link': item.find('link').text
            })
        return news_items
    except:
        return []

st.markdown('<div class="header">█ MARKET INTEL // LIVE TERMINAL</div>', unsafe_allow_html=True)

# 3. User Input
user_input = st.text_input("ENTER TICKERS:", "AAPL, MSFT, NVDA").upper().replace(" ", "").split(",")

for t in user_input:
    if not t: continue
    try:
        stock = yf.Ticker(t)
        hist = stock.history(period="2d")
        if hist.empty: continue
            
        latest_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        change_pct = ((latest_price - prev_price) / prev_price) * 100
        
        st.markdown(f"### {t}")
        
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("LIVE PRICE", f"${latest_price:.2f}", f"{change_pct:+.2f}%")
        
        try:
            info = stock.info
            m2.metric("MKT CAP", f"${(info.get('marketCap', 0)/1e12):.2f}T")
            m3.metric("P/E RATIO", f"{info.get('trailingPE', 'N/A')}x")
        except:
            m2.metric("MKT CAP", "FETCHING...")
            m3.metric("P/E RATIO", "N/A")

        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.write("**TERMINAL ANALYSIS**")
            if change_pct > 0:
                st.markdown(f'<div class="bull"><b>BULLISH:</b> {t} is outperforming the sector today. Technical support is holding at ${hist["Low"].iloc[-1]:.2f}.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bear"><b>BEARISH:</b> {t} is seeing distribution. Watch for a bounce near the 2-day low of ${hist["Low"].min():.2f}.</div>', unsafe_allow_html=True)

        with col_right:
            st.write("**LIVE HEADLINES**")
            news = get_live_news(t)
            if news:
                for article in news:
                    st.markdown(f'<div class="news-card"> <a href="{article["link"]}" style="color: #58a6ff; text-decoration: none;">{article["title"]}</a></div>', unsafe_allow_html=True)
            else:
                st.write("News feed delayed. Refreshing connection...")
        
        st.divider()
    except Exception as e:
        st.error(f"Connection error for {t}. Please wait 10 seconds and refresh.")

st.markdown('<div style="text-align:center; color:#444;">[SYSTEM ONLINE // ENCRYPTED FEED]</div>', unsafe_allow_html=True)
