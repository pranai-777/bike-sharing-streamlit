import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# Load data
df = pd.read_csv("train.csv")
df["datetime"] = pd.to_datetime(df["datetime"])
df["year"] = df["datetime"].dt.year
df["hour"] = df["datetime"].dt.hour
df["season"] = df["season"].map({
    1: "spring", 2: "summer", 3: "fall", 4: "winter"
})

# ---------------- SIDEBAR CONTROLS ----------------
st.sidebar.markdown("## 📊 Dashboard Controls")
st.sidebar.markdown("---")

# Year filter (multi-select)
selected_years = st.sidebar.multiselect(
    "Select Years:",
    options=sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

# Season filter (multi-select)
selected_seasons = st.sidebar.multiselect(
    "Select Seasons:",
    options=sorted(df["season"].unique()),
    default=sorted(df["season"].unique())
)

# Day type filter
day_type = st.sidebar.selectbox(
    "Day Type:",
    ["All Days", "Working Days Only", "Non-Working Days Only"]
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["year"].isin(selected_years)) &
    (df["season"].isin(selected_seasons))
]

if day_type == "Working Days Only":
    filtered_df = filtered_df[filtered_df["workingday"] == 1]
elif day_type == "Non-Working Days Only":
    filtered_df = filtered_df[filtered_df["workingday"] == 0]


st.title("🚲 Bike Sharing Demand Dashboard")
st.subheader("Average Bike Rentals by Hour")

fig, ax = plt.subplots()
sns.lineplot(
    data=filtered_df,
    x="hour",
    y="count",
    ax=ax
)

ax.set_xlabel("Hour of Day")
ax.set_ylabel("Total Rentals")
ax.set_title("Hourly Bike Demand")

st.pyplot(fig, clear_figure=True)
