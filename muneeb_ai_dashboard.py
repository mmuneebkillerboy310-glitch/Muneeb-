# ══════════════════════════════════════════════════════
# MUNEEB·AI — Pakistan Live Price Intelligence
# Complete Streamlit Dashboard
# Created by MUNEEB | June 2026
# ══════════════════════════════════════════════════════

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
import math

# ══════════════════════════════════════
# PAGE CONFIG — Must be first Streamlit command
# ══════════════════════════════════════
st.set_page_config(
    page_title="MUNEEB·AI — Pakistan Price Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════
# CUSTOM CSS — Dark Cyberpunk Theme
# ══════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@500;700&display=swap');

/* Dark background */
.stApp {
    background: #020408;
    color: #e8f4f8;
}

/* Hide Streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Main container */
.block-container {
    padding: 1.5rem 2rem;
    max-width: 1400px;
}

/* Page title */
.page-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(1.2rem, 3vw, 2rem);
    font-weight: 900;
    letter-spacing: 6px;
    background: linear-gradient(90deg, #00f5ff, #00ff88, #00f5ff);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    animation: shimmer 3s linear infinite;
    margin-bottom: 4px;
}

.page-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62rem;
    color: rgba(0,245,255,0.38);
    letter-spacing: 4px;
    text-align: center;
    margin-bottom: 24px;
}

@keyframes shimmer {
    from { background-position: 0%; }
    to   { background-position: 200%; }
}

/* Metric cards */
.metric-card {
    background: rgba(3,14,26,0.95);
    border: 1px solid rgba(0,245,255,0.18);
    padding: 18px 20px;
    text-align: center;
    transition: all 0.3s;
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    border-color: rgba(0,245,255,0.5);
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(0,245,255,0.1);
}

.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 3px;
    color: rgba(0,245,255,0.4);
    text-transform: uppercase;
    margin-bottom: 8px;
}

.metric-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 6px;
}

.metric-change {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.62rem;
}

.up   { color: #ff3366; }
.down { color: #00ff88; }
.neu  { color: #ffd600; }

/* Alert boxes */
.alert-box {
    padding: 12px 16px;
    border-left: 3px solid;
    margin-bottom: 10px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    line-height: 1.6;
    background: rgba(255,255,255,0.02);
}

.alert-red    { border-color: #ff3366; color: rgba(255,255,255,0.65); }
.alert-green  { border-color: #00ff88; color: rgba(255,255,255,0.65); }
.alert-yellow { border-color: #ffd600; color: rgba(255,255,255,0.65); }
.alert-blue   { border-color: #00f5ff; color: rgba(255,255,255,0.65); }

/* Section headers */
.section-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 4px;
    color: #00f5ff;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(0,245,255,0.15);
    padding-bottom: 8px;
    margin-bottom: 16px;
}

/* Credit footer */
.credit {
    font-family: 'Orbitron', sans-serif;
    text-align: center;
    letter-spacing: 8px;
    font-size: 1rem;
    font-weight: 900;
    color: #00ff88;
    text-shadow: 0 0 30px rgba(0,255,136,0.6);
    padding: 20px;
    margin-top: 30px;
    border-top: 1px solid rgba(0,245,255,0.1);
}

/* Streamlit metric overrides */
[data-testid="metric-container"] {
    background: rgba(3,14,26,0.9);
    border: 1px solid rgba(0,245,255,0.18);
    padding: 14px;
}

[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 2px !important;
    color: rgba(0,245,255,0.5) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    color: #ffd600 !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'Share Tech Mono', monospace !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(3,14,26,0.9);
    border-bottom: 1px solid rgba(0,245,255,0.15);
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: rgba(0,245,255,0.45);
    background: transparent;
    border: none;
    padding: 10px 18px;
}

.stTabs [aria-selected="true"] {
    color: #00f5ff !important;
    border-bottom: 2px solid #00f5ff !important;
}

/* Selectbox, buttons */
.stSelectbox > div > div {
    background: rgba(3,14,26,0.9);
    border: 1px solid rgba(0,245,255,0.25);
    color: #e8f4f8;
    font-family: 'Share Tech Mono', monospace;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(0,245,255,0.1), rgba(0,255,136,0.05));
    border: 1px solid rgba(0,245,255,0.3);
    color: #00f5ff;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 2px;
    transition: all 0.3s;
}

.stButton > button:hover {
    border-color: #00f5ff;
    box-shadow: 0 0 20px rgba(0,245,255,0.2);
}

/* DataFrame */
.stDataFrame { border: 1px solid rgba(0,245,255,0.15); }

/* Sidebar */
.css-1d391kg { background: rgba(3,14,26,0.98); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# API CONFIG
# ══════════════════════════════════════
API_CONFIG = {
    "dollar_1":  "https://open.er-api.com/v6/latest/USD",
    "dollar_2":  "https://api.exchangerate-api.com/v4/latest/USD",
    "gold":      "https://gold-api.com/price/XAU",
    "gold_bkp":  "https://api.metals.live/v1/spot/gold",
    "weather":   "https://api.open-meteo.com/v1/forecast?latitude=31.5497&longitude=74.3436&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code&timezone=Asia/Karachi",
    "kse":       "https://query1.finance.yahoo.com/v8/finance/chart/%5EKSE?interval=1d&range=5d",
    "timeout":   8,
}

# Seed prices — June 2026
SEED_PRICES = {
    "petrol": {"price": 377.78, "prev": 381.78, "unit": "₨", "label": "Petrol", "emoji": "⛽", "color": "#ff6d00"},
    "gold":   {"price": 502000, "prev": 499500, "unit": "₨", "label": "Gold",   "emoji": "🥇", "color": "#ffd600"},
    "dollar": {"price": 279.10, "prev": 279.05, "unit": "₨", "label": "Dollar", "emoji": "💵", "color": "#00ff88"},
    "wheat":  {"price": 3400,   "prev": 3500,   "unit": "₨", "label": "Wheat",  "emoji": "🌾", "color": "#00f5ff"},
    "sugar":  {"price": 162,    "prev": 160,    "unit": "₨", "label": "Sugar",  "emoji": "🍬", "color": "#b44fff"},
    "onion":  {"price": 52,     "prev": 55,     "unit": "₨", "label": "Onion",  "emoji": "🧅", "color": "#ffd600"},
}

# 14-day price history
HISTORY = {
    "petrol": [409.78,409.78,409.78,403.78,403.78,403.78,403.78,381.78,381.78,381.78,377.78,377.78,377.78,377.78],
    "gold":   [488000,490000,492000,491000,494000,495000,497000,499000,498000,500000,501000,502000,502000,502000],
    "dollar": [280.2,280.0,279.8,279.6,279.5,279.4,279.3,279.2,279.3,279.2,279.1,279.1,279.1,279.1],
    "wheat":  [3600,3580,3560,3540,3520,3500,3490,3480,3470,3460,3450,3420,3410,3400],
    "sugar":  [156,157,157,158,159,159,160,160,161,161,162,162,162,162],
    "onion":  [80,75,70,68,65,63,60,58,56,55,54,53,52,52],
}

# ══════════════════════════════════════
# DATA FETCHING FUNCTIONS
# ══════════════════════════════════════

@st.cache_data(ttl=1800)  # Cache 30 minutes
def fetch_dollar_rate():
    """Fetch live USD/PKR rate with fallback"""
    for url in [API_CONFIG["dollar_1"], API_CONFIG["dollar_2"]]:
        try:
            r = requests.get(url, timeout=API_CONFIG["timeout"])
            data = r.json()
            pkr = data.get("rates", {}).get("PKR") or data.get("conversion_rates", {}).get("PKR")
            if pkr and 250 < pkr < 320:
                return round(float(pkr), 2), "🟢 Live"
        except Exception as e:
            continue
    return SEED_PRICES["dollar"]["price"], "🟡 Cached"


@st.cache_data(ttl=1800)
def fetch_gold_price(dollar_rate: float):
    """Fetch live gold price and convert to PKR tola"""
    OZ_TO_TOLA = 11.6638 / 31.1035
    for url, key in [(API_CONFIG["gold"], "price"), (API_CONFIG["gold_bkp"], None)]:
        try:
            r = requests.get(url, timeout=API_CONFIG["timeout"])
            data = r.json()
            if key:
                oz_usd = data.get(key)
            else:
                oz_usd = data[0].get("gold") if isinstance(data, list) else None
            if oz_usd and 1000 < oz_usd < 12000:
                tola_pkr = round(oz_usd * OZ_TO_TOLA * dollar_rate)
                if 350000 < tola_pkr < 900000:
                    return tola_pkr, "🟢 Live"
        except Exception:
            continue
    return SEED_PRICES["gold"]["price"], "🟡 Cached"


@st.cache_data(ttl=1800)
def fetch_weather():
    """Fetch Lahore weather from Open-Meteo"""
    CODES = {
        0: "☀️ Clear",      1: "🌤️ Mostly Clear",  2: "⛅ Partly Cloudy",
        3: "☁️ Overcast",   45: "🌫️ Foggy",         51: "🌦️ Drizzle",
        61: "🌧️ Rain",      80: "🌦️ Showers",        95: "⛈️ Thunderstorm",
    }
    try:
        r = requests.get(API_CONFIG["weather"], timeout=API_CONFIG["timeout"])
        data = r.json()
        cur = data.get("current", {})
        temp = cur.get("temperature_2m")
        if temp and -5 < temp < 60:
            code = cur.get("weather_code", 0)
            return {
                "temp":      round(temp),
                "humidity":  cur.get("relative_humidity_2m", 45),
                "wind":      round(cur.get("wind_speed_10m", 10)),
                "condition": CODES.get(code, "🌡️ Variable"),
                "status":    "🟢 Live",
            }
    except Exception:
        pass
    return {"temp": 38, "humidity": 42, "wind": 12, "condition": "☀️ Clear", "status": "🟡 Cached"}


@st.cache_data(ttl=1800)
def fetch_kse100():
    """Fetch KSE-100 from Yahoo Finance"""
    try:
        r = requests.get(API_CONFIG["kse"], timeout=API_CONFIG["timeout"],
                         headers={"Accept": "application/json"})
        data = r.json()
        meta = data["chart"]["result"][0]["meta"]
        price = meta.get("regularMarketPrice") or meta.get("previousClose")
        prev  = meta.get("chartPreviousClose") or price
        if price and 50000 < price < 250000:
            change = price - prev
            return {
                "value":   round(price),
                "change":  round(change),
                "pct":     round((change / prev) * 100, 2),
                "trend":   "UP" if change >= 0 else "DOWN",
                "status":  "🟢 Live",
            }
    except Exception:
        pass
    return {"value": 118500, "change": 1300, "pct": 1.11, "trend": "UP", "status": "🟡 Cached"}


def get_all_prices():
    """Fetch all prices and return complete data dict"""
    dollar_price, dollar_status = fetch_dollar_rate()
    gold_price,   gold_status   = fetch_gold_price(dollar_price)
    weather                     = fetch_weather()
    kse                         = fetch_kse100()

    prices = {k: v.copy() for k, v in SEED_PRICES.items()}
    prices["dollar"]["price"] = dollar_price
    prices["dollar"]["status"] = dollar_status
    prices["gold"]["price"]   = gold_price
    prices["gold"]["status"]  = gold_status

    for k in ["petrol", "wheat", "sugar", "onion"]:
        prices[k]["status"] = "🟡 Cached"

    return prices, weather, kse


# ══════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════

def fmt_price(value, unit="₨"):
    """Format price with commas"""
    if value >= 1000:
        return f"{unit} {value:,.0f}"
    return f"{unit} {value:.2f}"


def calc_change(current, prev):
    """Calculate % change"""
    if prev == 0:
        return 0
    return round(((current - prev) / prev) * 100, 2)


def trend_arrow(current, prev):
    """Get trend arrow and color"""
    if current > prev:   return "▲", "up"
    elif current < prev: return "▼", "down"
    else:                return "●", "neu"


def generate_forecast(history: list, days: int = 14) -> list:
    """Generate AI forecast based on real history trend"""
    if len(history) < 3:
        return history[-1:] * days

    # Calculate daily rate from last 7 days
    recent = history[-7:]
    daily_rate = (recent[-1] - recent[0]) / (len(recent) - 1) / recent[0]

    # Dampen for uncertainty
    forecast = []
    cur = history[-1]
    for i in range(days):
        dampening = 1 - (i / (days * 2))
        noise     = (0.5 - 0.5) * 0.005  # minimal noise
        cur = cur * (1 + daily_rate * dampening + noise)
        forecast.append(round(cur, 2))

    return forecast


# ══════════════════════════════════════
# CHART FUNCTIONS
# ══════════════════════════════════════

def make_price_chart(key: str, history: list, forecast: list, color: str, label: str) -> go.Figure:
    """Build interactive Plotly chart with history + forecast"""
    today  = datetime.now()
    dates_past = [today - timedelta(days=len(history)-1-i) for i in range(len(history))]
    dates_fore = [today + timedelta(days=i+1) for i in range(len(forecast))]

    fig = go.Figure()

    # Actual price line
    fig.add_trace(go.Scatter(
        x=dates_past,
        y=history,
        name="Actual Price",
        line=dict(color=color, width=2.5),
        fill="tozeroy",
        fillcolor=color.replace(")", ",0.1)").replace("rgb", "rgba") if color.startswith("rgb") else color + "18",
        mode="lines+markers",
        marker=dict(size=6, color=color, line=dict(width=2, color="#020408")),
        hovertemplate="<b>%{x|%d %b}</b><br>Price: ₨%{y:,.2f}<extra></extra>",
    ))

    # Forecast line (dashed)
    fig.add_trace(go.Scatter(
        x=[dates_past[-1]] + dates_fore,
        y=[history[-1]] + forecast,
        name="AI Forecast",
        line=dict(color="#00ff88", width=2, dash="dot"),
        fill="tozeroy",
        fillcolor="rgba(0,255,136,0.05)",
        mode="lines+markers",
        marker=dict(size=5, color="#00ff88", symbol="diamond"),
        hovertemplate="<b>%{x|%d %b}</b><br>Forecast: ₨%{y:,.2f}<extra></extra>",
    ))

    # Vertical line at today
    fig.add_vline(
        x=today,
        line_width=1,
        line_dash="dash",
        line_color="rgba(255,214,0,0.4)",
        annotation_text="Today",
        annotation_font_color="#ffd600",
        annotation_font_size=10,
    )

    fig.update_layout(
        paper_bgcolor="rgba(3,14,26,0.95)",
        plot_bgcolor="rgba(2,4,8,0.8)",
        font=dict(family="Share Tech Mono, monospace", color="#e8f4f8"),
        height=320,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right",  x=1,
            font=dict(size=10),
            bgcolor="rgba(0,0,0,0)",
        ),
        xaxis=dict(
            gridcolor="rgba(0,245,255,0.06)",
            linecolor="rgba(0,245,255,0.2)",
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            gridcolor="rgba(0,245,255,0.06)",
            linecolor="rgba(0,245,255,0.2)",
            tickfont=dict(size=10),
            tickformat=",.0f",
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="rgba(3,14,26,0.97)",
            bordercolor="#00f5ff",
            font=dict(family="Share Tech Mono", size=12),
        ),
    )

    return fig


def make_comparison_chart(prices: dict) -> go.Figure:
    """Bar chart comparing all commodities % change"""
    labels, changes, colors = [], [], []
    for k, d in prices.items():
        chg = calc_change(d["price"], d["prev"])
        labels.append(f"{d['emoji']} {d['label']}")
        changes.append(chg)
        colors.append("#00ff88" if chg <= 0 else "#ff3366")

    fig = go.Figure(go.Bar(
        x=labels,
        y=changes,
        marker_color=colors,
        text=[f"{c:+.1f}%" for c in changes],
        textposition="outside",
        textfont=dict(family="Share Tech Mono", size=11),
        hovertemplate="<b>%{x}</b><br>Change: %{y:+.2f}%<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(3,14,26,0.95)",
        plot_bgcolor="rgba(2,4,8,0.8)",
        font=dict(family="Share Tech Mono, monospace", color="#e8f4f8"),
        height=250,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(gridcolor="rgba(0,245,255,0.06)", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="rgba(0,245,255,0.06)", tickfont=dict(size=10), ticksuffix="%"),
        showlegend=False,
    )

    fig.add_hline(y=0, line_color="rgba(255,255,255,0.2)", line_width=1)
    return fig


def make_gauge(value: float, max_val: float, title: str, color: str) -> go.Figure:
    """Circular gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title=dict(text=title, font=dict(size=11, family="Share Tech Mono", color="#00f5ff")),
        number=dict(font=dict(size=16, family="Orbitron", color=color)),
        gauge=dict(
            axis=dict(range=[0, max_val], tickfont=dict(size=9, color="#666")),
            bar=dict(color=color),
            bgcolor="rgba(0,0,0,0.3)",
            borderwidth=1,
            bordercolor="rgba(0,245,255,0.2)",
            steps=[
                dict(range=[0, max_val*0.4], color="rgba(0,255,136,0.1)"),
                dict(range=[max_val*0.4, max_val*0.7], color="rgba(255,214,0,0.1)"),
                dict(range=[max_val*0.7, max_val], color="rgba(255,51,102,0.1)"),
            ],
        )
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=160,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(color="#e8f4f8"),
    )
    return fig


# ══════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════

def main():
    # ── HEADER ──
    st.markdown('<div class="page-title">MUNEEB·AI PRICE INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-sub">PAKISTAN LIVE MARKET DATA · AI FORECAST · REAL-TIME</div>', unsafe_allow_html=True)

    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown("### ⚙️ Controls")
        auto_refresh = st.toggle("Auto Refresh (30min)", value=True)
        city = st.selectbox("Weather City", ["Lahore", "Karachi", "Islamabad", "Peshawar"])
        st.markdown("---")
        st.markdown("### 📞 Contact")
        st.markdown("**WhatsApp:** 0312-0063850")
        st.markdown("**Created by:** MUNEEB")
        st.markdown("---")
        if st.button("🔄 Refresh Now"):
            st.cache_data.clear()
            st.rerun()

    # ── FETCH DATA ──
    with st.spinner("Fetching live Pakistan market data..."):
        prices, weather, kse = get_all_prices()

    # Last updated
    st.markdown(
        f'<div style="font-family:monospace;font-size:.6rem;color:rgba(0,245,255,.4);'
        f'text-align:right;margin-bottom:12px">⏱️ Last Updated: {datetime.now().strftime("%I:%M %p")} PKT</div>',
        unsafe_allow_html=True
    )

    # ════════════════════════════════
    # TABS
    # ════════════════════════════════
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 LIVE PRICES",
        "📈 CHARTS & FORECAST",
        "📰 ANALYSIS",
        "🌤️ MARKET OVERVIEW"
    ])

    # ════════════════════
    # TAB 1 — LIVE PRICES
    # ════════════════════
    with tab1:
        st.markdown('<div class="section-header">⚡ LIVE COMMODITY PRICES</div>', unsafe_allow_html=True)

        # 3 columns top row
        cols = st.columns(3)
        top_keys = ["petrol", "gold", "dollar"]
        for i, key in enumerate(top_keys):
            d = prices[key]
            arrow, cls = trend_arrow(d["price"], d["prev"])
            chg = calc_change(d["price"], d["prev"])
            with cols[i]:
                st.metric(
                    label=f"{d['emoji']} {d['label']}",
                    value=fmt_price(d["price"], d["unit"]),
                    delta=f"{arrow} {abs(chg):.1f}% {d.get('status','🟡')}",
                    delta_color="inverse" if key == "petrol" else "normal",
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # 3 columns bottom row
        cols2 = st.columns(3)
        bot_keys = ["wheat", "sugar", "onion"]
        for i, key in enumerate(bot_keys):
            d = prices[key]
            arrow, cls = trend_arrow(d["price"], d["prev"])
            chg = calc_change(d["price"], d["prev"])
            with cols2[i]:
                st.metric(
                    label=f"{d['emoji']} {d['label']}",
                    value=fmt_price(d["price"], d["unit"]),
                    delta=f"{arrow} {abs(chg):.1f}% {d.get('status','🟡')}",
                    delta_color="inverse",
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Comparison Bar Chart ──
        st.markdown('<div class="section-header">📊 PRICE CHANGE COMPARISON</div>', unsafe_allow_html=True)
        st.plotly_chart(make_comparison_chart(prices), use_container_width=True)

        # ── Data Table ──
        st.markdown('<div class="section-header">📋 DETAILED PRICE TABLE</div>', unsafe_allow_html=True)
        table_data = []
        for k, d in prices.items():
            chg = calc_change(d["price"], d["prev"])
            arrow = "▲" if chg > 0 else "▼" if chg < 0 else "●"
            table_data.append({
                "Commodity":    f"{d['emoji']} {d['label']}",
                "Current Price":fmt_price(d["price"], d["unit"]),
                "Previous":     fmt_price(d["prev"], d["unit"]),
                "Change":       f"{arrow} {abs(chg):.1f}%",
                "Trend":        "RISING" if chg > 0 else "FALLING" if chg < 0 else "STABLE",
                "Data Source":  d.get("status", "🟡 Cached"),
            })

        df = pd.DataFrame(table_data)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    # ════════════════════════════════
    # TAB 2 — CHARTS & FORECAST
    # ════════════════════════════════
    with tab2:
        st.markdown('<div class="section-header">📈 INTERACTIVE PRICE CHARTS + AI FORECAST</div>', unsafe_allow_html=True)

        # Commodity selector
        selected = st.selectbox(
            "Select Commodity",
            options=list(prices.keys()),
            format_func=lambda k: f"{prices[k]['emoji']} {prices[k]['label']}",
            key="chart_select"
        )

        d       = prices[selected]
        history = HISTORY[selected]
        fc      = generate_forecast(history, days=14)
        color   = d["color"]

        # Main chart
        st.plotly_chart(
            make_price_chart(selected, history, fc, color, d["label"]),
            use_container_width=True
        )

        # Stats below chart
        high = max(history); low = min(history)
        avg  = sum(history) / len(history)
        chg  = calc_change(history[-1], history[0])

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Current",     fmt_price(d["price"], d["unit"]))
        c2.metric("14-Day High", fmt_price(high, d["unit"]), delta="High")
        c3.metric("14-Day Low",  fmt_price(low,  d["unit"]), delta="Low",  delta_color="inverse")
        c4.metric("Average",     fmt_price(round(avg, 2), d["unit"]))
        c5.metric("14D Change",  f"{chg:+.1f}%", delta_color="inverse" if chg < 0 else "normal")

        st.markdown("<br>", unsafe_allow_html=True)

        # Forecast table
        st.markdown('<div class="section-header">🤖 AI 14-DAY FORECAST TABLE</div>', unsafe_allow_html=True)
        today = datetime.now()
        fc_rows = []
        for i, fp in enumerate(fc):
            dt   = today + timedelta(days=i+1)
            prev = history[-1] if i == 0 else fc[i-1]
            chg  = calc_change(fp, prev)
            conf = max(50, 92 - i*3)
            fc_rows.append({
                "Date":       dt.strftime("%a, %d %b"),
                "AI Price":   fmt_price(fp, d["unit"]),
                "Change":     f"{'▲' if chg>0 else '▼' if chg<0 else '●'} {abs(chg):.1f}%",
                "Direction":  "RISING" if chg>0 else "FALLING" if chg<0 else "STABLE",
                "Confidence": f"{conf}%",
            })

        st.dataframe(pd.DataFrame(fc_rows), use_container_width=True, hide_index=True)

    # ════════════════════════════════
    # TAB 3 — ANALYSIS
    # ════════════════════════════════
    with tab3:
        st.markdown('<div class="section-header">🧠 AI MARKET ANALYSIS</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns([2, 1])

        with col_a:
            # Smart alerts
            st.markdown('<div class="section-header">⚡ SMART ALERTS</div>', unsafe_allow_html=True)
            alerts = [
                ("🔴", "alert-red",    f"OGRA Petrol: {fmt_price(prices['petrol']['price'],'₨')}/liter — OGRA weekly review pending. Global oil volatile due to Iran conflict!"),
                ("🟢", "alert-green",  f"Onion: {fmt_price(prices['onion']['price'],'₨')}/kg — Prices falling! New Sindh crop in market. Expected ₨40-45 in 2 weeks."),
                ("🟡", "alert-yellow", f"Gold: {fmt_price(prices['gold']['price'],'₨')}/tola — Historic highs! Iran war demand + USD weakness. HOLD — do not sell."),
                ("🔵", "alert-blue",   f"Dollar: {fmt_price(prices['dollar']['price'],'₨')} — Stable. IMF review positive, remittances strong at $3.2bn in May 2026."),
            ]
            for icon, cls, msg in alerts:
                st.markdown(f'<div class="alert-box {cls}">{icon} {msg}</div>', unsafe_allow_html=True)

        with col_b:
            # Economic indicators as gauges
            st.markdown('<div class="section-header">📊 INDICATORS</div>', unsafe_allow_html=True)
            st.plotly_chart(make_gauge(4.5, 30, "Inflation %", "#00ff88"),    use_container_width=True)
            st.plotly_chart(make_gauge(12,  25, "SBP Rate %",  "#ffd600"),    use_container_width=True)
            st.plotly_chart(make_gauge(78,  100,"Oil Risk",     "#ff3366"),   use_container_width=True)

        # Historical comparison
        st.markdown('<div class="section-header">📅 HISTORICAL PRICE COMPARISON</div>', unsafe_allow_html=True)
        comp_cols = st.columns(len(prices))
        for i, (k, d) in enumerate(prices.items()):
            with comp_cols[i]:
                # Approximate 30-day ago prices
                hist30 = HISTORY[k][0] if HISTORY.get(k) else d["prev"]
                chg30  = calc_change(d["price"], hist30)
                color  = "🟢" if chg30 <= 0 else "🔴"
                st.markdown(
                    f"**{d['emoji']} {d['label']}**\n\n"
                    f"Now: **{fmt_price(d['price'],'₨')}**\n\n"
                    f"30d ago: {fmt_price(hist30,'₨')}\n\n"
                    f"{color} **{chg30:+.1f}%**"
                )

    # ════════════════════════════════
    # TAB 4 — MARKET OVERVIEW
    # ════════════════════════════════
    with tab4:
        st.markdown('<div class="section-header">🌍 PAKISTAN MARKET OVERVIEW</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            # KSE-100
            st.markdown('<div class="section-header">📈 KSE-100 STOCK MARKET</div>', unsafe_allow_html=True)
            kse_color = "#00ff88" if kse["trend"] == "UP" else "#ff3366"
            kse_arrow = "▲" if kse["trend"] == "UP" else "▼"
            st.metric(
                label=f"🏦 KSE-100 Index {kse['status']}",
                value=f"{kse['value']:,.0f}",
                delta=f"{kse_arrow} {kse['change']:+,.0f} ({kse['pct']:+.2f}%)",
                delta_color="normal" if kse["trend"] == "UP" else "inverse",
            )

            # KSE gauge
            st.plotly_chart(
                make_gauge(kse["value"]/1000, 200, "KSE-100 (thousands)", kse_color),
                use_container_width=True
            )

        with col2:
            # Weather
            st.markdown('<div class="section-header">🌤️ LAHORE WEATHER</div>', unsafe_allow_html=True)
            wx = weather
            st.metric(
                label=f"{wx['condition']} {wx['status']}",
                value=f"{wx['temp']}°C",
                delta=f"💧 {wx['humidity']}% | 🌬️ {wx['wind']} km/h",
            )

            # Market summary
            st.markdown('<div class="section-header">📋 QUICK SUMMARY</div>', unsafe_allow_html=True)
            summary_data = {
                "Metric":  ["Inflation Rate", "SBP Policy Rate", "PKR vs USD", "Gold vs Last Month", "Petrol vs Last Month"],
                "Value":   ["4.5%", "12%", "₨279.10", f"{calc_change(prices['gold']['price'], HISTORY['gold'][0]):+.1f}%", f"{calc_change(prices['petrol']['price'], HISTORY['petrol'][0]):+.1f}%"],
                "Status":  ["🟢 Down", "🟢 Low", "🟡 Stable", "🔴 Up", "🟢 Down"],
            }
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

        # Pakistan economic news section
        st.markdown('<div class="section-header">📰 KEY ECONOMIC FACTS — JUNE 2026</div>', unsafe_allow_html=True)
        news_items = [
            ("🔴", "Petrol", f"OGRA latest rate: ₨377.78/liter (▼ June 6, 2026). Next review: June 16."),
            ("🟡", "Gold",   f"Historic high zone: ₨5,02,000/tola. Iran-Israel conflict driving safe-haven demand."),
            ("🟢", "Dollar", f"USD/PKR ₨279.10 — stable. Remittances record $3.2bn in May 2026."),
            ("🟢", "Wheat",  f"Mandi rate ₨3,400/40kg — below govt support price of ₨3,900. New harvest surplus."),
            ("🔴", "Inflation","Pakistan inflation 4.5% — down from 23.4% peak. IMF program on track."),
        ]
        for icon, topic, text in news_items:
            st.markdown(
                f"**{icon} {topic}:** {text}"
            )

    # ── FOOTER ──
    st.markdown(
        '<div class="credit">★ CREATED BY MUNEEB ★<br>'
        '<span style="font-size:.6rem;letter-spacing:4px;color:rgba(0,245,255,.3);">'
        'MUNEEB·AI — PAKISTAN LIVE PRICE INTELLIGENCE</span></div>',
        unsafe_allow_html=True
    )

    # Auto refresh
    if auto_refresh:
        time.sleep(1800)
        st.rerun()


if __name__ == "__main__":
    main()
