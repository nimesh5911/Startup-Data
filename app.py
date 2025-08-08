import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("startup_cleaned.csv")

# Convert date column if it exists
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

st.set_page_config(page_title="Startup Funding Dashboard", layout="wide")
st.title("Startup Funding Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Investment Type filter
investment_col = None
for col in df.columns:
    if "Investment" in col:
        investment_col = col
        break

if investment_col:
    investment_options = ["All"] + sorted(df[investment_col].dropna().unique().tolist())
    selected_investment = st.sidebar.selectbox("Select Investment Type", investment_options)
else:
    investment_col = None
    selected_investment = "All"

# City filter
city_col = None
for col in df.columns:
    if "City" in col:
        city_col = col
        break

if city_col:
    city_options = ["All"] + sorted(df[city_col].dropna().unique().tolist())
    selected_city = st.sidebar.selectbox("Select City", city_options)
else:
    city_col = None
    selected_city = "All"

# Industry filter
industry_col = None
for col in df.columns:
    if "Industry" in col:
        industry_col = col
        break

if industry_col:
    industry_options = ["All"] + sorted(df[industry_col].dropna().unique().tolist())
    selected_industry = st.sidebar.selectbox("Select Industry", industry_options)
else:
    industry_col = None
    selected_industry = "All"

# --- Apply Filters ---
filtered_df = df.copy()

if selected_investment != "All" and investment_col:
    filtered_df = filtered_df[filtered_df[investment_col] == selected_investment]
if selected_city != "All" and city_col:
    filtered_df = filtered_df[filtered_df[city_col] == selected_city]
if selected_industry != "All" and industry_col:
    filtered_df = filtered_df[filtered_df[industry_col] == selected_industry]

# --- Filter Data Preview ---
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head(10))

# --- Show Raw Data ---
if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("Raw Dataset")
    st.dataframe(df)

# --- Plots ---
col1, col2 = st.columns(2)

with col1:
    if industry_col:
        industry_count = filtered_df[industry_col].value_counts()
        plt.figure(figsize=(6, 4))
        industry_count.plot(kind="bar")
        plt.title("Number of Startups by Industry")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(plt)

with col2:
    if "Month" in filtered_df.columns and "Amount in USD" in filtered_df.columns:
        monthly_trend = (
            filtered_df.groupby("Month")["Amount in USD"]
            .sum()
            .sort_index()
        )
        plt.figure(figsize=(6, 4))
        monthly_trend.plot(kind="line", marker="o")
        plt.title("Monthly Funding Trend")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(plt)
