"""
S&P 500 Statistical Analysis — Finviz-style Streamlit App
Loads pre-generated PNG files from ./plots/ folder

Folder structure:
  sp500_finviz.py
  plots/
    Distribution of Descriptive Statistics (S&P 500 Stocks).png
    S&P 500 Index — 30-Day Rolling Statistics of Log Returns.png
    ... etc

Run: streamlit run sp500_finviz.py
"""

import streamlit as st
from PIL import Image
import os
from io import BytesIO

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="S&P 500 Statistical Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Finviz-style CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
  html, body, .stApp { background-color: #0d1117; color: #c9d1d9; font-family: Arial, sans-serif; }
  section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] span,
  section[data-testid="stSidebar"] label { color: #c9d1d9 !important; font-size: 13px; }

  .finviz-header {
    background: linear-gradient(90deg, #161b22 0%, #1f2937 100%);
    border-bottom: 2px solid #00d2ff;
    padding: 12px 20px;
    margin-bottom: 20px;
    display: flex; align-items: center; gap: 16px;
  }
  .finviz-header h1 { color: #00d2ff; font-size: 22px; font-weight: 700; margin: 0; letter-spacing: 1px; }
  .finviz-header span { color: #8b949e; font-size: 13px; }

  .section-title {
    background: #161b22;
    border-left: 3px solid #00d2ff;
    padding: 6px 12px;
    margin: 16px 0 10px 0;
    color: #ffffff;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
  }

  .chart-caption {
    color: #8b949e;
    font-size: 11px;
    margin-top: 4px;
    margin-bottom: 12px;
  }

  .insight-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 4px;
    padding: 12px 16px;
    font-size: 12px;
    line-height: 1.8;
    color: #c9d1d9;
    margin-bottom: 16px;
  }

  .stDownloadButton > button {
    background: #21262d !important;
    color: #00d2ff !important;
    border: 1px solid #30363d !important;
    border-radius: 3px !important;
    font-size: 11px !important;
    padding: 3px 12px !important;
  }
  .stDownloadButton > button:hover {
    background: #00d2ff !important;
    color: #0d1117 !important;
  }

  #MainMenu, footer, header { visibility: hidden; }
  ::-webkit-scrollbar { width: 6px; background: #0d1117; }
  ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
PLOTS_DIR = "plots"

def load_img(filename):
    path = os.path.join(PLOTS_DIR, filename + ".png")
    if os.path.exists(path):
        return Image.open(path)
    return None

def show_img(filename, caption=""):
    img = load_img(filename)
    if img:
        st.image(img, use_container_width=True)
        buf = BytesIO()
        img.save(buf, format="PNG")
        st.download_button(
            label="⬇ Download",
            data=buf.getvalue(),
            file_name=filename + ".png",
            mime="image/png",
            key="dl_" + filename.replace(" ", "_").replace("–", "-").replace("/", "_"),
        )
        if caption:
            st.markdown(f'<div class="chart-caption">{caption}</div>', unsafe_allow_html=True)
    else:
        st.warning(f"Image not found: `plots/{filename}.png`")

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="finviz-header">
  <h1>📊 S&P 500 STATISTICAL ANALYSIS</h1>
  <span>Gerry O'Brian &nbsp;·&nbsp; Mathilde Lafon &nbsp;·&nbsp; Camille Desurmont &nbsp;|&nbsp; 2016–2026 &nbsp;|&nbsp; 503 stocks</span>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📈 Navigation")
    page = st.radio("", [
        "Overview",
        "Q1 · Individual Stock Properties",
        "Q2 · Index Rolling Stats",
        "Q3 · Cross-Section",
        "Q4 · Pairwise Scatterplots",
        "Q5 · Stock–Index Correlation",
        "Q6 · Sector Correlations",
        "Q7 · Two Regimes",
        "Q8 · Is the World More Risky?",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:12px; color:#8b949e; line-height:1.8;">
    <b style="color:#00d2ff;">Key findings</b><br>
    • Returns are structurally non-Gaussian<br>
    • Index understates individual risk<br>
    • Market + sector co-movement factors<br>
    • Post-2021 is a different regime<br>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    section("Objective")
    insight("""
    <b style="color:#00d2ff;">Objective:</b> To characterise the full statistical distribution of S&amp;P 500 individual stock returns
    and assess whether the index is a faithful representation of its constituents' behaviour across time and market regimes.<br><br>
    <b style="color:#ff5252;">Central finding:</b> The S&amp;P 500 index is a poor representation of what its constituents actually experience.
    Diversification destroys kurtosis, compresses skewness, and masks a structural regime break that only the cross-section reveals.
    """)

    section("Statistical Measures")
    c1, c2, c3 = st.columns(3)
    measures = [
        ("Mean", "Average daily return — measures central tendency of the distribution"),
        ("Variance", "Average squared deviation from the mean — measures how spread out returns are"),
        ("Skewness", "Measures asymmetry — negative skewness means large losses are more frequent than large gains"),
        ("Kurtosis", "Measures tail weight — high kurtosis means extreme daily moves occur far more often than a normal distribution predicts"),
        ("P1", "1st percentile return — direct measure of tail risk on the worst days"),
        ("P99", "99th percentile return — direct measure of tail risk on the best days"),
    ]
    for i, (name, desc) in enumerate(measures):
        with [c1, c2, c3][i % 3]:
            st.markdown(f"""
            <div style="background:#161b22; border:1px solid #30363d; border-radius:4px;
                        padding:10px 14px; margin-bottom:8px;">
              <div style="color:#00d2ff; font-size:13px; font-weight:700;">{name}</div>
              <div style="color:#c9d1d9; font-size:12px; margin-top:4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    section("Agenda")
    items = [
        ("01", "Q1", "Individual Stock Properties", "Non-Gaussian returns, skewness, kurtosis"),
        ("02", "Q2", "Index Rolling Stats", "30-day rolling moments of the S&P 500 index"),
        ("03", "Q3", "Cross-Section", "Daily stats across all 503 stocks"),
        ("04", "Q4", "Pairwise Scatterplots", "How stock characteristics relate to each other"),
        ("05", "Q5", "Stock–Index Correlation", "Common market factor, mean 0.55"),
        ("06", "Q6", "Sector Correlations", "Within (0.44) vs between (0.32) sector"),
        ("07", "Q7", "Two Regimes", "Pre-2020 calm baseline vs Post-2021 macro-driven"),
        ("08", "Q8", "Is the World More Risky?", "KS test + rolling variance regime comparison"),
    ]
    c1, c2 = st.columns(2)
    for i, (num, q, title, sub) in enumerate(items):
        with (c1 if i % 2 == 0 else c2):
            st.markdown(f"""
            <div style="background:#161b22; border:1px solid #30363d; border-radius:4px;
                        padding:10px 14px; margin-bottom:8px; display:flex; gap:12px; align-items:center;">
              <div style="color:#00d2ff; font-size:18px; font-weight:700; min-width:28px;">{num}</div>
              <div>
                <div style="color:#ffffff; font-size:13px; font-weight:600;">{q}: {title}</div>
                <div style="color:#8b949e; font-size:11px;">{sub}</div>
              </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Q1
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Q1 · Individual Stock Properties":
    section("Q1 — Distribution of Descriptive Statistics (S&P 500 Stocks)")
    insight("""
    <b style="color:#00d2ff;">Small positive mean:</b> Average daily log return ~0.05%, confirming the equity risk premium at daily frequency.<br>
    <b style="color:#ffab40;">Negative skewness:</b> Most stocks exhibit left-skewed returns — large drops are more frequent than equivalent gains.<br>
    <b style="color:#ff5252;">High excess kurtosis:</b> Median kurtosis ~12, confirming extreme daily moves occur far more often than a Gaussian model predicts.<br>
    <b style="color:#ffffff;">Takeaway:</b> High excess kurtosis and negative skewness are structural features of individual equity returns, not anomalies.
    Statistical normality tests firmly reject Gaussianity for the vast majority of S&amp;P 500 stocks.
    """)
    show_img("Distribution of Descriptive Statistics (S&P 500 Stocks)")

# ══════════════════════════════════════════════════════════════════════════════
# Q2
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Q2 · Index Rolling Stats":
    section("Q2 — S&P 500 Index: 30-Day Rolling Statistics of Log Returns")
    insight("""
    <b style="color:#00d2ff;">Rolling variance</b> spikes sharply at systematic events (COVID-19, early 2025), but peaks at ~30 —
    attenuated by the diversified weighting of the index.<br>
    <b style="color:#ffab40;">Rolling skewness</b> stays close to zero: gains and losses at the index level are roughly symmetric,
    because stocks pulling in opposite directions cancel each other out.<br>
    <b style="color:#ff5252;">Excess kurtosis</b> peaks at ~14: extreme return events at the individual stock level are averaged away,
    making tail risk appear far smaller than it actually is.
    """)
    show_img("S&P 500 Index — 30-Day Rolling Statistics of Log Returns")

# ══════════════════════════════════════════════════════════════════════════════
# Q3
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Q3 · Cross-Section":
    section("Q3 — Daily Cross-Sectional Statistics of S&P 500 Stock Returns")
    insight("""
    <b style="color:#00d2ff;">Cross-sectional variance</b> peaks above 60 at the same events as the index — twice the index's peak of ~30.<br>
    <b style="color:#ffab40;">Skewness</b> swings between −15 and +15 vs −2 to +1 for the index:
    a single stock with an extreme move on any given day can tilt the entire distribution.<br>
    <b style="color:#ff5252;">Kurtosis</b> peaks ~350 — 25× the index measure of ~14. Fat tails that are omnipresent in the cross-section
    are almost completely invisible at the index level.<br>
    <b style="color:#ffffff;">Takeaway:</b> The index hides what individual stocks actually experience.
    """)
    show_img("Daily Cross-Sectional Statistics of S&P 500 Stock Returns")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Cross-Sectional Density — 3D Surface")
    show_img("Daily Cross-Sectional Density of S&P 500 Stock Returns")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Cross-Sectional Density — Heatmap")
    show_img("Daily Cross-Sectional Density of S&P 500 Stock Returns - Heatmap")

# ══════════════════════════════════════════════════════════════════════════════
# Q4
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Q4 · Pairwise Scatterplots":
    section("Q4 — Pairwise Scatterplots of Descriptive Statistics (S&P 500 Stocks)")
    insight("""
    <b style="color:#00d2ff;">Variance · P1 · P99 · Kurtosis</b> are all strongly correlated —
    volatile stocks are fat-tailed in both directions simultaneously.<br>
    <b style="color:#ffab40;">Skewness vs Kurtosis</b> shows a quadratic relationship: any strong asymmetry,
    whether from crashes or jumps, drives kurtosis up.<br>
    <b style="color:#ff5252;">Mean return</b> is essentially uncorrelated with everything else —
    a stock's average return tells you nothing about the shape of its distribution.<br>
    <b style="color:#ffffff;">Takeaway:</b> The cross-section is defined by dispersion and tail risk, not by average returns.
    """)
    show_img("Pairwise Scatterplots of Descriptive Statistics (S&P 500 Stocks)")

# ══════════════════════════════════════════════════════════════════════════════
# Q5
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Q5 · Stock–Index Correlation":
    section("Q5 — Distribution of Stock–Index Correlations (S&P 500)")
    insight("""
    <b style="color:#00d2ff;">Every S&amp;P 500 stock is positively correlated with the index</b> —
    range 0.16 to 0.80, mean 0.55. No stock has a near-zero or negative correlation.<br>
    <b style="color:#00e676;">Most correlated:</b> large financials and mega-cap tech (BLK, MSFT, TROW) —
    their revenues are directly tied to market conditions.<br>
    <b style="color:#ff5252;">Least correlated:</b> consumer staples and idiosyncratic names (KR, CPB, MRNA) —
    driven by firm-specific factors largely independent of market direction.<br>
    <b style="color:#ffffff;">Takeaway:</b> A single dominant market factor explains most return co-movement.
    In a broad market crash, essentially all stocks fall together.
    """)
    show_img("Distribution of Stock–Index Correlations (S&P 500)")

# ══════════════════════════════════════════════════════════════════════════════
# Q6
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Q6 · Sector Correlations":
    section("Q6 — Distribution of All Pairwise Stock Correlations (S&P 500)")
    insight("""
    The full pairwise distribution covers 126,253 unique stock pairs.
    Overall mean correlation is 0.33 — lower than the stock-to-index correlation (0.55)
    because the index aggregates away firm-specific noise.
    """)
    show_img("Distribution of All Pairwise Stock Correlations (S&P 500)")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Within-Sector vs Between-Sector Pairwise Correlations (S&P 500)")
    insight("""
    <b style="color:#00e676;">Within-sector</b> correlations (mean 0.44) systematically exceed
    <b style="color:#ff5252;">between-sector</b> correlations (mean 0.32) —
    confirmed by Mann-Whitney U test (p ≈ 0.00).<br>
    Stocks in the same sector share common fundamental drivers (commodity prices for Energy,
    rate sensitivity for Financials) that cause them to move together more than cross-sector pairs.<br>
    <b style="color:#ffffff;">Takeaway:</b> Two layers of co-movement — a market factor synchronising all stocks,
    and a sector factor creating tighter clusters within industries.
    """)
    show_img("Within-Sector vs Between-Sector Pairwise Correlations (S&P 500)")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Average Pairwise Correlation Between and Within Sectors")
    insight("""
    <b style="color:#00e676;">Energy (0.59) and Utilities (0.58)</b> — tightest clusters, driven by oil prices and rate sensitivity.<br>
    <b style="color:#ffab40;">Financials (0.51) and Real Estate (0.55)</b> — both highly sensitive to interest rate movements.<br>
    <b style="color:#ff5252;">Consumer Staples vs Energy (0.18)</b> — most insulated cross-sector pair, entirely different macro drivers.
    """)
    show_img("Average Pairwise Correlation Between and Within Sectors")

# ══════════════════════════════════════════════════════════════════════════════
# Q7
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Q7 · Two Regimes":
    section("Q7 — Two Regimes: Pre-2020 vs Post-2021")
    insight("""
    <b style="color:#00e676;">Pre-2020:</b> Variance touches near zero between spikes — stocks move almost in lockstep on calm days.
    Skewness oscillates widely between ±15. Kurtosis spikes episodically to ~350 then reverts.<br>
    <b style="color:#ff5252;">Post-2021:</b> Variance floor shifts up permanently to 3–5 even on calm days.
    Skewness is visibly compressed — macro-driven moves affect stocks more uniformly.
    Kurtosis unchanged — fat tails are regime-invariant.<br>
    <b style="color:#ffffff;">Takeaway:</b> Post-2021 is a genuinely different regime. The index understates it — the cross-section reveals it.
    """)

    section("Index Rolling Statistics — Pre-2020 vs Post-2021")
    c1, c2 = st.columns(2)
    with c1:
        show_img("S&P 500 Index — 30-Day Rolling Statistics of Log Returns before 2020")
    with c2:
        show_img("S&P 500 Index — 30-Day Rolling Statistics of Log Returns after 2021")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Cross-Sectional Statistics — Pre-2020 vs Post-2021")
    c1, c2 = st.columns(2)
    with c1:
        show_img("Daily Cross-Sectional Statistics of S&P 500 Stock Returns pre-2020")
    with c2:
        show_img("Daily Cross-Sectional Statistics of S&P 500 Stock Returns post-2020")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Cross-Sectional Density Heatmaps — Pre-2020 vs Post-2021")
    c1, c2 = st.columns(2)
    with c1:
        show_img("Daily Cross-Sectional Density of S&P 500 Stock Returns Pre-2020 - Heatmap")
    with c2:
        show_img("Daily Cross-Sectional Density of S&P 500 Stock Returns Post-2020 - Heatmap")

    st.markdown("<br>", unsafe_allow_html=True)
    section("Cross-Sectional Density 3D — Post-2021")
    show_img("Daily Cross-Sectional Density of S&P 500 Stock Returns Post-2020")

# ══════════════════════════════════════════════════════════════════════════════
# Q8
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Q8 · Is the World More Risky?":
    section("Q8 — Is the World Becoming More Risky? Rolling Variance of S&P 500 (2016–2026)")
    insight("""
    <b style="color:#00d2ff;">KS Test:</b> Strongly rejects H0 (p ≈ 2.9e-05) — pre-2020 and post-2021 distributions are statistically distinguishable.<br>
    <b style="color:#00e676;">Pre-2020:</b> 252-day variance consistently below 1 — the low-volatility, central-bank-supported era.<br>
    <b style="color:#ff5252;">Post-2021:</b> Baseline variance ~1.0–1.5, roughly double pre-2020.
    COVID crash produced the largest single spike (peak ~16 on 60-day measure).<br>
    <b style="color:#ffffff;">Verdict:</b> Yes — but moderately. The risk floor has shifted up, gradually mean-reverting rather than persistently escalating.
    """)
    show_img("Is the World Becoming More Risky? Rolling Variance of S&P 500 (2016–2026)")
