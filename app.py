import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="MARKET INTEL v1.0", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Roboto+Mono&display=swap');
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .header { font-family: 'Roboto Mono', monospace; color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; margin-bottom: 20px; font-size: 24px; font-weight: bold; }
    .bull { color: #3fb950; border-left: 3px solid #3fb950; padding-left: 10px; }
    .bear { color: #f85149; border-left: 3px solid #f85149; padding-left: 10px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def fetch_market_data(tickers):
    results = {}
    for t in tickers:
        try:
            s = yf.Ticker(t)
            info = s.info
            results[t] = {
                "Price": info.get("currentPrice", 0),
                "Change": info.get("regularMarketChangePercent", 0),
                "MCap": info.get("marketCap", 0) / 1e12,
                "PE": info.get("trailingPE", 0),
                "Rev": info.get("revenueGrowth", 0) * 100
            }
        except: pass
    return results

INTELLIGENCE = {
    "AAPL": {"Rating": "BULLISH", "News": ["iPhone 17 Pro demand spikes", "Services revenue hits 28%"], "Bull": "AI-driven upgrade cycle provides tailwinds.", "Bear": "Regulatory pressure on App Store remains high."},
    "MSFT": {"Rating": "NEUTRAL", "News": ["$190B CapEx guidance weighed", "Azure AI growth stabilizes"], "Bull": "Enterprise dominance with Copilot.", "Bear": "High infrastructure spend compressing margins."},
    "NVDA": {"Rating": "BULLISH", "News": ["Blackwell chip yields hit 95%", "Rubin GPU architecture announced"], "Bull": "Data center demand outpaces supply.", "Bear": "Heightened export controls on silicon."}
}

st.markdown('<div class="header">█ MARKET INTEL // TERMINAL v1.0</div>', unsafe_allow_html=True)
input_tickers = st.text_input("ENTER TICKERS:", "AAPL, MSFT, NVDA").upper().replace(" ", "").split(",")

if input_tickers:
    data = fetch_market_data(input_tickers)
    for t in input_tickers:
        if t in data:
            d = data[t]
            st.markdown(f"### {t}")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("PRICE", f"${d['Price']:.2f}", f"{d['Change']:+.2f}%")
            m2.metric("MKT CAP", f"${d['MCap']:.2f}T")
            m3.metric("P/E", f"{d['PE']:.1f}x")
            m4.metric("REV GROWTH", f"{d['Rev']:.1f}%")
            col_a, col_b = st.columns([2, 1])
            with col_a:
                intel = INTELLIGENCE.get(t, {"Rating": "N/A", "Bull": "Generating...", "Bear": "Generating..."})
                st.write(f"**SENTIMENT: {intel['Rating']}**")
                st.markdown(f'<div class="bull"><b>BULL CASE:</b> {intel["Bull"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="bear"><b>BEAR CASE:</b> {intel["Bear"]}</div>', unsafe_allow_html=True)
            with col_b:
                st.write("**BLOOMBERG HIGHLIGHTS**")
                news_list = INTELLIGENCE.get(t, {"News": ["No recent alerts"]})["News"]
                for n in news_list: st.markdown(f"• <small>{n}</small>", unsafe_allow_html=True)
            st.divider()
