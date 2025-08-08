# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# App configuration
st.set_page_config(page_title="Startup Funding Dashboard", layout="wide")
st.title("🚀 Indian Startup Funding Analysis")

# Load dataset
df = pd.read_csv("startup_cleaned.csv")  # Your cleaned CSV

# Data Cleaning
df["Amount in USD"] = pd.to_numeric(df["Amount in USD"], errors="coerce")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Amount in USD", "City Location", "Startup Name"])

# Sidebar Filters (Improved)
st.sidebar.header("Filter Options")

# Multi-select for cities
all_cities = sorted(df["City Location"].dropna().unique())
selected_cities = st.sidebar.multiselect("Select Cities", options=all_cities, default=all_cities)

# Year range slider
min_year, max_year = int(df["Date"].dt.year.min()), int(df["Date"].dt.year.max())
selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# Multi-select for industries
all_industries = sorted(df["Industry Vertical"].dropna().unique())
selected_industries = st.sidebar.multiselect("Select Industries", options=all_industries, default=all_industries)

# Funding amount slider
amount_range = st.sidebar.slider("Select Funding Amount Range (USD)", 
                                  int(df["Amount in USD"].min()), 
                                  int(df["Amount in USD"].max()), 
                                  (int(df["Amount in USD"].min()), int(df["Amount in USD"].max())))

# Filter data based on selections
filtered_df = df[
    (df["City Location"].isin(selected_cities)) &
    (df["Date"].dt.year.between(selected_years[0], selected_years[1])) &
    (df["Industry Vertical"].isin(selected_industries)) &
    (df["Amount in USD"].between(amount_range[0], amount_range[1]))
]

# Filtered Data Preview
st.subheader("📊 Filtered Data Preview")
st.write(filtered_df.head())

# Show Full Filtered Data
if st.checkbox("Show Full Filtered Data"):
    st.dataframe(filtered_df)

# Layout: 2x2 grid
col1, col2 = st.columns(2)

# 1️⃣ Top 10 Funded Startups
with col1:
    st.subheader(f"Top 10 Funded Startups ({selected_years[0]} - {selected_years[1]})")
    top_startups = (
        filtered_df.groupby("Startup Name")["Amount in USD"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig1, ax1 = plt.subplots()
    sns.barplot(data=top_startups, x="Amount in USD", y="Startup Name", palette="Set3", ax=ax1)
    st.pyplot(fig1)

# 2️⃣ Top 10 Investors
with col2:
    st.subheader(f"Top 10 Investors ({selected_years[0]} - {selected_years[1]})")
    top_investors = (
        filtered_df.groupby("Investors Name")["Amount in USD"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig2, ax2 = plt.subplots()
    sns.barplot(data=top_investors, x="Amount in USD", y="Investors Name", palette="Set2", ax=ax2)
    st.pyplot(fig2)

# 3️⃣ Monthly Funding Trend
with col1:
    st.subheader("Monthly Funding Trend")
    monthly_trend = (
        filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Amount in USD"]
        .sum()
        .reset_index()
    )
    monthly_trend["Date"] = monthly_trend["Date"].astype(str)
    fig3, ax3 = plt.subplots()
    sns.lineplot(data=monthly_trend, x="Date", y="Amount in USD", marker="o", ax=ax3)
    plt.xticks(rotation=45)
    st.pyplot(fig3)

# 4️⃣ Funding by Industry
with col2:
    st.subheader("Funding Distribution by Industry")
    industry_funding = (
        filtered_df.groupby("Industry Vertical")["Amount in USD"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig4, ax4 = plt.subplots()
    sns.barplot(data=industry_funding, x="Amount in USD", y="Industry Vertical", palette="coolwarm", ax=ax4)
    st.pyplot(fig4)
