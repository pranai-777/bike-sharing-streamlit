import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bike Sharing Demand Intelligence",
    page_icon="🚲",
    layout="wide"
)


# ============================================================
# PREMIUM COLOR PALETTE
# ============================================================

TEAL = "#3FB8AF"
COPPER = "#D98E5B"
ORCHID = "#A77BCA"
SAGE = "#8FAF9B"
ROSE = "#C86B85"
STEEL = "#5B8DB8"
SAND = "#D8B477"

BACKGROUND = "#081313"
CARD = "#101D1D"
TEXT = "#F4F1EA"
MUTED = "#9AA9A5"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   MAIN APPLICATION
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at 8% 8%,
            rgba(63,184,175,0.08),
            transparent 24%
        ),
        radial-gradient(
            circle at 92% 15%,
            rgba(167,123,202,0.06),
            transparent 25%
        ),
        #081313;

    color: #F4F1EA;
}


/* =========================================================
   MAIN CONTAINER
   ========================================================= */

.block-container {
    max-width: 1500px;
    padding-top: 30px;
    padding-bottom: 50px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0A1717,
            #0C1B1A
        );

    border-right:
        1px solid rgba(63,184,175,0.20);
}

section[data-testid="stSidebar"] * {
    color: #F4F1EA !important;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {

    background:
        radial-gradient(
            circle at 85% 20%,
            rgba(63,184,175,0.10),
            transparent 25%
        ),

        radial-gradient(
            circle at 70% 90%,
            rgba(217,142,91,0.08),
            transparent 25%
        ),

        linear-gradient(
            135deg,
            rgba(63,184,175,0.10),
            rgba(16,29,29,0.98)
        );

    border:
        1px solid rgba(63,184,175,0.25);

    border-radius:
        22px;

    padding:
        38px 42px;

    margin-bottom:
        28px;

    box-shadow:
        0 20px 60px rgba(0,0,0,0.30);
}


/* =========================================================
   HERO LABEL
   ========================================================= */

.hero-label {

    color: #3FB8AF;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 3px;

    margin-bottom: 10px;
}


/* =========================================================
   HERO TITLE
   ========================================================= */

.hero-title {

    color: #F4F1EA;

    font-size: 46px;

    font-weight: 700;

    line-height: 1.08;

    margin-bottom: 12px;
}

.hero-title span {
    color: #D98E5B;
}


/* =========================================================
   HERO DESCRIPTION
   ========================================================= */

.hero-text {

    color: #A8B4B0;

    font-size: 15px;

    line-height: 1.7;

    max-width: 780px;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {

    color: #F4F1EA;

    font-size: 21px;

    font-weight: 600;

    margin-top: 30px;

    margin-bottom: 15px;

    border-left:
        3px solid #3FB8AF;

    padding-left:
        11px;
}


/* =========================================================
   KPI CARDS
   ========================================================= */

.kpi {

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.015)
        );

    border-radius:
        16px;

    padding:
        20px;

    min-height:
        112px;

    border:
        1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 12px 35px rgba(0,0,0,0.20);
}


.kpi-teal {
    border-color:
        rgba(63,184,175,0.35);
}


.kpi-copper {
    border-color:
        rgba(217,142,91,0.35);
}


.kpi-orchid {
    border-color:
        rgba(167,123,202,0.35);
}


.kpi-sage {
    border-color:
        rgba(143,175,155,0.35);
}


.kpi-label {

    color: #93A19D;

    font-size: 11px;

    text-transform: uppercase;

    letter-spacing: 1.5px;
}


.kpi-value {

    color: #F4F1EA;

    font-size: 29px;

    font-weight: 700;

    margin-top: 8px;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {

    border:
        1px solid rgba(63,184,175,0.16);

    border-radius:
        12px;

    overflow:
        hidden;
}


/* =========================================================
   BUTTON
   ========================================================= */

.stDownloadButton button {

    background:
        linear-gradient(
            135deg,
            #3FB8AF,
            #5B8DB8
        );

    color:
        #081313;

    border:
        none;

    font-weight:
        700;

    border-radius:
        9px;
}


/* =========================================================
   INPUTS
   ========================================================= */

input {

    color:
        #F4F1EA !important;

    background-color:
        rgba(255,255,255,0.035) !important;
}


/* =========================================================
   DIVIDER
   ========================================================= */

hr {

    border-color:
        rgba(63,184,175,0.15);
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {

    text-align:
        center;

    color:
        #899894;

    font-size:
        12px;

    padding:
        25px;
}


.footer-title {

    color:
        #3FB8AF;

    font-weight:
        600;

    letter-spacing:
        1px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("train.csv")

    df["datetime"] = pd.to_datetime(
        df["datetime"]
    )

    df["year"] = (
        df["datetime"].dt.year
    )

    df["month"] = (
        df["datetime"].dt.month
    )

    df["hour"] = (
        df["datetime"].dt.hour
    )

    df["day_of_week"] = (
        df["datetime"].dt.day_name()
    )

    df["season"] = df["season"].map(
        {
            1: "Spring",
            2: "Summer",
            3: "Fall",
            4: "Winter"
        }
    )

    df["weather_label"] = df["weather"].map(
        {
            1: "Clear",
            2: "Cloudy",
            3: "Light Rain / Snow",
            4: "Heavy Rain / Snow"
        }
    )

    return df


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_data()

except Exception as e:

    st.error(
        "Unable to load train.csv"
    )

    st.code(str(e))

    st.stop()


# ============================================================
# HERO
# ============================================================

st.markdown(
    """<div class="hero">
<div class="hero-label">URBAN MOBILITY • DATA SCIENCE • DEMAND ANALYTICS</div>
<div class="hero-title">Bike Sharing Demand<br><span>Intelligence</span></div>
<div class="hero-text">Interactive analysis of Washington D.C. bike rental demand across time, seasons, weather conditions, working days and hourly usage patterns.</div>
</div>""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚲 Dashboard Controls")

st.sidebar.write(
    "Explore bike rental demand."
)

st.sidebar.divider()


# ============================================================
# YEAR FILTER
# ============================================================

year_options = sorted(
    df["year"].unique().tolist()
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    year_options
)


# ============================================================
# SEASON FILTER
# ============================================================

season_options = [
    "All",
    "Spring",
    "Summer",
    "Fall",
    "Winter"
]

selected_season = st.sidebar.selectbox(
    "Select Season",
    season_options
)


# ============================================================
# DAY TYPE FILTER
# ============================================================

day_options = [
    "All Days",
    "Working Days Only",
    "Non-Working Days Only"
]

selected_day_type = st.sidebar.selectbox(
    "Day Type",
    day_options
)


# ============================================================
# FILTER DATA
# ============================================================

filtered = df[
    df["year"] == selected_year
].copy()


if selected_season != "All":

    filtered = filtered[
        filtered["season"] ==
        selected_season
    ]


if selected_day_type == "Working Days Only":

    filtered = filtered[
        filtered["workingday"] == 1
    ]


elif selected_day_type == "Non-Working Days Only":

    filtered = filtered[
        filtered["workingday"] == 0
    ]


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered.empty:

    st.warning(
        "No records match the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_rentals = int(
    filtered["count"].sum()
)

average_hourly_rentals = (
    filtered["count"].mean()
)

peak_hour = (
    filtered
    .groupby("hour")["count"]
    .mean()
    .idxmax()
)

peak_hour_rentals = (
    filtered
    .groupby("hour")["count"]
    .mean()
    .max()
)


# ============================================================
# MARKET SNAPSHOT
# ============================================================

st.markdown(
    '<div class="section-title">Demand Snapshot</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(4)


# ============================================================
# KPI 1
# ============================================================

with k1:

    st.markdown(
        f"""<div class="kpi kpi-teal">
<div class="kpi-label">TOTAL RENTALS</div>
<div class="kpi-value">{total_rentals:,}</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# KPI 2
# ============================================================

with k2:

    st.markdown(
        f"""<div class="kpi kpi-copper">
<div class="kpi-label">AVG RENTALS / RECORD</div>
<div class="kpi-value">{average_hourly_rentals:,.0f}</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# KPI 3
# ============================================================

with k3:

    st.markdown(
        f"""<div class="kpi kpi-orchid">
<div class="kpi-label">PEAK HOUR</div>
<div class="kpi-value">{peak_hour:02d}:00</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# KPI 4
# ============================================================

with k4:

    st.markdown(
        f"""<div class="kpi kpi-sage">
<div class="kpi-label">PEAK AVG DEMAND</div>
<div class="kpi-value">{peak_hour_rentals:,.0f}</div>
</div>""",
        unsafe_allow_html=True
    )


# ============================================================
# COMMON PLOTLY STYLE
# ============================================================

common_layout = dict(

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color=TEXT
    ),

    margin=dict(
        l=50,
        r=30,
        t=60,
        b=50
    ),

    xaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.06)"
    ),

    yaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.06)"
    ),

    hoverlabel=dict(
        bgcolor="#172626",
        bordercolor=TEAL,
        font=dict(
            color=TEXT
        )
    )
)


# ============================================================
# HOURLY DEMAND
# ============================================================

st.markdown(
    '<div class="section-title">Hourly Demand Analysis</div>',
    unsafe_allow_html=True
)


hourly = (
    filtered
    .groupby("hour")["count"]
    .mean()
    .reset_index()
)


fig_hour = px.line(
    hourly,
    x="hour",
    y="count",
    markers=True,
    title="Average Rentals by Hour"
)


fig_hour.update_traces(
    line=dict(
        color=TEAL,
        width=3
    ),

    marker=dict(
        color=TEAL,
        size=7
    )
)


fig_hour.update_layout(
    **common_layout,

    xaxis_title="Hour of Day",

    yaxis_title="Average Rentals"
)


st.plotly_chart(
    fig_hour,
    use_container_width=True
)


# ============================================================
# SEASON + MONTH
# ============================================================

st.markdown(
    '<div class="section-title">Seasonal & Monthly Patterns</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


# ============================================================
# SEASON
# ============================================================

with col1:

    season_df = (
        filtered
        .groupby("season")["count"]
        .mean()
        .reindex(
            [
                "Spring",
                "Summer",
                "Fall",
                "Winter"
            ]
        )
        .reset_index()
    )


    fig_season = px.bar(

        season_df,

        x="season",

        y="count",

        title="Average Rentals by Season",

        color="season",

        color_discrete_sequence=[
            SAGE,
            TEAL,
            COPPER,
            STEEL
        ]
    )


    fig_season.update_layout(
        **common_layout,

        showlegend=False,

        xaxis_title="Season",

        yaxis_title="Average Rentals"
    )


    st.plotly_chart(
        fig_season,
        use_container_width=True
    )


# ============================================================
# MONTH
# ============================================================

with col2:

    monthly = (
        filtered
        .groupby("month")["count"]
        .mean()
        .reset_index()
    )

    fig_month = px.line(
        monthly,
        x="month",
        y="count",
        markers=True,
        title="Monthly Demand Trend"
    )

    fig_month.update_traces(
        line=dict(
            color=ORCHID,
            width=3
        ),
        marker=dict(
            color=ORCHID,
            size=7
        )
    )

    fig_month.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#F4F1EA"
        ),
        margin=dict(
            l=50,
            r=30,
            t=60,
            b=50
        ),
        xaxis=dict(
            title="Month",
            tickmode="linear",
            dtick=1,
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.06)"
        ),
        yaxis=dict(
            title="Average Rentals",
            gridcolor="rgba(255,255,255,0.06)",
            zerolinecolor="rgba(255,255,255,0.06)"
        )
    )

    st.plotly_chart(
        fig_month,
        use_container_width=True
    )

# ============================================================
# WEATHER ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Weather Impact</div>',
    unsafe_allow_html=True
)


weather_df = (
    filtered
    .groupby(
        "weather_label"
    )["count"]
    .mean()
    .reset_index()
)


weather_order = [
    "Clear",
    "Cloudy",
    "Light Rain / Snow",
    "Heavy Rain / Snow"
]


weather_df["weather_label"] = pd.Categorical(
    weather_df["weather_label"],
    categories=weather_order,
    ordered=True
)


weather_df = weather_df.sort_values(
    "weather_label"
)


fig_weather = px.bar(

    weather_df,

    x="weather_label",

    y="count",

    title="Average Rentals by Weather Condition",

    color="weather_label",

    color_discrete_sequence=[
        SAND,
        STEEL,
        ORCHID,
        ROSE
    ]
)


fig_weather.update_layout(

    **common_layout,

    showlegend=False,

    xaxis_title="Weather",

    yaxis_title="Average Rentals"
)


st.plotly_chart(
    fig_weather,
    use_container_width=True
)


# ============================================================
# WORKING DAY ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">Working Day Analysis</div>',
    unsafe_allow_html=True
)


working_df = (
    filtered
    .groupby("workingday")["count"]
    .mean()
    .reset_index()
)


working_df["Day Type"] = (
    working_df["workingday"]
    .map(
        {
            0: "Non-Working Day",
            1: "Working Day"
        }
    )
)


fig_working = px.bar(

    working_df,

    x="Day Type",

    y="count",

    title="Average Rentals: Working vs Non-Working Days",

    color="Day Type",

    color_discrete_sequence=[
        ROSE,
        TEAL
    ]
)


fig_working.update_layout(

    **common_layout,

    showlegend=False,

    xaxis_title="Day Type",

    yaxis_title="Average Rentals"
)


st.plotly_chart(

    fig_working,

    use_container_width=True
)


# ============================================================
# DAY OF WEEK
# ============================================================

st.markdown(
    '<div class="section-title">Weekly Demand Pattern</div>',
    unsafe_allow_html=True
)


day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


day_df = (
    filtered
    .groupby(
        "day_of_week"
    )["count"]
    .mean()
    .reindex(day_order)
    .reset_index()
)


fig_day = px.bar(

    day_df,

    x="day_of_week",

    y="count",

    title="Average Rentals by Day of Week"
)


fig_day.update_traces(

    marker=dict(
        color=STEEL
    )
)


fig_day.update_layout(

    **common_layout,

    xaxis_title="Day",

    yaxis_title="Average Rentals"
)


st.plotly_chart(

    fig_day,

    use_container_width=True
)


# ============================================================
# CORRELATION HEATMAP
# ============================================================

st.markdown(
    '<div class="section-title">Demand Correlation</div>',
    unsafe_allow_html=True
)


numeric_columns = [
    "temp",
    "atemp",
    "humidity",
    "windspeed",
    "casual",
    "registered",
    "count"
]


available_numeric = [
    column
    for column in numeric_columns
    if column in filtered.columns
]


corr = filtered[
    available_numeric
].corr()


fig_corr = px.imshow(

    corr,

    text_auto=".2f",

    aspect="auto",

    title="Correlation Between Weather & Rental Variables",

    color_continuous_scale=[
        "#182828",
        STEEL,
        TEAL,
        SAND,
        COPPER
    ]
)


fig_corr.update_layout(

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color=TEXT
    ),

    margin=dict(
        l=50,
        r=30,
        t=60,
        b=50
    )
)


st.plotly_chart(

    fig_corr,

    use_container_width=True
)


# ============================================================
# DATA EXPLORER
# ============================================================

st.markdown(
    '<div class="section-title">Data Explorer</div>',
    unsafe_allow_html=True
)


search = st.text_input(

    "Search records",

    placeholder=
        "Search datetime, season, weather..."
)


display_df = filtered.copy()


if search:

    search_mask = (

        display_df
        .astype(str)
        .apply(

            lambda row:
                row.str.contains(
                    search,
                    case=False,
                    na=False
                ).any(),

            axis=1
        )
    )

    display_df = display_df[
        search_mask
    ]


st.dataframe(

    display_df,

    use_container_width=True,

    height=420
)


# ============================================================
# DOWNLOAD
# ============================================================

csv_data = display_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(

    label="⬇ Download Filtered Data",

    data=csv_data,

    file_name=
        "bike_sharing_filtered.csv",

    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """<div class="footer">

<br>
@Pranai Teja Sabbe
<br><br>
Data Scientist
</div>""",
    unsafe_allow_html=True
)
