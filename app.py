# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="📊 Indian Startup Funding Dashboard", layout="wide")
st.title("📊 Indian Startup Funding Dashboard")

# Load Data
df = pd.read_csv("cleaned_startup_funding.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

# Sidebar Filters
st.sidebar.header("Filter Options")

# Gender-like filter = Industry
industry_options = ["All"] + sorted(df["Industry Vertical"].dropna().unique().tolist())
selected_industry = st.sidebar.selectbox("Select Industry Vertical", industry_options)

# Passenger class-like filter = City
city_options = ["All"] + sorted(df["City"].dropna().unique().tolist())
selected_city = st.sidebar.selectbox("Select City", city_options)

# New useful filter = Year
year_options = ["All"] + sorted(df["Date"].dropna().dt.year.unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options)

# Apply Filters
filtered_df = df.copy()

if selected_industry != "All":
    filtered_df = filtered_df[filtered_df["Industry Vertical"] == selected_industry]

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Date"].dt.year == selected_year]

# Show Data Preview
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head(20))

# Option to show all raw data
if st.checkbox("Show Full Raw Data"):
    st.dataframe(df)

# Plot 1: Top 10 Industries by Funding
st.subheader("Top 10 Industries by Total Funding")
top_industries = (
    filtered_df.groupby("Industry Vertical")["Amount in USD"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
fig1, ax1 = plt.subplots()
sns.barplot(x=top_industries.values, y=top_industries.index, ax=ax1)
ax1.set_xlabel("Total Funding (USD)")
ax1.set_ylabel("Industry Vertical")
st.pyplot(fig1)

# Plot 2: Funding by City
st.subheader("Top Cities by Funding Amount")
top_cities = (
    filtered_df.groupby("City")["Amount in USD"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_cities.values, y=top_cities.index, ax=ax2)
ax2.set_xlabel("Total Funding (USD)")
ax2.set_ylabel("City")
st.pyplot(fig2)

# Plot 3: Monthly Funding Trend
st.subheader("Monthly Funding Trend")
if not filtered_df.empty:
    monthly_trend = (
        filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Amount in USD"]
        .sum()
        .sort_index()
    )
    monthly_trend.index = monthly_trend.index.to_timestamp()  # Convert Period to Timestamp
    fig3, ax3 = plt.subplots()
    ax3.plot(monthly_trend.index, monthly_trend.values, marker="o")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Funding Amount (USD)")
    ax3.tick_params(axis='x', rotation=45)
    st.pyplot(fig3)
else:
    st.warning("No data available for the selected filters.")
