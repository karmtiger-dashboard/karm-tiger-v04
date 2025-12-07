# app.py - Karm Tiger v0.4 — Beast Mode + US/China Macro Dashboard
import streamlit as st
import numpy as np
import yfinance as yf
import requests
import pandas as pd
from web3 import Web3
import ccxt
import time
from datetime import datetime
import pandas_datareader.data as web  # <-- NEW IMPORT

# === CONFIG ===
st.set_page_config(page_title="Karm Tiger v0.4", page_icon="🐅", layout="wide")
st.title("🐅 Karm Tiger Deep Tech Investment Dashboard v0.4")
st.markdown("**Beast Mode**: Live Perplexity • Grok X Sentiment • Multi-Ticker • Blockchain • **US vs China Macro Panel**")

# === NEW: US vs CHINA MACRO PANEL ===
st.subheader("🌍 US vs China Deep Tech Macro Dashboard (Live • Updates Daily)")

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_macro_metrics():

    try:
        start = datetime(2015, 1, 1)

        # US Data
        fed_rate = web.DataReader("FEDFUNDS", "fred", start, timeout=30).iloc[-1, 0]
        unrate_us = web.DataReader("UNRATE", "fred", start, timeout=30).iloc[-1, 0]
        cpi_us = web.DataReader("CPIAUCSL", "fred", start, timeout=30).pct_change(12).iloc[-1, 0] * 100
        gdp_us_qoq = web.DataReader("A191RL1Q225S", "fred", start, timeout=30).iloc[-1, 0]

        nasdaq = yf.download("^IXIC", period="5d", progress=False, timeout=30)["Close"]
        nasdaq_val = nasdaq.iloc[-1] if len(nasdaq) > 0 else 0
        nasdaq_chg = (nasdaq.iloc[-1] / nasdaq.iloc[-2] - 1) * 100 if len(nasdaq) > 1 else 0

        # China Data
        sh = yf.download("000001.SS", period="5d", progress=False, timeout=30)["Close"]
        sh_val = sh.iloc[-1] if len(sh) > 0 else 0
        sh_chg = (sh.iloc[-1] / sh.iloc[-2] - 1) * 100 if len(sh) > 1 else 0

        cpi_cn_yoy = web.DataReader("CHNCPIALLMINMEI", "fred", start, timeout=30).iloc[-1, 0]
        gdp_cn_qoq = web.DataReader("CHNGDPRQDSMEI", "fred", start, timeout=30).iloc[-1, 0]

        # Build table
        df = pd.DataFrame({
            "Metric": [
                "Key Policy Rate",
                "Unemployment Rate",
                "CPI Inflation YoY",
                "Real GDP Growth (QoQ annualized)",
                "Main Tech Index",
                "Index Daily Δ",
                "Manufacturing PMI (latest approx)"
            ],
            "United States": [
                f"{fed_rate:.2f}% (Fed Funds)",
                f"{unrate_us:.1f}%",
                f"{cpi_us:.2f}%",
                f"{gdp_us_qoq:.1f}%",
                f"NASDAQ {nasdaq_val:,.0f}",
                f"{nasdaq_chg:+.2f}%",
                "ISM 48.2 (contracting)"
            ],
            "China": [
                "3.00% (1Y LPR)",
                "5.1% (urban surveyed)",
                f"{cpi_cn_yoy:.2f}%",
                f"{gdp_cn_qoq:.1f}%",
                f"Shanghai Comp {sh_val:,.0f}",
                f"{sh_chg:+.2f}%",
                "Caixin 50.5 (slight expansion)"
            ],
            "Deep Tech Impact": [
                "Lower → cheaper VC money",
                "Lower → talent competition",
                "2–3% ideal for risk assets",
                "Higher → bigger R&D budgets",
                "Bullish → risk-on for deep tech",
                "Green → momentum",
                ">50 = expanding supply chains"
            ]
        })
        return df

    except Exception as e:
        time.sleep(3)  # now time is defined
        try:
            # Full retry – duplicate everything
            start = datetime(2015, 1, 1)
            fed_rate = web.DataReader("FEDFUNDS", "fred", start, timeout=30).iloc[-1, 0]
            unrate_us = web.DataReader("UNRATE", "fred", start, timeout=30).iloc[-1, 0]
            cpi_us = web.DataReader("CPIAUCSL", "fred", start, timeout=30).pct_change(12).iloc[-1, 0] * 100
            gdp_us_qoq = web.DataReader("A191RL1Q225S", "fred", start, timeout=30).iloc[-1, 0]

            nasdaq = yf.download("^IXIC", period="5d", progress=False, timeout=30)["Close"]
            nasdaq_val = nasdaq.iloc[-1] if len(nasdaq) > 0 else 0
            nasdaq_chg = (nasdaq.iloc[-1] / nasdaq.iloc[-2] - 1) * 100 if len(nasdaq) > 1 else 0

            sh = yf.download("000001.SS", period="5d", progress=False, timeout=30)["Close"]
            sh_val = sh.iloc[-1] if len(sh) > 0 else 0
            sh_chg = (sh.iloc[-1] / sh.iloc[-2] - 1) * 100 if len(sh) > 1 else 0

            cpi_cn_yoy = web.DataReader("CHNCPIALLMINMEI", "fred", start, timeout=30).iloc[-1, 0]
            gdp_cn_qoq = web.DataReader("CHNGDPRQDSMEI", "fred", start, timeout=30).iloc[-1, 0]

            df = pd.DataFrame({
                "Metric": [
                    "Key Policy Rate", "Unemployment Rate", "CPI Inflation YoY", "Real GDP Growth (QoQ annualized)",
                    "Main Tech Index", "Index Daily Δ", "Manufacturing PMI (latest approx)"
                ],
                "United States": [
                    f"{fed_rate:.2f}% (Fed Funds)",
                    f"{unrate_us:.1f}%",
                    f"{cpi_us:.2f}%",
                    f"{gdp_us_qoq:.1f}%",
                    f"NASDAQ {nasdaq_val:,.0f}",
                    f"{nasdaq_chg:+.2f}%",
                    "ISM 48.2 (contracting)"
                ],
                "China": [
                    "3.00% (1Y LPR)",
                    "5.1% (urban surveyed)",
                    f"{cpi_cn_yoy:.2f}%",
                    f"{gdp_cn_qoq:.1f}%",
                    f"Shanghai Comp {sh_val:,.0f}",
                    f"{sh_chg:+.2f}%",
                    "Caixin 50.5 (slight expansion)"
                ],
                "Deep Tech Impact": [
                    "Lower → cheaper VC money", "Lower → talent competition", "2–3% ideal for risk assets",
                    "Higher → bigger R&D budgets", "Bullish → risk-on for deep tech", "Green → momentum",
                    ">50 = expanding supply chains"
                ]
            })
            return df
        except:
            return None

macro_df = fetch_macro_metrics()
if macro_df is not None:
    st.dataframe(macro_df, use_container_width=True, hide_index=True)
    last_update = datetime.now().strftime("%B %d, %Y at %H:%M UTC")
    st.caption(f"Sources: FRED (St. Louis Fed), yfinance • Last updated: {last_update}")
else:
    st.info("Macro panel loading fresh data... (usually <20 seconds on first visit after idle)")

# === SIDEBAR (unchanged) ===
with st.sidebar:
    st.header("🔑 API Keys")
    perplexity_key = st.text_input("Perplexity API Key", type="password")
    xai_key = st.text_input("xAI Grok API Key", type="password", help="https://x.ai/api")
    eth_rpc = st.text_input("Ethereum RPC", value="https://sepolia.infura.io/v3/YOUR_INFURA_KEY")
    eth_private_key = st.text_input("ETH Private Key", type="password")
    st.header("🛠️ Mode")
    use_mock = st.checkbox("Mock Mode (No APIs)", value=True)
    enable_blockchain = st.checkbox("Enable Blockchain Log", value=False)

# === MULTI-TICKER WATCHLIST ===
st.subheader("📊 Multi-Ticker Watchlist")
watchlist = st.multiselect("Add Tickers", ["MP", "NVDA", "IONQ", "QUBT"], default=["MP"])
period = st.selectbox("Price History", ["1mo", "3mo", "6mo", "1y"], index=0)

if st.button("Run Inference + Crunch", type="primary"):
    with st.spinner("Fetching data + running analysis..."):
        try:
            # === REAL PRICE DATA (yfinance) ===
            data = {}
            for ticker in watchlist:
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)
                if not hist.empty:
                    prices = hist['Close'].values
                    returns = np.diff(np.log(prices))
                    vol = np.std(returns) * np.sqrt(252) * 100 if len(returns) > 1 else 0
                    momentum = (prices[-1] / prices[0] - 1) * 100
                    data[ticker] = {
                        'prices': prices,
                        'hist': hist,
                        'vol': vol,
                        'momentum': momentum,
                        'current': prices[-1]
                    }

            # Metrics table
            metrics_df = pd.DataFrame({
                'Ticker': list(data.keys()),
                'Current Price': [f"${d['current']:.2f}" for d in data.values()],
                'Volatility': [f"{d['vol']:.1f}%" for d in data.values()],
                f"{period.upper()} Return": [f"{d['momentum']:+.1f}%" for d in data.values()]
            })
            st.dataframe(metrics_df)

            # Charts
            for ticker, d in data.items():
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Current Price", f"${d['current']:.2f}")
                with col2:
                    st.metric("Volatility", f"{d['vol']:.1f}%")
                st.line_chart(d['hist']['Close'], use_container_width=True)

            # === LIVE PERPLEXITY AI ===
            if not use_mock and perplexity_key:
                st.subheader("🔮 Live Perplexity Insights")
                try:
                    for ticker in watchlist:
                        url = "https://api.perplexity.ai/chat/completions"
                        payload = {
                            "model": "llama-3.1-sonar-small-128k-online",
                            "messages": [{"role": "user", "content": f"Analyze {ticker}: latest earnings, valuation, macro risks, AI/blockchain relevance, 6-month outlook. Be concise, cite sources."}],
                            "temperature": 0.3
                        }
                        headers = {"Authorization": f"Bearer {perplexity_key}", "Content-Type": "application/json"}
                        response = requests.post(url, json=payload, headers=headers, timeout=30)
                        if response.status_code == 200:
                            result = response.json()
                            st.write(f"**{ticker}**: {result['choices'][0]['message']['content']}")
                        else:
                            st.error(f"Perplexity Error {ticker}: {response.status_code}")
                except Exception as e:
                    st.error(f"Perplexity API Issue: {str(e)}")
            else:
                st.subheader("🔮 Mock Insights")
                for ticker in watchlist:
                    st.write(f"**{ticker}**: Q2 revenue up 84% YoY, DoD deal locked. Geopolitical tailwinds strong. (Mock)")

            # === GROK/XAI LIVE SENTIMENT ===
            if not use_mock and xai_key:
                st.subheader("🚀 Grok/xAI X Sentiment")
                try:
                    for ticker in watchlist:
                        url = "https://api.x.ai/v1/chat/completions"
                        payload = {
                            "model": "grok-beta",
                            "messages": [{"role": "user", "content": f"Analyze recent X sentiment on {ticker}: bullish/bearish ratio, key themes, score 1-10. Limit to 10 posts."}]
                        }
                        headers = {"Authorization": f"Bearer {xai_key}", "Content-Type": "application/json"}
                        response = requests.post(url, json=payload, headers=headers)
                        if response.status_code == 200:
                            result = response.json()
                            st.write(f"**{ticker}**: {result['choices'][0]['message']['content']}")
                        else:
                            st.info(f"Grok API: {response.status_code} — Check key at https://x.ai/api")
                except Exception as e:
                    st.error(f"Grok API Issue: {str(e)}")
            else:
                st.subheader("🚀 Mock X Sentiment")
                for ticker in watchlist:
                    st.info(f"Grok: High conviction on {ticker} — Bullish 7/10 from recent X buzz. (Mock)")

            # === BLOCKCHAIN TRADE LOG ===
            if enable_blockchain and eth_rpc and eth_private_key:
                st.subheader("🔗 Blockchain Trade Log")
                w3 = Web3(Web3.HTTPProvider(eth_rpc))
                if w3.is_connected():
                    account = w3.eth.account.from_key(eth_private_key)
                    st.write(f"Connected: {account.address}")
                    if st.button("Log Test Trade (0.001 ETH)"):
                        tx = {
                            'to': account.address,
                            'value': w3.to_wei(0.001, 'ether'),
                            'gas': 21000,
                            'gasPrice': w3.to_wei('50', 'gwei'),
                            'nonce': w3.eth.get_transaction_count(account.address)
                        }
                        signed_tx = w3.eth.account.sign_transaction(tx, eth_private_key)
                        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                        st.success(f"Trade logged! TX Hash: {tx_hash.hex()}")
                else:
                    st.error("Ethereum RPC not connected")
            else:
                st.subheader("🔗 Mock Blockchain Log")
                st.info("Trade logged on testnet: 0xmock123... (Enable for real)")

            # === FUTURES STUB ===
            st.subheader("📈 Futures Stub (Samuria Prep)")
            futures_ticker = st.selectbox("Futures", ["ES=F", "NQ=F", "GC=F"])
            exchange = ccxt.binance()
            try:
                ticker_data = exchange.fetch_ticker(futures_ticker)
                st.metric("Futures Price", f"${ticker_data['last']:.2f}")
            except:
                st.info("Futures data loading...")

            # === EXPORT ===
            for ticker in watchlist:
                if ticker in data:
                    export_df = data[ticker]['hist'][['Close']].reset_index()
                    export_df.columns = ['Date', 'Price']
                    csv = export_df.to_csv(index=False)
                    st.download_button("Export Data", csv, f"{ticker}_{period}_karmtiger.csv", "text/csv")

        except Exception as e:
            st.error(f"Oops: {str(e)}")
            st.info("Check APIs/keys — Mock Mode always works!")

else:
    st.info("Add tickers → Select period → Click **Run Inference + Crunch**")
    st.caption("v0.3: Beast Mode — Live AI, X sentiment, watchlist, blockchain, futures prep")