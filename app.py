import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("startup_cleaned.csv")

# Function to find the correct column name
def get_column(possible_names):
    for name in df.columns:
        if name.strip().lower() in [p.lower() for p in possible_names]:
            return name
    return None

# Detect column names dynamically
investment_col = get_column(["Investment Type", "Investment", "Type of Investment"])
city_col = get_column(["City", "City Location", "Location"])
sector_col = get_column(["Industry Vertical", "Sector", "Industry"])
amount_col = get_column(["Amount in USD", "Amount", "Funding Amount"])
date_col = get_column(["Date", "Startup Date", "Funding Date"])

# Sidebar filters
st.sidebar.header("Filter Options")

investment_options = ["All"] + sorted(df[investment_col].dropna().unique().tolist())
selected_investment = st.sidebar.selectbox("Select Investment Type", investment_options)

city_options = ["All"] + sorted(df[city_col].dropna().unique().tolist())
selected_city = st.sidebar.selectbox("Select City", city_options)

sector_options = ["All"] + sorted(df[sector_col].dropna().unique().tolist())
selected_sector = st.sidebar.selectbox("Select Sector", sector_options)

# Filter DataFrame
filtered_df = df.copy()
if selected_investment != "All":
    filtered_df = filtered_df[filtered_df[investment_col] == selected_investment]
if selected_city != "All":
    filtered_df = filtered_df[filtered_df[city_col] == selected_city]
if selected_sector != "All":
    filtered_df = filtered_df[filtered_df[sector_col] == selected_sector]

# Main title
st.title("Startup Data Dashboard")

# Show filtered data preview
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df)

# Visual 1: Investment Type Distribution
st.subheader("Investment Type Distribution")
investment_counts = filtered_df[investment_col].value_counts()
fig1, ax1 = plt.subplots()
investment_counts.plot(kind="bar", ax=ax1)
ax1.set_ylabel("Number of Startups")
ax1.set_xlabel("Investment Type")
ax1.set_title("Distribution of Investment Types")
st.pyplot(fig1)

# Visual 2: Sector Distribution
st.subheader("Sector Distribution")
sector_counts = filtered_df[sector_col].value_counts().head(10)
fig2, ax2 = plt.subplots()
sector_counts.plot(kind="barh", ax=ax2)
ax2.set_xlabel("Number of Startups")
ax2.set_ylabel("Sector")
ax2.set_title("Top 10 Sectors")
st.pyplot(fig2)

# Visual 3: Funding Amount Trend
if date_col and amount_col:
    st.subheader("Funding Amount Trend Over Time")
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    monthly_trend = filtered_df.groupby(filtered_df[date_col].dt.to_period("M"))[amount_col].sum()
    monthly_trend.index = monthly_trend.index.to_timestamp()
    fig3, ax3 = plt.subplots()
    ax3.plot(monthly_trend.index, monthly_trend.values)
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Total Funding Amount")
    ax3.set_title("Monthly Funding Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

# Visual 4: City-wise Startup Count
st.subheader("Top Cities by Number of Startups")
city_counts = filtered_df[city_col].value_counts().head(10)
fig4, ax4 = plt.subplots()
sns.barplot(x=city_counts.values, y=city_counts.index, ax=ax4)
ax4.set_xlabel("Number of Startups")
ax4.set_ylabel("City")
ax4.set_title("Top 10 Cities with Most Startups")
st.pyplot(fig4)

# Visual 5: Funding Amount by City
if amount_col:
    st.subheader("Total Funding Amount by City")
    funding_by_city = filtered_df.groupby(city_col)[amount_col].sum().sort_values(ascending=False).head(10)
    fig5, ax5 = plt.subplots()
    funding_by_city.plot(kind="bar", ax=ax5)
    ax5.set_xlabel("City")
    ax5.set_ylabel("Total Funding Amount")
    ax5.set_title("Top 10 Cities by Total Funding")
    st.pyplot(fig5)

st.success("Dashboard Loaded Successfully!")
