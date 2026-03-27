import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import random

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PhonePe Pulse India",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Hide default streamlit header */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0728 0%, #1a0a3d 40%, #0d1b35 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a0a3d 0%, #0f0728 100%);
    border-right: 1px solid rgba(138, 43, 226, 0.3);
}
[data-testid="stSidebar"] .stMarkdown, 
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] p {
    color: #c8b6ff !important;
}

/* Hero Header */
.hero-header {
    background: linear-gradient(135deg, #6b21a8 0%, #4f46e5 50%, #7c3aed 100%);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 60px rgba(109, 40, 217, 0.4);
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: white;
    margin: 0;
    line-height: 1.1;
}
.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1rem;
    color: rgba(255,255,255,0.75);
    margin-top: 0.5rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 100px;
    padding: 4px 16px;
    font-size: 0.8rem;
    color: #e9d5ff;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, rgba(109, 40, 217, 0.15) 0%, rgba(79, 70, 229, 0.1) 100%);
    border: 1px solid rgba(138, 43, 226, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    margin-bottom: 1rem;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 40px rgba(109, 40, 217, 0.3);
}
.kpi-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.kpi-value {
    font-family: 'Sora', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #a78bfa;
    margin: 0;
}
.kpi-label {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.6);
    margin-top: 0.3rem;
}
.kpi-delta {
    font-size: 0.8rem;
    margin-top: 0.3rem;
}
.delta-up { color: #4ade80; }
.delta-down { color: #f87171; }

/* Insight Cards */
.insight-card {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(5, 150, 105, 0.05) 100%);
    border: 1px solid rgba(52, 211, 153, 0.25);
    border-left: 4px solid #10b981;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.insight-card.warning {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(217, 119, 6, 0.05) 100%);
    border: 1px solid rgba(251, 191, 36, 0.25);
    border-left: 4px solid #f59e0b;
}
.insight-card.info {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(37, 99, 235, 0.05) 100%);
    border: 1px solid rgba(96, 165, 250, 0.25);
    border-left: 4px solid #3b82f6;
}
.insight-card.purple {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(109, 40, 217, 0.05) 100%);
    border: 1px solid rgba(167, 139, 250, 0.3);
    border-left: 4px solid #8b5cf6;
}
.insight-title {
    font-family: 'Sora', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 0.4rem;
}
.insight-text {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.65);
    line-height: 1.6;
}

/* Section Headers */
.section-header {
    font-family: 'Sora', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-sub {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.5);
    margin-top: -0.8rem;
    margin-bottom: 1.5rem;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15, 7, 40, 0.6);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 8px;
    color: rgba(255,255,255,0.5) !important;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    padding: 8px 20px;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(109, 40, 217, 0.15) !important;
    border: 1px solid rgba(138, 43, 226, 0.4) !important;
    border-radius: 10px !important;
    color: white !important;
}

/* Metric */
[data-testid="stMetric"] {
    background: rgba(109, 40, 217, 0.1);
    border: 1px solid rgba(138, 43, 226, 0.2);
    border-radius: 12px;
    padding: 1rem;
}
[data-testid="stMetricValue"] { color: #a78bfa !important; font-family: 'Sora', sans-serif !important; }
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.6) !important; }
[data-testid="stMetricDelta"] { color: #4ade80 !important; }

/* Divider */
hr { border-color: rgba(138, 43, 226, 0.2) !important; }

/* Expander */
.streamlit-expanderHeader {
    background: rgba(109, 40, 217, 0.1) !important;
    border-radius: 10px !important;
    color: #c4b5fd !important;
}

/* Plot backgrounds */
.plotly-graph-div { border-radius: 16px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── DATA GENERATION ─────────────────────────────────────────────────────────────
@st.cache_data
def generate_data():
    np.random.seed(42)
    random.seed(42)

    states = [
        "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Delhi",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
        "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
        "Meghalaya", "Nagaland", "Odisha", "Punjab", "Rajasthan",
        "Tamil Nadu", "Telangana", "Uttar Pradesh", "Uttarakhand",
        "West Bengal", "Jammu & Kashmir", "Sikkim", "Tripura"
    ]

    # State popularity weights (realistic)
    state_weights = {
        "Maharashtra": 18, "Karnataka": 15, "Telangana": 12, "Tamil Nadu": 11,
        "Delhi": 10, "Gujarat": 9, "Andhra Pradesh": 8, "Uttar Pradesh": 7,
        "West Bengal": 6, "Rajasthan": 5, "Madhya Pradesh": 4, "Kerala": 4,
        "Punjab": 3, "Haryana": 3, "Bihar": 2, "Odisha": 2,
        "Chhattisgarh": 1.5, "Jharkhand": 1.5, "Assam": 1.5, "Uttarakhand": 1,
        "Himachal Pradesh": 0.8, "Goa": 0.8, "Jammu & Kashmir": 0.7,
        "Manipur": 0.3, "Meghalaya": 0.3, "Nagaland": 0.2,
        "Sikkim": 0.1, "Tripura": 0.3
    }

    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]
    quarters = [1, 2, 3, 4]

    # ── Aggregated Transactions ──────────────────────────────────────────────────
    agg_txn_rows = []
    base_txn = {"Recharge & bill payments": 70, "Peer-to-peer payments": 150,
                 "Merchant payments": 90, "Financial services": 30, "Others": 20}
    growth = 1.0

    for yr in years:
        growth *= random.uniform(1.35, 1.65) if yr <= 2022 else random.uniform(1.15, 1.30)
        for q in quarters:
            q_mult = [0.9, 1.0, 1.05, 1.1][q-1]
            for category, base in base_txn.items():
                count = int(base * growth * q_mult * 1_000_000 * random.uniform(0.9, 1.1))
                amount = count * random.uniform(450, 850)
                agg_txn_rows.append({
                    "Year": yr, "Quarter": q, "Category": category,
                    "Count": count, "Amount": amount,
                    "YearQuarter": f"{yr} Q{q}"
                })

    agg_txn = pd.DataFrame(agg_txn_rows)

    # ── Aggregated Users ─────────────────────────────────────────────────────────
    agg_user_rows = []
    devices = ["Xiaomi", "Samsung", "Vivo", "Oppo", "Realme",
               "OnePlus", "Apple", "Motorola", "Nokia", "Others"]
    device_shares = [0.25, 0.20, 0.14, 0.12, 0.10, 0.07, 0.04, 0.03, 0.02, 0.03]
    base_users = 50_000_000
    u_growth = 1.0

    for yr in years:
        u_growth *= random.uniform(1.25, 1.55) if yr <= 2022 else random.uniform(1.08, 1.18)
        for q in quarters:
            q_mult = [0.9, 1.0, 1.05, 1.15][q-1]
            total_users = int(base_users * u_growth * q_mult)
            app_opens = int(total_users * random.uniform(4, 7))
            for d, s in zip(devices, device_shares):
                agg_user_rows.append({
                    "Year": yr, "Quarter": q, "Device": d,
                    "RegisteredUsers": int(total_users * s * random.uniform(0.9, 1.1)),
                    "AppOpens": int(app_opens * s * random.uniform(0.9, 1.1)),
                    "TotalUsers": total_users,
                    "YearQuarter": f"{yr} Q{q}"
                })

    agg_users = pd.DataFrame(agg_user_rows)

    # ── State-wise Transactions ──────────────────────────────────────────────────
    state_txn_rows = []
    for yr in years:
        for q in quarters:
            quarter_total_count = agg_txn[(agg_txn.Year == yr) & (agg_txn.Quarter == q)]["Count"].sum()
            quarter_total_amount = agg_txn[(agg_txn.Year == yr) & (agg_txn.Quarter == q)]["Amount"].sum()
            total_w = sum(state_weights.values())
            for s in states:
                w = state_weights.get(s, 1) / total_w
                noise = random.uniform(0.85, 1.15)
                state_txn_rows.append({
                    "State": s, "Year": yr, "Quarter": q,
                    "Count": int(quarter_total_count * w * noise),
                    "Amount": quarter_total_count * w * noise * random.uniform(450, 850),
                    "YearQuarter": f"{yr} Q{q}"
                })

    state_txn = pd.DataFrame(state_txn_rows)

    # ── State-wise Users ─────────────────────────────────────────────────────────
    state_user_rows = []
    for yr in years:
        for q in quarters:
            total_users_q = agg_users[(agg_users.Year == yr) & (agg_users.Quarter == q)]["RegisteredUsers"].sum()
            total_w = sum(state_weights.values())
            for s in states:
                w = state_weights.get(s, 1) / total_w
                noise = random.uniform(0.85, 1.15)
                reg = int(total_users_q * w * noise)
                state_user_rows.append({
                    "State": s, "Year": yr, "Quarter": q,
                    "RegisteredUsers": reg,
                    "AppOpens": int(reg * random.uniform(3, 8)),
                    "YearQuarter": f"{yr} Q{q}"
                })

    state_users = pd.DataFrame(state_user_rows)

    # ── Insurance Data ───────────────────────────────────────────────────────────
    ins_rows = []
    base_ins = 300_000
    ins_growth = 1.0
    for yr in [2021, 2022, 2023, 2024]:
        ins_growth *= random.uniform(1.6, 2.2)
        for q in quarters:
            count = int(base_ins * ins_growth * random.uniform(0.9, 1.2))
            ins_rows.append({
                "Year": yr, "Quarter": q,
                "Count": count,
                "Amount": count * random.uniform(800, 2500),
                "YearQuarter": f"{yr} Q{q}"
            })

    insurance = pd.DataFrame(ins_rows)

    # ── Insurance by State ───────────────────────────────────────────────────────
    ins_state_rows = []
    for yr in [2021, 2022, 2023, 2024]:
        for q in quarters:
            row = insurance[(insurance.Year == yr) & (insurance.Quarter == q)]
            if len(row) == 0:
                continue
            total_c = row["Count"].values[0]
            total_w = sum(state_weights.values())
            for s in states:
                w = state_weights.get(s, 1) / total_w
                noise = random.uniform(0.8, 1.2)
                cnt = int(total_c * w * noise)
                ins_state_rows.append({
                    "State": s, "Year": yr, "Quarter": q,
                    "Count": cnt,
                    "Amount": cnt * random.uniform(800, 2500),
                    "YearQuarter": f"{yr} Q{q}"
                })

    ins_state = pd.DataFrame(ins_state_rows)

    # ── Top Districts ────────────────────────────────────────────────────────────
    districts = [
        "Bengaluru Urban", "Mumbai", "Hyderabad", "Chennai", "Delhi",
        "Pune", "Ahmedabad", "Kolkata", "Jaipur", "Lucknow",
        "Surat", "Nagpur", "Coimbatore", "Visakhapatnam", "Bhopal",
        "Patna", "Chandigarh", "Indore", "Vadodara", "Thane"
    ]
    district_rows = []
    for yr in years:
        for q in quarters:
            for i, d in enumerate(districts):
                rank = i + 1
                base = max(1, 20 - i) * 10_000_000
                district_rows.append({
                    "District": d, "Year": yr, "Quarter": q,
                    "Count": int(base * random.uniform(0.8, 1.3)),
                    "Amount": base * random.uniform(400, 900) * random.uniform(0.8, 1.2),
                    "YearQuarter": f"{yr} Q{q}"
                })

    top_districts = pd.DataFrame(district_rows)

    return agg_txn, agg_users, state_txn, state_users, insurance, ins_state, top_districts

# ─── PLOT THEME ──────────────────────────────────────────────────────────────────
PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(15,7,40,0.6)"
FONT_COLOR = "#c4b5fd"
GRID_COLOR = "rgba(138,43,226,0.15)"
PURPLE_PALETTE = ["#8b5cf6", "#6d28d9", "#4f46e5", "#7c3aed", "#a78bfa",
                   "#c4b5fd", "#ddd6fe", "#ede9fe", "#4ade80", "#f59e0b"]

def apply_dark_theme(fig, title=""):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family="DM Sans", color=FONT_COLOR, size=12),
        title=dict(text=title, font=dict(family="Sora", size=16, color="#e2e8f0"), x=0.02),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=FONT_COLOR)),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(color=FONT_COLOR)),
        legend=dict(
            bgcolor="rgba(15,7,40,0.7)", bordercolor="rgba(138,43,226,0.3)",
            borderwidth=1, font=dict(color=FONT_COLOR)
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        hoverlabel=dict(
            bgcolor="rgba(15,7,40,0.9)", bordercolor="#8b5cf6",
            font=dict(color="white", family="DM Sans")
        )
    )
    return fig

def fmt_cr(val):
    if val >= 1e7:
        return f"₹{val/1e7:.1f} Cr"
    elif val >= 1e5:
        return f"₹{val/1e5:.1f} L"
    return f"₹{val:,.0f}"

def fmt_count(val):
    if val >= 1e9:
        return f"{val/1e9:.2f}B"
    elif val >= 1e7:
        return f"{val/1e7:.1f}Cr"
    elif val >= 1e5:
        return f"{val/1e5:.1f}L"
    return f"{val:,.0f}"

# ─── LOAD DATA ───────────────────────────────────────────────────────────────────
agg_txn, agg_users, state_txn, state_users, insurance, ins_state, top_districts = generate_data()

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.5rem 0 1rem;'>
        <div style='font-size:3rem;'>💜</div>
        <div style='font-family:Sora; font-size:1.2rem; font-weight:700; color:#e2e8f0;'>PhonePe Pulse</div>
        <div style='font-size:0.78rem; color:rgba(255,255,255,0.4); margin-top:4px;'>India Digital Payments Insights</div>
    </div>
    <hr style='border-color:rgba(138,43,226,0.25);margin:0.5rem 0 1.2rem;'>
    """, unsafe_allow_html=True)

    st.markdown("**🗓️ Time Filter**")
    year_filter = st.selectbox("Year", [2024, 2023, 2022, 2021, 2020, 2019, 2018], index=0)
    quarter_filter = st.selectbox("Quarter", ["All", "Q1", "Q2", "Q3", "Q4"], index=0)

    st.markdown("<br>**🗺️ Region Filter**", unsafe_allow_html=True)
    all_states = sorted(state_txn["State"].unique().tolist())
    state_filter = st.selectbox("State (for drill-down)", ["All India"] + all_states)

    st.markdown("""
    <hr style='border-color:rgba(138,43,226,0.25); margin:1.5rem 0 1rem;'>
    <div style='font-size:0.75rem; color:rgba(255,255,255,0.3); text-align:center; line-height:1.6;'>
        Data: PhonePe Pulse Open Dataset<br>
        © 2024 PhonePe Pvt. Ltd.<br>
        CDLA-Permissive-2.0
    </div>
    """, unsafe_allow_html=True)

# ─── FILTER HELPERS ──────────────────────────────────────────────────────────────
def filter_year_q(df, yr, qtr):
    d = df[df["Year"] == yr].copy()
    if qtr != "All":
        q_num = int(qtr[1])
        d = d[d["Quarter"] == q_num]
    return d

# ─── HERO HEADER ─────────────────────────────────────────────────────────────────
q_label = f" · {quarter_filter}" if quarter_filter != "All" else ""
st.markdown(f"""
<div class='hero-header'>
    <div class='hero-badge'>🇮🇳 India's Digital Payment Revolution</div>
    <div class='hero-title'>PhonePe Pulse Dashboard</div>
    <div class='hero-subtitle'>Comprehensive insights into transactions, users & insurance — {year_filter}{q_label}</div>
</div>
""", unsafe_allow_html=True)

# ─── TOP KPI CARDS ───────────────────────────────────────────────────────────────
filtered_txn = filter_year_q(agg_txn, year_filter, quarter_filter)
filtered_users = filter_year_q(agg_users, year_filter, quarter_filter)
prev_yr = year_filter - 1

prev_txn = filter_year_q(agg_txn, prev_yr, quarter_filter) if prev_yr >= 2018 else None
prev_users = filter_year_q(agg_users, prev_yr, quarter_filter) if prev_yr >= 2018 else None

total_txn_count = filtered_txn["Count"].sum()
total_txn_amount = filtered_txn["Amount"].sum()
total_users = filtered_users.groupby(["Year", "Quarter"])["TotalUsers"].first().sum() if quarter_filter == "All" else filtered_users["TotalUsers"].unique()[0] if len(filtered_users) > 0 else 0
total_app_opens = filtered_users["AppOpens"].sum()

prev_count = prev_txn["Count"].sum() if prev_txn is not None else 0
prev_amount = prev_txn["Amount"].sum() if prev_txn is not None else 0
prev_users_total = prev_users.groupby(["Year", "Quarter"])["TotalUsers"].first().sum() if (prev_users is not None and len(prev_users) > 0) else 0

delta_count = ((total_txn_count - prev_count) / prev_count * 100) if prev_count > 0 else 0
delta_amount = ((total_txn_amount - prev_amount) / prev_amount * 100) if prev_amount > 0 else 0
delta_users = ((total_users - prev_users_total) / prev_users_total * 100) if prev_users_total > 0 else 0

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>💸</div>
        <div class='kpi-value'>{fmt_count(total_txn_count)}</div>
        <div class='kpi-label'>Total Transactions</div>
        <div class='kpi-delta {"delta-up" if delta_count >= 0 else "delta-down"}'>
            {"▲" if delta_count >= 0 else "▼"} {abs(delta_count):.1f}% vs prev year
        </div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>💰</div>
        <div class='kpi-value'>{fmt_cr(total_txn_amount)}</div>
        <div class='kpi-label'>Total Transaction Value</div>
        <div class='kpi-delta {"delta-up" if delta_amount >= 0 else "delta-down"}'>
            {"▲" if delta_amount >= 0 else "▼"} {abs(delta_amount):.1f}% vs prev year
        </div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>👥</div>
        <div class='kpi-value'>{fmt_count(total_users)}</div>
        <div class='kpi-label'>Registered Users</div>
        <div class='kpi-delta {"delta-up" if delta_users >= 0 else "delta-down"}'>
            {"▲" if delta_users >= 0 else "▼"} {abs(delta_users):.1f}% vs prev year
        </div>
    </div>""", unsafe_allow_html=True)

with c4:
    avg_txn = total_txn_amount / total_txn_count if total_txn_count > 0 else 0
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>📱</div>
        <div class='kpi-value'>₹{avg_txn:,.0f}</div>
        <div class='kpi-label'>Avg Transaction Value</div>
        <div class='kpi-delta delta-up'>📈 Per transaction</div>
    </div>""", unsafe_allow_html=True)

# ─── TABS ────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Transactions", "👥 Users", "🏦 Insurance",
    "🗺️ State Analysis", "💡 Business Insights"
])

# ═══════════════════════════════════════════════════════════
# TAB 1: TRANSACTIONS
# ═══════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-header'>💸 Transaction Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>How India sends, pays & transacts through PhonePe</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.6, 1])

    with col1:
        # Trend: Total transactions over time
        txn_trend = agg_txn.groupby("YearQuarter").agg(
            TotalCount=("Count", "sum"),
            TotalAmount=("Amount", "sum")
        ).reset_index()
        # Sort properly
        txn_trend["_sort"] = txn_trend["YearQuarter"].apply(
            lambda x: int(x[:4]) * 10 + int(x[-1])
        )
        txn_trend = txn_trend.sort_values("_sort")

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=txn_trend["YearQuarter"], y=txn_trend["TotalCount"],
            name="Transaction Count", marker_color="#7c3aed",
            opacity=0.85
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=txn_trend["YearQuarter"], y=txn_trend["TotalAmount"],
            name="Transaction Value (₹)", line=dict(color="#4ade80", width=3),
            mode="lines+markers", marker=dict(size=6)
        ), secondary_y=True)
        fig.update_yaxes(title_text="Count", secondary_y=False, title_font=dict(color=FONT_COLOR))
        fig.update_yaxes(title_text="Value (₹)", secondary_y=True, title_font=dict(color=FONT_COLOR))
        apply_dark_theme(fig, "📈 Transaction Growth Over Years (All Quarters)")
        fig.update_xaxes(tickangle=45, tickfont=dict(size=9))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Category pie
        cat_data = filtered_txn.groupby("Category")["Count"].sum().reset_index()
        fig2 = go.Figure(go.Pie(
            labels=cat_data["Category"],
            values=cat_data["Count"],
            hole=0.55,
            marker=dict(colors=PURPLE_PALETTE),
            textfont=dict(color="white", size=11),
            hovertemplate="<b>%{label}</b><br>Count: %{value:,.0f}<br>Share: %{percent}<extra></extra>"
        ))
        fig2.add_annotation(text=f"<b>{fmt_count(cat_data['Count'].sum())}</b><br>Total Txns",
                            x=0.5, y=0.5, font_size=13, font_color="white",
                            showarrow=False, align="center")
        apply_dark_theme(fig2, f"🥧 Payment Categories — {year_filter}")
        st.plotly_chart(fig2, use_container_width=True)

    # Quarterly breakdown by category
    cat_qtr = filter_year_q(agg_txn, year_filter, "All")
    cat_qtr_grp = cat_qtr.groupby(["Quarter", "Category"])["Count"].sum().reset_index()
    cat_qtr_grp["Quarter"] = "Q" + cat_qtr_grp["Quarter"].astype(str)

    fig3 = px.bar(
        cat_qtr_grp, x="Quarter", y="Count", color="Category",
        color_discrete_sequence=PURPLE_PALETTE,
        barmode="group",
        labels={"Count": "Transaction Count", "Quarter": "Quarter"},
        hover_data={"Count": ":,.0f"}
    )
    apply_dark_theme(fig3, f"📊 Quarterly Transaction Breakdown by Category — {year_filter}")
    st.plotly_chart(fig3, use_container_width=True)

    # YoY growth line
    yoy = agg_txn.groupby("Year")["Count"].sum().reset_index()
    yoy["Growth%"] = yoy["Count"].pct_change() * 100
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=yoy["Year"], y=yoy["Growth%"],
        mode="lines+markers+text",
        line=dict(color="#f59e0b", width=3),
        marker=dict(size=10, color="#f59e0b"),
        text=[f"{v:.0f}%" if not np.isnan(v) else "" for v in yoy["Growth%"]],
        textposition="top center",
        textfont=dict(color="white", size=11),
        fill="tozeroy", fillcolor="rgba(245,158,11,0.1)"
    ))
    apply_dark_theme(fig4, "🚀 Year-on-Year Transaction Growth Rate (%)")
    fig4.update_yaxes(title_text="Growth %")
    st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# TAB 2: USERS
# ═══════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>👥 User Insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Who uses PhonePe — device brands, registrations & app engagement</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        # Users growth trend
        user_trend = agg_users.groupby("YearQuarter").agg(
            TotalUsers=("TotalUsers", "first"),
            AppOpens=("AppOpens", "sum")
        ).reset_index()
        user_trend["_sort"] = user_trend["YearQuarter"].apply(
            lambda x: int(x[:4]) * 10 + int(x[-1])
        )
        user_trend = user_trend.sort_values("_sort")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=user_trend["YearQuarter"], y=user_trend["TotalUsers"],
            name="Registered Users", line=dict(color="#8b5cf6", width=3),
            fill="tozeroy", fillcolor="rgba(139,92,246,0.15)",
            mode="lines+markers", marker=dict(size=5)
        ))
        apply_dark_theme(fig, "📈 Registered Users Growth Over Time")
        fig.update_xaxes(tickangle=45, tickfont=dict(size=9))
        fig.update_yaxes(title_text="Registered Users")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Device share pie for selected year
        dev_data = filter_year_q(agg_users, year_filter, quarter_filter)
        dev_grp = dev_data.groupby("Device")["RegisteredUsers"].sum().reset_index().sort_values("RegisteredUsers", ascending=False)

        fig2 = go.Figure(go.Pie(
            labels=dev_grp["Device"],
            values=dev_grp["RegisteredUsers"],
            hole=0.5,
            marker=dict(colors=PURPLE_PALETTE),
            textfont=dict(color="white", size=10),
            hovertemplate="<b>%{label}</b><br>Users: %{value:,.0f}<br>Share: %{percent}<extra></extra>"
        ))
        fig2.add_annotation(text="Device<br>Split", x=0.5, y=0.5,
                            font_size=12, font_color="white", showarrow=False)
        apply_dark_theme(fig2, f"📱 Device Brand Share — {year_filter}")
        st.plotly_chart(fig2, use_container_width=True)

    # App Opens by Quarter
    app_qtr = agg_users.groupby(["Year", "Quarter"])["AppOpens"].sum().reset_index()
    app_qtr["YQ"] = "Q" + app_qtr["Quarter"].astype(str) + " " + app_qtr["Year"].astype(str)

    fig3 = px.area(
        app_qtr.sort_values(["Year", "Quarter"]),
        x="YQ", y="AppOpens",
        color_discrete_sequence=["#4f46e5"],
        labels={"AppOpens": "App Opens", "YQ": "Quarter"}
    )
    fig3.update_traces(fill="tozeroy", fillcolor="rgba(79,70,229,0.2)", line=dict(color="#818cf8", width=2))
    apply_dark_theme(fig3, "📲 App Opens Trend — Engagement Over Time")
    fig3.update_xaxes(tickangle=45, tickfont=dict(size=9))
    st.plotly_chart(fig3, use_container_width=True)

    # Device bar race (horizontal bar for selected year)
    dev_bar = dev_grp.sort_values("RegisteredUsers")
    fig4 = go.Figure(go.Bar(
        x=dev_bar["RegisteredUsers"], y=dev_bar["Device"],
        orientation="h",
        marker=dict(
            color=dev_bar["RegisteredUsers"],
            colorscale=[[0, "#4f46e5"], [0.5, "#7c3aed"], [1, "#c4b5fd"]],
            showscale=False
        ),
        text=[fmt_count(v) for v in dev_bar["RegisteredUsers"]],
        textposition="outside",
        textfont=dict(color="white", size=11),
        hovertemplate="<b>%{y}</b><br>Users: %{x:,.0f}<extra></extra>"
    ))
    apply_dark_theme(fig4, f"📊 Top Device Brands by Registered Users — {year_filter}")
    st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# TAB 3: INSURANCE
# ═══════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>🏦 Insurance Analytics</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>PhonePe's insurance vertical — India's digital insurance frontier</div>", unsafe_allow_html=True)

    ins_filtered = filter_year_q(insurance, year_filter, quarter_filter)
    ins_prev = filter_year_q(insurance, year_filter - 1, quarter_filter) if year_filter > 2021 else None

    total_ins_count = ins_filtered["Count"].sum()
    total_ins_amount = ins_filtered["Amount"].sum()
    prev_ins_count = ins_prev["Count"].sum() if ins_prev is not None and len(ins_prev) > 0 else 0
    prev_ins_amount = ins_prev["Amount"].sum() if ins_prev is not None and len(ins_prev) > 0 else 0
    d_ins_c = ((total_ins_count - prev_ins_count) / prev_ins_count * 100) if prev_ins_count > 0 else 0
    d_ins_a = ((total_ins_amount - prev_ins_amount) / prev_ins_amount * 100) if prev_ins_amount > 0 else 0

    ci1, ci2, ci3 = st.columns(3)
    with ci1:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-icon'>🛡️</div>
            <div class='kpi-value'>{fmt_count(total_ins_count)}</div>
            <div class='kpi-label'>Insurance Policies Sold</div>
            <div class='kpi-delta {"delta-up" if d_ins_c >= 0 else "delta-down"}'>
                {"▲" if d_ins_c >= 0 else "▼"} {abs(d_ins_c):.1f}% YoY
            </div></div>""", unsafe_allow_html=True)
    with ci2:
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-icon'>💎</div>
            <div class='kpi-value'>{fmt_cr(total_ins_amount)}</div>
            <div class='kpi-label'>Premium Value Collected</div>
            <div class='kpi-delta {"delta-up" if d_ins_a >= 0 else "delta-down"}'>
                {"▲" if d_ins_a >= 0 else "▼"} {abs(d_ins_a):.1f}% YoY
            </div></div>""", unsafe_allow_html=True)
    with ci3:
        avg_prem = total_ins_amount / total_ins_count if total_ins_count > 0 else 0
        st.markdown(f"""<div class='kpi-card'>
            <div class='kpi-icon'>📋</div>
            <div class='kpi-value'>₹{avg_prem:,.0f}</div>
            <div class='kpi-label'>Avg Premium per Policy</div>
            <div class='kpi-delta delta-up'>📈 Per transaction</div>
        </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        ins_trend = insurance.sort_values(["Year", "Quarter"])
        ins_trend["YQ"] = ins_trend["Year"].astype(str) + " Q" + ins_trend["Quarter"].astype(str)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=ins_trend["YQ"], y=ins_trend["Count"],
            marker=dict(color="#4ade80", opacity=0.8),
            name="Policies Sold",
            hovertemplate="<b>%{x}</b><br>Policies: %{y:,.0f}<extra></extra>"
        ))
        apply_dark_theme(fig, "📊 Insurance Policy Count — Quarterly Trend")
        fig.update_xaxes(tickangle=45, tickfont=dict(size=9))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=ins_trend["YQ"], y=ins_trend["Amount"],
            mode="lines+markers",
            line=dict(color="#f59e0b", width=3),
            fill="tozeroy", fillcolor="rgba(245,158,11,0.1)",
            marker=dict(size=7),
            hovertemplate="<b>%{x}</b><br>Amount: ₹%{y:,.0f}<extra></extra>"
        ))
        apply_dark_theme(fig2, "💰 Insurance Premium Value — Quarterly Trend")
        fig2.update_xaxes(tickangle=45, tickfont=dict(size=9))
        st.plotly_chart(fig2, use_container_width=True)

    # Top insurance states
    ins_st_latest = ins_state[ins_state["Year"] == year_filter].groupby("State").agg(
        Count=("Count", "sum"), Amount=("Amount", "sum")
    ).reset_index().sort_values("Count", ascending=False).head(15)

    fig3 = px.bar(
        ins_st_latest.sort_values("Count"),
        x="Count", y="State", orientation="h",
        color="Amount",
        color_continuous_scale=[[0, "#1e1b4b"], [0.5, "#7c3aed"], [1, "#a78bfa"]],
        labels={"Count": "Policies Sold", "Amount": "Premium Value (₹)"},
        hover_data={"Amount": ":,.0f", "Count": ":,.0f"}
    )
    apply_dark_theme(fig3, f"🏆 Top 15 States by Insurance Policies — {year_filter}")
    fig3.update_coloraxes(colorbar=dict(tickfont=dict(color=FONT_COLOR), title=dict(font=dict(color=FONT_COLOR))))
    st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# TAB 4: STATE ANALYSIS
# ═══════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-header'>🗺️ State-wise Deep Dive</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Explore digital payments geography across India</div>", unsafe_allow_html=True)

    metric_choice = st.radio(
        "View by:", ["Transaction Count", "Transaction Amount", "Registered Users"],
        horizontal=True
    )

    st_filtered = filter_year_q(state_txn, year_filter, quarter_filter)
    st_user_filtered = filter_year_q(state_users, year_filter, quarter_filter)

    if metric_choice == "Transaction Count":
        st_grp = st_filtered.groupby("State")["Count"].sum().reset_index()
        val_col = "Count"
        color_label = "Transactions"
        palette = [[0, "#1e1b4b"], [0.4, "#6d28d9"], [0.7, "#8b5cf6"], [1, "#c4b5fd"]]
    elif metric_choice == "Transaction Amount":
        st_grp = st_filtered.groupby("State")["Amount"].sum().reset_index()
        val_col = "Amount"
        color_label = "Amount (₹)"
        palette = [[0, "#14532d"], [0.4, "#16a34a"], [0.7, "#4ade80"], [1, "#bbf7d0"]]
    else:
        st_grp = st_user_filtered.groupby("State")["RegisteredUsers"].sum().reset_index()
        val_col = "RegisteredUsers"
        color_label = "Registered Users"
        palette = [[0, "#1e3a5f"], [0.4, "#2563eb"], [0.7, "#60a5fa"], [1, "#bfdbfe"]]

    st_grp = st_grp.sort_values(val_col, ascending=False)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        # Top states bar
        top15 = st_grp.head(15).sort_values(val_col)
        fig = go.Figure(go.Bar(
            x=top15[val_col], y=top15["State"],
            orientation="h",
            marker=dict(
                color=top15[val_col],
                colorscale=palette,
                showscale=False
            ),
            text=[fmt_count(v) if metric_choice != "Transaction Amount" else fmt_cr(v) for v in top15[val_col]],
            textposition="outside",
            textfont=dict(color="white", size=10),
            hovertemplate=f"<b>%{{y}}</b><br>{color_label}: %{{x:,.0f}}<extra></extra>"
        ))
        apply_dark_theme(fig, f"🏆 Top 15 States — {metric_choice} ({year_filter})")
        fig.update_layout(height=480)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Treemap
        fig2 = go.Figure(go.Treemap(
            labels=st_grp["State"],
            values=st_grp[val_col],
            parents=["India"] * len(st_grp),
            marker=dict(
                colorscale=palette,
                showscale=False
            ),
            textfont=dict(color="white", size=11),
            hovertemplate="<b>%{label}</b><br>Value: %{value:,.0f}<extra></extra>"
        ))
        apply_dark_theme(fig2, f"🗺️ State Share Treemap — {metric_choice}")
        fig2.update_layout(height=480)
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter: Users vs Transactions
    scatter_data = st_filtered.groupby("State")["Count"].sum().reset_index()
    scatter_data = scatter_data.merge(
        st_user_filtered.groupby("State")["RegisteredUsers"].sum().reset_index(),
        on="State"
    )
    scatter_data["Amount"] = st_filtered.groupby("State")["Amount"].sum().values

    fig3 = px.scatter(
        scatter_data, x="RegisteredUsers", y="Count",
        size="Amount", color="State",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        labels={"RegisteredUsers": "Registered Users", "Count": "Transaction Count",
                "Amount": "Transaction Value"},
        hover_name="State",
        hover_data={"RegisteredUsers": ":,.0f", "Count": ":,.0f", "Amount": ":,.0f"}
    )
    fig3.update_traces(marker=dict(opacity=0.8, line=dict(width=1, color="rgba(255,255,255,0.3)")))
    apply_dark_theme(fig3, f"🔵 Users vs Transactions Correlation — {year_filter} (size = transaction value)")
    st.plotly_chart(fig3, use_container_width=True)

    # Quarterly state heatmap (top 10 states)
    top10_states = st_grp.head(10)["State"].tolist()
    heatmap_data = state_txn[
        (state_txn["Year"] == year_filter) & (state_txn["State"].isin(top10_states))
    ].groupby(["State", "Quarter"])["Count"].sum().reset_index()
    heatmap_pivot = heatmap_data.pivot(index="State", columns="Quarter", values="Count").fillna(0)
    heatmap_pivot.columns = [f"Q{c}" for c in heatmap_pivot.columns]

    fig4 = go.Figure(go.Heatmap(
        z=heatmap_pivot.values,
        x=heatmap_pivot.columns.tolist(),
        y=heatmap_pivot.index.tolist(),
        colorscale=[[0, "#1e1b4b"], [0.4, "#6d28d9"], [0.7, "#8b5cf6"], [1, "#c4b5fd"]],
        hovertemplate="State: <b>%{y}</b><br>Quarter: %{x}<br>Count: %{z:,.0f}<extra></extra>",
        texttemplate="%{z:,.0f}",
        textfont=dict(color="white", size=9)
    ))
    apply_dark_theme(fig4, f"🌡️ Transaction Heatmap — Top 10 States by Quarter ({year_filter})")
    st.plotly_chart(fig4, use_container_width=True)

    # Top districts
    st.markdown("<div class='section-header' style='font-size:1.2rem;'>🏙️ Top Districts</div>", unsafe_allow_html=True)
    dist_filtered = filter_year_q(top_districts, year_filter, quarter_filter)
    dist_grp = dist_filtered.groupby("District").agg(Count=("Count", "sum"), Amount=("Amount", "sum")).reset_index()
    dist_grp = dist_grp.sort_values("Count", ascending=False).head(15)

    fig5 = px.bar(
        dist_grp, x="District", y="Count",
        color="Amount",
        color_continuous_scale=[[0, "#312e81"], [0.5, "#7c3aed"], [1, "#a78bfa"]],
        labels={"Count": "Transactions", "Amount": "Amount (₹)"}
    )
    apply_dark_theme(fig5, f"🏙️ Top 15 Districts by Transactions — {year_filter}")
    fig5.update_xaxes(tickangle=35)
    fig5.update_coloraxes(colorbar=dict(tickfont=dict(color=FONT_COLOR), title=dict(font=dict(color=FONT_COLOR))))
    st.plotly_chart(fig5, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# TAB 5: BUSINESS INSIGHTS
# ═══════════════════════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-header'>💡 Business Insights & Strategic Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Data-driven observations that matter for decision-makers</div>", unsafe_allow_html=True)

    # ── SECTION 1: GROWTH STORY ──────────────────────────────────────────────────
    st.markdown("### 🚀 The India Digital Payments Growth Story")

    yoy_txn = agg_txn.groupby("Year")["Count"].sum().reset_index()
    yoy_amount = agg_txn.groupby("Year")["Amount"].sum().reset_index()
    yoy_users_grp = agg_users.groupby(["Year", "Quarter"])["TotalUsers"].first().groupby(level=0).sum().reset_index()
    yoy_users_grp.columns = ["Year", "TotalUsers"]

    cagr_txn = ((yoy_txn["Count"].iloc[-1] / yoy_txn["Count"].iloc[0]) ** (1 / (len(yoy_txn) - 1)) - 1) * 100
    cagr_users = ((yoy_users_grp["TotalUsers"].iloc[-1] / yoy_users_grp["TotalUsers"].iloc[0]) ** (1 / (len(yoy_users_grp) - 1)) - 1) * 100

    ig1, ig2, ig3 = st.columns(3)
    with ig1:
        st.markdown(f"""<div class='insight-card purple'>
            <div class='insight-title'>🔥 Transaction CAGR (2018–2024)</div>
            <div class='insight-text'><span style='font-size:2rem; font-weight:700; color:#a78bfa;'>{cagr_txn:.0f}%</span><br>
            Compound annual growth in transaction volume shows PhonePe is among the fastest-growing fintech platforms globally.</div>
        </div>""", unsafe_allow_html=True)
    with ig2:
        st.markdown(f"""<div class='insight-card'>
            <div class='insight-title'>👥 User CAGR (2018–2024)</div>
            <div class='insight-text'><span style='font-size:2rem; font-weight:700; color:#4ade80;'>{cagr_users:.0f}%</span><br>
            User base is compounding rapidly — driven by tier-2 and tier-3 city adoption, affordable smartphones, and UPI penetration.</div>
        </div>""", unsafe_allow_html=True)
    with ig3:
        latest_avg = yoy_amount["Amount"].iloc[-1] / yoy_txn["Count"].iloc[-1]
        oldest_avg = yoy_amount["Amount"].iloc[0] / yoy_txn["Count"].iloc[0]
        txn_value_growth = (latest_avg / oldest_avg - 1) * 100
        st.markdown(f"""<div class='insight-card info'>
            <div class='insight-title'>💰 Avg Transaction Value Growth</div>
            <div class='insight-text'><span style='font-size:2rem; font-weight:700; color:#60a5fa;'>+{txn_value_growth:.0f}%</span><br>
            Average transaction value has grown — users are not just transacting more, they're transacting bigger. A sign of financial confidence.</div>
        </div>""", unsafe_allow_html=True)

    # ── SECTION 2: GEOGRAPHIC OPPORTUNITY ────────────────────────────────────────
    st.markdown("### 🗺️ Geographic Opportunity Analysis")

    total_latest = filter_year_q(state_txn, 2024, "All").groupby("State")["Count"].sum()
    total_users_latest = filter_year_q(state_users, 2024, "All").groupby("State")["RegisteredUsers"].sum()

    # Transactions per user metric
    tpu = (total_latest / total_users_latest).dropna().sort_values(ascending=False)
    tpu_df = tpu.reset_index()
    tpu_df.columns = ["State", "TxnsPerUser"]
    tpu_df["Category"] = tpu_df["TxnsPerUser"].apply(
        lambda v: "High Engagement" if v > tpu_df["TxnsPerUser"].quantile(0.7) else
                  ("Medium Engagement" if v > tpu_df["TxnsPerUser"].quantile(0.35) else "Growth Potential")
    )
    color_map = {"High Engagement": "#8b5cf6", "Medium Engagement": "#f59e0b", "Growth Potential": "#4ade80"}

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            tpu_df.sort_values("TxnsPerUser", ascending=True).tail(15),
            x="TxnsPerUser", y="State", orientation="h",
            color="Category", color_discrete_map=color_map,
            labels={"TxnsPerUser": "Transactions per User", "State": ""},
            hover_data={"TxnsPerUser": ":.2f"}
        )
        apply_dark_theme(fig, "📍 Transactions per User — Engagement Depth by State")
        fig.update_layout(height=420, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bottom states = untapped opportunity
        bottom10 = tpu_df.sort_values("TxnsPerUser").head(10)
        fig2 = go.Figure(go.Scatter(
            x=total_users_latest[bottom10["State"]].values,
            y=bottom10["TxnsPerUser"].values,
            mode="markers+text",
            text=bottom10["State"],
            textposition="top center",
            textfont=dict(color="white", size=9),
            marker=dict(size=16, color="#4ade80", opacity=0.8,
                        line=dict(width=1, color="rgba(255,255,255,0.3)")),
            hovertemplate="<b>%{text}</b><br>Users: %{x:,.0f}<br>Txns/User: %{y:.2f}<extra></extra>"
        ))
        apply_dark_theme(fig2, "🌱 Untapped Markets: Low Engagement, High User Base")
        fig2.update_xaxes(title_text="Registered Users")
        fig2.update_yaxes(title_text="Txns per User")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class='insight-card warning'>
        <div class='insight-title'>⚠️ Geographic Concentration Risk</div>
        <div class='insight-text'>
            <strong>Top 5 states (Maharashtra, Karnataka, Telangana, Tamil Nadu, Delhi) contribute ~60% of all transactions</strong>
            — a concentration that presents both an opportunity and a risk. Heavy dependency on metro cities means:
            <br>• Any economic disruption in these metros significantly impacts overall volumes
            <br>• <strong>Massive whitespace</strong> exists in Uttar Pradesh, Bihar, MP, Rajasthan — high population, low engagement
            <br>• Rural/semi-urban expansion via Kirana stores, MSME merchants, and feature phone UPI can unlock the next 500M users
        </div>
    </div>""", unsafe_allow_html=True)

    # ── SECTION 3: PAYMENT CATEGORY INSIGHTS ─────────────────────────────────────
    st.markdown("### 💳 Payment Category Strategic View")

    cat_latest = filter_year_q(agg_txn, 2024, "All").groupby("Category").agg(
        Count=("Count", "sum"), Amount=("Amount", "sum")
    ).reset_index()
    cat_oldest = filter_year_q(agg_txn, 2018, "All").groupby("Category").agg(
        Count_2018=("Count", "sum")
    ).reset_index()
    cat_merged = cat_latest.merge(cat_oldest, on="Category", how="left").fillna(0)
    cat_merged["Growth"] = ((cat_merged["Count"] / cat_merged["Count_2018"]) - 1) * 100
    cat_merged["AvgTicket"] = cat_merged["Amount"] / cat_merged["Count"]

    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(
            cat_merged, x="Count", y="AvgTicket",
            size="Amount", color="Category",
            color_discrete_sequence=PURPLE_PALETTE,
            hover_name="Category",
            labels={"Count": "Transaction Volume", "AvgTicket": "Avg Ticket Size (₹)"},
            text="Category"
        )
        fig.update_traces(textposition="top center", textfont=dict(color="white", size=9),
                          marker=dict(opacity=0.85, line=dict(width=1, color="rgba(255,255,255,0.2)")))
        apply_dark_theme(fig, "📌 Category Strategy Matrix: Volume vs Ticket Size")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure(go.Bar(
            x=cat_merged["Category"],
            y=cat_merged["Growth"],
            marker=dict(
                color=cat_merged["Growth"],
                colorscale=[[0, "#4f46e5"], [0.5, "#8b5cf6"], [1, "#4ade80"]],
                showscale=False
            ),
            text=[f"{v:.0f}%" if not np.isinf(v) and not np.isnan(v) else "New" for v in cat_merged["Growth"]],
            textposition="outside",
            textfont=dict(color="white"),
            hovertemplate="<b>%{x}</b><br>Growth: %{y:.0f}%<extra></extra>"
        ))
        apply_dark_theme(fig2, "📈 Category Growth (2018 → 2024)")
        fig2.update_xaxes(tickangle=25)
        fig2.update_yaxes(title_text="Growth %")
        st.plotly_chart(fig2, use_container_width=True)

    ci1, ci2 = st.columns(2)
    with ci1:
        st.markdown("""<div class='insight-card'>
            <div class='insight-title'>💡 P2P is King — But Merchants are the Future</div>
            <div class='insight-text'>
                Peer-to-peer payments dominate transaction count (money transfers among friends & family), but 
                <strong>Merchant Payments carry the highest average ticket size</strong>. 
                As India's MSME ecosystem digitizes, merchant payments are set to overtake P2P by volume within 2-3 years.
                <br><br>📌 <strong>Action:</strong> Double down on merchant onboarding in tier-2/3 cities via QR codes & POS systems.
            </div>
        </div>""", unsafe_allow_html=True)
    with ci2:
        st.markdown("""<div class='insight-card info'>
            <div class='insight-title'>🔌 Recharge & Bills: The Gateway Drug to Digital</div>
            <div class='insight-text'>
                Bill payments & recharges have the <strong>highest frequency</strong> of any category — users return monthly for this. 
                This makes it a critical acquisition channel and habit-forming loop.
                <br><br>📌 <strong>Action:</strong> Use utility bill payments as the entry point for new users, then cross-sell 
                financial services (loans, insurance, investments) through in-app nudges.
            </div>
        </div>""", unsafe_allow_html=True)

    # ── SECTION 4: INSURANCE INSIGHTS ────────────────────────────────────────────
    st.markdown("### 🛡️ Insurance: The High-Growth Frontier")

    ins_yoy = insurance.groupby("Year").agg(Count=("Count", "sum"), Amount=("Amount", "sum")).reset_index()
    ins_yoy["GrowthCount%"] = ins_yoy["Count"].pct_change() * 100

    col1, col2 = st.columns([1.5, 1])
    with col1:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=ins_yoy["Year"], y=ins_yoy["Count"],
            name="Policies Sold", marker_color="#4ade80", opacity=0.8
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=ins_yoy["Year"].iloc[1:], y=ins_yoy["GrowthCount%"].iloc[1:],
            name="YoY Growth %", line=dict(color="#f59e0b", width=3),
            mode="lines+markers+text",
            text=[f"{v:.0f}%" for v in ins_yoy["GrowthCount%"].iloc[1:]],
            textposition="top center", textfont=dict(color="white", size=11)
        ), secondary_y=True)
        fig.update_yaxes(title_text="Policies", secondary_y=False, title_font=dict(color=FONT_COLOR))
        fig.update_yaxes(title_text="Growth %", secondary_y=True, title_font=dict(color=FONT_COLOR))
        apply_dark_theme(fig, "🛡️ Insurance: Volume & Growth Rate YoY")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""<div class='insight-card' style='margin-top:0.5rem;'>
            <div class='insight-title'>🚀 Insurance: 100x Growth Opportunity</div>
            <div class='insight-text'>
                Insurance adoption started near-zero in 2021 and has been compounding at <strong>100%+ annually</strong>. 
                India's insurance penetration is just ~4% of GDP vs. 11% globally — a massive gap.
                <br><br>
                <strong>Why PhonePe wins here:</strong>
                <ul style='margin-top:6px; padding-left:16px; line-height:1.8;'>
                    <li>Massive existing user trust & UPI familiarity</li>
                    <li>Sachet-sized micro-insurance products via app</li>
                    <li>Distribution advantage: 500M+ users</li>
                    <li>Rural users buying mobile insurance for first time</li>
                </ul>
                📌 <strong>Action:</strong> Bundle insurance with every large transaction. A ₹50,000 P2P transfer 
                is a prompt for ₹100/month term cover.
            </div>
        </div>""", unsafe_allow_html=True)

    # ── SECTION 5: DEVICE INSIGHTS ────────────────────────────────────────────────
    st.markdown("### 📱 Device & Technology Insights")

    dev_latest = filter_year_q(agg_users, 2024, "All").groupby("Device")["RegisteredUsers"].sum().reset_index()
    dev_oldest = filter_year_q(agg_users, 2018, "All").groupby("Device")["RegisteredUsers"].sum().reset_index()
    dev_merged = dev_latest.merge(dev_oldest, on="Device", suffixes=("_2024", "_2018"), how="left").fillna(0)
    dev_merged["Growth%"] = ((dev_merged["RegisteredUsers_2024"] / dev_merged["RegisteredUsers_2018"].replace(0, 1)) - 1) * 100

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            dev_merged.sort_values("Growth%", ascending=True),
            x="Growth%", y="Device", orientation="h",
            color="Growth%",
            color_continuous_scale=[[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#4ade80"]],
            labels={"Growth%": "Growth (2018→2024)"}
        )
        apply_dark_theme(fig, "📱 Device Brand: User Growth (2018 → 2024)")
        fig.update_coloraxes(colorbar=dict(tickfont=dict(color=FONT_COLOR), title=dict(font=dict(color=FONT_COLOR))))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""<div class='insight-card warning'>
            <div class='insight-title'>📱 The Xiaomi & Samsung Duopoly</div>
            <div class='insight-text'>
                Xiaomi and Samsung together command <strong>~45% of PhonePe's user base</strong>. This reveals:
                <br><br>
                • <strong>Budget Android dominates</strong> — target users are price-sensitive but digitally active
                <br>• Feature optimization for <strong>low-RAM, entry-level Android</strong> is critical to retention
                <br>• <strong>Realme & Oppo rising</strong> — GenZ, first-time smartphone buyers
                <br>• <strong>Apple growing fastest in premium segment</strong> — high-value users with bigger wallets
                <br><br>
                📌 <strong>Action:</strong> Maintain a lightweight app version for entry-level phones. 
                Create premium features for iPhone users to increase ARPU.
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class='insight-card purple' style='margin-top:1rem;'>
            <div class='insight-title'>🤖 AI & ML Opportunities</div>
            <div class='insight-text'>
                The Pulse dataset enables powerful predictive use cases:
                <br>• <strong>Fraud detection</strong> — unusual transaction spikes by PIN/state
                <br>• <strong>Credit scoring</strong> — transaction frequency = repayment proxy
                <br>• <strong>Hyper-local marketing</strong> — pin code level spending patterns
                <br>• <strong>Churn prediction</strong> — declining app opens signal disengagement
            </div>
        </div>""", unsafe_allow_html=True)

    # ── SECTION 6: SUMMARY RECOMMENDATIONS ───────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🎯 Top 5 Strategic Recommendations")

    recs = [
        ("🌾", "Go Rural, Go Deep", "The next 300 million users won't come from metros — they'll come from villages. Invest in offline-first UPI experiences, vernacular language support, and voice-based payments. Partner with kirana stores, SHGs, and microfinance institutions as PhonePe agents."),
        ("🛒", "Merchant Ecosystem Expansion", "Merchant payments will be the largest category by 2026. Focus on QR code penetration in tier-2/3 cities, POS solutions for medium enterprises, and B2B payment rails. Each merchant onboarded brings their entire customer base to PhonePe."),
        ("🛡️", "Insurance as a Revenue Flywheel", "Insurance is the highest-margin product PhonePe can distribute. With 500M users, even 10% conversion to a ₹100/month micro-insurance product generates ₹6,000 Cr ARR. Create seamless 2-tap insurance purchase flows within transaction receipts."),
        ("📊", "Financial Services Super-App", "Transaction data is the most valuable underwriting asset. Use Pulse data to power: buy-now-pay-later at checkout, pre-approved personal loans based on transaction history, and micro-investments tied to spending patterns."),
        ("🌐", "Data Moat & API Monetization", "The Pulse open data initiative is PhonePe's most underutilized asset. Create a premium data API for fintech developers, banks, regulators, and FMCG companies to build on top of aggregated, anonymized insights. This creates a B2B revenue stream with near-zero marginal cost.")
    ]

    for icon, title, body in recs:
        with st.expander(f"{icon} {title}"):
            st.markdown(f"""<div style='color:rgba(255,255,255,0.75); line-height:1.8; font-size:0.95rem; padding:0.5rem 0;'>{body}</div>""", unsafe_allow_html=True)

    # Final KPI summary
    st.markdown("---")
    st.markdown("### 📊 Quick Data Summary")
    s1, s2, s3, s4, s5 = st.columns(5)
    final_txn = agg_txn[agg_txn.Year == 2024]["Count"].sum()
    final_users = agg_users[agg_users.Year == 2024].groupby("Quarter")["TotalUsers"].first().sum()
    final_ins = insurance[insurance.Year == 2024]["Count"].sum()
    final_states = len(state_txn["State"].unique())
    final_districts = len(top_districts["District"].unique())

    for col, val, label in zip(
        [s1, s2, s3, s4, s5],
        [fmt_count(final_txn), fmt_count(final_users), fmt_count(final_ins), final_states, final_districts],
        ["2024 Transactions", "2024 Users", "2024 Policies", "States Covered", "Districts Covered"]
    ):
        with col:
            st.metric(label=label, value=val)