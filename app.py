import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# Premium CSS
# ==========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background:
        radial-gradient(circle at 12% 15%, rgba(37,99,235,0.09) 0%, transparent 45%),
        radial-gradient(circle at 88% 8%, rgba(16,185,129,0.09) 0%, transparent 45%),
        #f4f7fb;
}

.block-container {
    padding-top: 1.2rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1550px;
}

/* Hero */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(120deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
    padding: 42px 40px;
    border-radius: 26px;
    color: white;
    box-shadow: 0 18px 40px rgba(15,23,42,0.25);
    margin-bottom: 30px;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60%; right: -10%;
    width: 120%; height: 220%;
    background: radial-gradient(circle, rgba(255,255,255,0.10) 0%, transparent 60%);
    transform: rotate(8deg);
}
.hero h1 {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 6px;
    position: relative;
}
.hero p {
    opacity: 0.88;
    font-size: 1.02rem;
    position: relative;
    color: #e2e8f0 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] .stSelectbox label { font-weight: 600; }

/* Section titles */
.section-title {
    font-size: 1.25rem;
    font-weight: 800;
    color: #111827;
    margin: 4px 0 14px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title .accent {
    width: 6px;
    height: 20px;
    border-radius: 4px;
    background: linear-gradient(180deg, #2563eb, #10b981);
    display: inline-block;
}

/* KPI cards */
.kpi-card {
    background: white;
    border-radius: 20px;
    padding: 20px 22px;
    box-shadow: 0 8px 22px rgba(15,23,42,0.06);
    border: 1px solid rgba(15,23,42,0.04);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.kpi-card:hover { transform: translateY(-5px); box-shadow: 0 16px 30px rgba(15,23,42,0.10); }
.kpi-label { font-size: 0.82rem; font-weight: 600; color: #6b7280; margin-bottom: 4px; }
.kpi-value { font-size: 1.7rem; font-weight: 800; color: #111827; }
.kpi-sub { font-size: 0.78rem; color: #9ca3af; margin-top: 2px; }

/* Chart card wrapper */
.chart-card {
    background: white;
    border-radius: 22px;
    padding: 18px 20px 6px 20px;
    box-shadow: 0 8px 22px rgba(15,23,42,0.06);
    border: 1px solid rgba(15,23,42,0.04);
    margin-bottom: 22px;
}

.footer-note {
    text-align: center;
    color: #94a3b8;
    font-size: 0.8rem;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["month_name"] = df["datetime"].dt.month_name()
    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.day_name()
    df["season"] = df["season"].map({
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter",
    })
    df["weather_label"] = df["weather"].map({
        1: "Clear",
        2: "Mist / Cloudy",
        3: "Light Rain / Snow",
        4: "Heavy Rain / Storm",
    })
    return df


df = load_data()

DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ==========================================================
# HERO
# ==========================================================

st.markdown("""
<div class="hero">
    <h1>🚲 Bike Sharing Demand Dashboard</h1>
    <p>Interactive analysis of Washington D.C. bike rentals (2011–2012)</p>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.markdown("## 📊 Filters")
st.sidebar.markdown("---")

year = st.sidebar.selectbox("Select Year", sorted(df["year"].unique()))

season = st.sidebar.selectbox(
    "Select Season",
    ["All", "Spring", "Summer", "Fall", "Winter"],
)

working = st.sidebar.selectbox(
    "Day Type",
    ["All Days", "Working Days Only", "Non-Working Days Only"],
)

st.sidebar.markdown("---")
st.sidebar.caption("Data source: Capital Bikeshare, Washington D.C.")

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered = df[df["year"] == year]

if season != "All":
    filtered = filtered[filtered["season"] == season]

if working == "Working Days Only":
    filtered = filtered[filtered["workingday"] == 1]
elif working == "Non-Working Days Only":
    filtered = filtered[filtered["workingday"] == 0]

if filtered.empty:
    st.warning("No data matches the selected filters. Try a different combination.")
    st.stop()

# ==========================================================
# KPI ROW
# ==========================================================

st.markdown('<div class="section-title"><span class="accent"></span>Key Metrics</div>', unsafe_allow_html=True)

total_rentals = int(filtered["count"].sum())
avg_hourly = filtered["count"].mean()
peak_hour = filtered.groupby("hour")["count"].mean().idxmax()
busiest_day = filtered.groupby("day_of_week")["count"].mean().idxmax()

k1, k2, k3, k4 = st.columns(4)

kpis = [
    ("Total Rentals", f"{total_rentals:,}", "in selected period"),
    ("Avg. Rentals / Hour", f"{avg_hourly:,.0f}", "across filtered records"),
    ("Peak Hour", f"{peak_hour}:00", "highest average demand"),
    ("Busiest Day", busiest_day, "highest average demand"),
]

for col, (label, value, sub) in zip([k1, k2, k3, k4], kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ==========================================================
# CHART THEME
# ==========================================================

PLOTLY_TEMPLATE = "plotly_white"
ACCENT = "#2563eb"
ACCENT2 = "#10b981"

def style_fig(fig, height=380):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(family="Plus Jakarta Sans, sans-serif", size=13, color="#111827"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig

# ==========================================================
# ROW 1 — Hourly trend / Season
# ==========================================================

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span class="accent"></span>Average Rentals by Hour</div>', unsafe_allow_html=True)
    hourly = filtered.groupby("hour", as_index=False)["count"].mean()
    fig = px.line(hourly, x="hour", y="count", markers=True,
                  color_discrete_sequence=[ACCENT])
    fig.update_traces(line=dict(width=3), fill="tozeroy",
                       fillcolor="rgba(37,99,235,0.08)")
    fig.update_xaxes(title="Hour of Day", dtick=2)
    fig.update_yaxes(title="Avg. Rentals")
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span class="accent"></span>Average Rentals by Season</div>', unsafe_allow_html=True)
    season_avg = filtered.groupby("season", as_index=False)["count"].mean()
    fig = px.bar(season_avg, x="season", y="count", color="season",
                 color_discrete_sequence=[ACCENT, ACCENT2, "#f59e0b", "#8b5cf6"],
                 text_auto=".0f")
    fig.update_traces(textposition="outside")
    fig.update_xaxes(title="Season")
    fig.update_yaxes(title="Avg. Rentals")
    fig.update_layout(showlegend=False)
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# ROW 2 — Monthly trend / Weather impact
# ==========================================================

c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span class="accent"></span>Monthly Trend</div>', unsafe_allow_html=True)
    monthly = filtered.groupby(["month", "month_name"], as_index=False)["count"].mean().sort_values("month")
    fig = px.line(monthly, x="month_name", y="count", markers=True,
                  color_discrete_sequence=[ACCENT2])
    fig.update_traces(line=dict(width=3), fill="tozeroy",
                       fillcolor="rgba(16,185,129,0.08)")
    fig.update_xaxes(title="Month")
    fig.update_yaxes(title="Avg. Rentals")
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span class="accent"></span>Weather Impact</div>', unsafe_allow_html=True)
    weather_avg = filtered.groupby("weather_label", as_index=False)["count"].agg(
        mean_count=("count", "mean"), std_count=("count", "std")
    )
    fig = px.bar(weather_avg, x="weather_label", y="mean_count",
                 error_y="std_count", color="weather_label",
                 color_discrete_sequence=["#10b981", "#3b82f6", "#f59e0b", "#ef4444"],
                 text_auto=".0f")
    fig.update_traces(textposition="outside")
    fig.update_xaxes(title="Weather Condition")
    fig.update_yaxes(title="Avg. Rentals")
    fig.update_layout(showlegend=False)
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# ROW 3 — Day of week / Registered vs Casual
# ==========================================================

c5, c6 = st.columns(2)

with c5:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span class="accent"></span>Rentals by Day of Week</div>', unsafe_allow_html=True)
    dow = filtered.groupby("day_of_week", as_index=False)["count"].mean()
    dow["day_of_week"] = pd.Categorical(dow["day_of_week"], categories=DAY_ORDER, ordered=True)
    dow = dow.sort_values("day_of_week")
    fig = px.bar(dow, x="day_of_week", y="count", text_auto=".0f",
                 color_discrete_sequence=[ACCENT])
    fig.update_traces(textposition="outside", marker_color=ACCENT)
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Avg. Rentals")
    st.plotly_chart(style_fig(fig), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c6:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><span class="accent"></span>Registered vs. Casual Riders</div>', unsafe_allow_html=True)
    if {"registered", "casual"}.issubset(filtered.columns):
        rc = filtered.groupby("hour", as_index=False)[["registered", "casual"]].mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=rc["hour"], y=rc["registered"], name="Registered",
                                  mode="lines", line=dict(width=3, color=ACCENT),
                                  fill="tozeroy", fillcolor="rgba(37,99,235,0.08)"))
        fig.add_trace(go.Scatter(x=rc["hour"], y=rc["casual"], name="Casual",
                                  mode="lines", line=dict(width=3, color="#f59e0b"),
                                  fill="tozeroy", fillcolor="rgba(245,158,11,0.08)"))
        fig.update_xaxes(title="Hour of Day", dtick=2)
        fig.update_yaxes(title="Avg. Riders")
        st.plotly_chart(style_fig(fig), use_container_width=True)
    else:
        st.info("Columns 'registered' and 'casual' not found in this dataset.")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title"><span class="accent"></span>Correlation Heatmap</div>', unsafe_allow_html=True)

corr = filtered.corr(numeric_only=True)
fig = px.imshow(
    corr,
    color_continuous_scale="RdBu_r",
    zmin=-1, zmax=1,
    text_auto=".2f",
    aspect="auto",
)
fig.update_layout(
    template=PLOTLY_TEMPLATE,
    height=520,
    margin=dict(l=10, r=10, t=20, b=10),
    font=dict(family="Plus Jakarta Sans, sans-serif", size=12, color="#111827"),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# DATA EXPORT
# ==========================================================

st.markdown('<div class="section-title"><span class="accent"></span>Export Filtered Data</div>', unsafe_allow_html=True)

exp_col, _ = st.columns([1, 3])
with exp_col:
    st.download_button(
        label="⬇️ Download Filtered CSV",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name=f"bike_rentals_{year}_{season}.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown('<p class="footer-note">Bike Sharing Demand Dashboard · Data: Capital Bikeshare, Washington D.C. (2011–2012)</p>', unsafe_allow_html=True)
