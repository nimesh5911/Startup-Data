# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Startup Funding Dashboard", layout="wide")

# Title
st.title("🚀 Startup Funding Analytics Dashboard")

# Load Data
df = pd.read_csv("startup_funding_cleaned.csv")

# Sidebar Filters
st.sidebar.header("Filter Options")

# Industry filter with "All" option
industry_options = ["All"] + sorted(df["Industry Vertical"].dropna().unique().tolist())
selected_industry = st.sidebar.selectbox("Select Industry Vertical", industry_options)

# Investment type filter
investment_options = ["All"] + sorted(df["Investment Type"].dropna().unique().tolist())
selected_investment = st.sidebar.selectbox("Select Investment Type", investment_options)

# City filter
city_options = ["All"] + sorted(df["City"].dropna().unique().tolist())
selected_city = st.sidebar.selectbox("Select City", city_options)

# Apply filters
filtered_df = df.copy()
if selected_industry != "All":
    filtered_df = filtered_df[filtered_df["Industry Vertical"] == selected_industry]
if selected_investment != "All":
    filtered_df = filtered_df[filtered_df["Investment Type"] == selected_investment]
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

# Show Raw Data
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# Filtered Data Preview
st.subheader("Filtered Data Preview")
st.write(filtered_df.head())

# --- Visualizations ---
# 1. Funding by Industry
st.subheader("Funding Amount by Industry Vertical")
fig1, ax1 = plt.subplots()
industry_funding = (
    filtered_df.groupby("Industry Vertical")["Amount in USD"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
sns.barplot(x=industry_funding.values, y=industry_funding.index, ax=ax1)
ax1.set_xlabel("Total Funding (USD)")
ax1.set_ylabel("Industry Vertical")
st.pyplot(fig1)

# 2. Funding by Investment Type
st.subheader("Funding Amount by Investment Type")
fig2, ax2 = plt.subplots()
investment_funding = (
    filtered_df.groupby("Investment Type")["Amount in USD"]
    .sum()
    .sort_values(ascending=False)
)
sns.barplot(x=investment_funding.values, y=investment_funding.index, ax=ax2)
ax2.set_xlabel("Total Funding (USD)")
ax2.set_ylabel("Investment Type")
st.pyplot(fig2)

# 3. Monthly Funding Trend
st.subheader("Monthly Funding Trend")
fig3, ax3 = plt.subplots()
monthly_trend = (
    filtered_df.groupby("Month")["Amount in USD"]
    .sum()
    .reindex(range(1, 13), fill_value=0)  # Ensure months are in order
)
sns.lineplot(x=monthly_trend.index, y=monthly_trend.values, marker="o", ax=ax3)
ax3.set_xlabel("Month")
ax3.set_ylabel("Total Funding (USD)")
ax3.set_xticks(range(1, 13))
ax3.set_xticklabels(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
)
st.pyplot(fig3)
