import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config (must be first Streamlit command)
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="centered"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    df['year'] = df['datetime'].dt.year
    return df

df = load_data()

# Title
st.title("🚲 Bike Sharing Demand Dashboard")

# Widget
year = st.selectbox("Select Year", sorted(df['year'].unique()))

# Filter data
filtered = df[df['year'] == year]

# Plot (delta generator safe)
fig, ax = plt.subplots()
sns.lineplot(
    data=filtered,
    x="hour",
    y="count",
    ax=ax
)

ax.set_title("Average Bike Rentals by Hour")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Total Rentals")

# Render plot (correct Streamlit way)
st.pyplot(fig, clear_figure=True)
