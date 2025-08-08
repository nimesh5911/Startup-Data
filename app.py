import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# Load Dataset
# ===============================
df = pd.read_csv("startup_cleaned.csv")

# ===============================
# Page Config
# ===============================
st.set_page_config(page_title="Startup Funding Dashboard", layout="wide")
st.title("Startup Funding Dashboard")

# ===============================
# Filters
# ===============================
col1, col2, col3 = st.columns(3)

# Year Filter
year_options = ["All"] + sorted(df["Year"].dropna().unique().tolist())
selected_year = col1.selectbox("Select Year", year_options)

# City Filter
city_options = ["All"] + sorted(df["City"].dropna().unique().tolist())
selected_city = col2.selectbox("Select City", city_options)

# Investment Type Filter
inv_type_options = ["All"] + sorted(df["Investment Type"].dropna().unique().tolist())
selected_inv_type = col3.selectbox("Select Investment Type", inv_type_options)

# ===============================
# Apply Filters
# ===============================
filtered_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_inv_type != "All":
    filtered_df = filtered_df[filtered_df["Investment Type"] == selected_inv_type]

# ===============================
# Filtered Data Preview
# ===============================
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head(10))

# ===============================
# Show Raw Data Toggle
# ===============================
if st.checkbox("Show Raw Data"):
    st.dataframe(df)

# ===============================
# Visual 1: Funding Amount Distribution by Industry
# ===============================
st.subheader("Funding Amount Distribution by Industry Vertical")
industry_funding = (
    filtered_df.groupby("Industry Vertical")["Amount in USD"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1, ax1 = plt.subplots()
industry_funding.plot(kind="barh", ax=ax1)
ax1.set_xlabel("Total Funding (USD)")
ax1.set_ylabel("Industry Vertical")
ax1.set_title("Top 10 Funded Industries")
st.pyplot(fig1)

# ===============================
# Visual 2: Monthly Funding Trend
# ===============================
st.subheader("Monthly Funding Trend")
monthly_trend = (
    filtered_df.groupby("Month")["Amount in USD"]
    .sum()
    .reset_index()
    .sort_values("Month")
)

fig2, ax2 = plt.subplots()
sns.lineplot(data=monthly_trend, x="Month", y="Amount in USD", marker="o", ax=ax2)
ax2.set_xlabel("Month")
ax2.set_ylabel("Total Funding (USD)")
ax2.set_title("Monthly Funding Trend")
st.pyplot(fig2)

# ===============================
# Visual 3: Investment Type Share
# ===============================
st.subheader("Investment Type Share")
inv_type_share = filtered_df["Investment Type"].value_counts()

fig3, ax3 = plt.subplots()
ax3.pie(inv_type_share, labels=inv_type_share.index, autopct="%1.1f%%", startangle=90)
ax3.set_title("Investment Type Distribution")
st.pyplot(fig3)

# ===============================
# Visual 4: Top Startups by Funding
# ===============================
st.subheader("Top Startups by Funding")
top_startups = (
    filtered_df.groupby("Startup Name")["Amount in USD"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig4, ax4 = plt.subplots()
top_startups.plot(kind="bar", ax=ax4)
ax4.set_xlabel("Startup Name")
ax4.set_ylabel("Total Funding (USD)")
ax4.set_title("Top 10 Funded Startups")
st.pyplot(fig4)

# ===============================
# Footer
# ===============================
st.markdown("---")
st.markdown("Dashboard created for Startup Funding Data Analysis")
