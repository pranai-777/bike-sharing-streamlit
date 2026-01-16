import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month
    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.day_name()
    df["season"] = df["season"].map({
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    })
    return df

df = load_data()

# ---------------- TITLE ----------------
st.title("🚲 Bike Sharing Demand Dashboard")
st.markdown("Interactive analysis of Washington D.C. bike rentals (2011–2012)")

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("📊 Dashboard")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["year"].unique())
)

season = st.sidebar.selectbox(
    "Select Season",
    ["All", "Spring", "Summer", "Fall", "Winter"]
)

working = st.sidebar.selectbox(
    "Day Type",
    ["All Days", "Working Days Only", "Non-Working Days Only"]
)

# ---------------- APPLY FILTERS ----------------
filtered = df[df["year"] == year]

# Season filter
if season != "All":
    filtered = filtered[filtered["season"] == season]

# Working day filter
if working == "Working Days Only":
    filtered = filtered[filtered["workingday"] == 1]
elif working == "Non-Working Days Only":
    filtered = filtered[filtered["workingday"] == 0]

# ---------------- LAYOUT ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Average Rentals by Hour")
    fig, ax = plt.subplots()
    sns.lineplot(data=filtered, x="hour", y="count", ax=ax)
    st.pyplot(fig, clear_figure=True)

with col2:
    st.subheader("Average Rentals by Season")
    fig, ax = plt.subplots()
    sns.barplot(data=filtered, x="season", y="count", ax=ax)
    st.pyplot(fig, clear_figure=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Monthly Trend")
    fig, ax = plt.subplots()
    sns.lineplot(data=filtered, x="month", y="count", ax=ax)
    st.pyplot(fig, clear_figure=True)

with col4:
    st.subheader("Weather Impact")
    fig, ax = plt.subplots()
    sns.barplot(
        data=filtered,
        x="weather",
        y="count",
        ax=ax,
        errorbar=("ci", 95)
    )
    st.pyplot(fig, clear_figure=True)

# ---------------- CORRELATION ----------------
st.subheader("Correlation Heatmap")
corr = filtered.corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, cmap="coolwarm", ax=ax)
st.pyplot(fig, clear_figure=True)
