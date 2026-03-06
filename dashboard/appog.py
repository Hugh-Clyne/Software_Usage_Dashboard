import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st



base_dir = Path(__file__).resolve().parent.parent
db_path = base_dir / "database" / "usage_data.db"

# page title

st.title("SaaS Usage Analysis Dashboard")
conn = sqlite3.connect(db_path)

# Load data
@st.cache_data
def load_data():
    """
    Load data from the SQLite database and return it as a DataFrame.
    """
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM usage_enriched", conn)
    conn.close()
    return df

df = load_data()
#creating filter sections

st.sidebar.header("Filters")

company = st.sidebar.selectbox(
    "Company",
    ["All"] + sorted(df["company"].unique().tolist())
)

department = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["department"].unique().tolist())
)

app = st.sidebar.selectbox(
    "Application",
    ["All"] + sorted(df["app"].unique().tolist())
)

filtered_df = df.copy()

if company != "All":
    filtered_df = filtered_df[filtered_df["company"] == company]

if department != "All":
    filtered_df = filtered_df[filtered_df["department"] == department]

if app != "All":
    filtered_df = filtered_df[filtered_df["app"] == app]

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Users", filtered_df["user_id"].nunique())
col2.metric("Total Sessions", filtered_df["sessions"].sum())
col3.metric("Unique Applications", filtered_df["app"].nunique())

st.subheader("Usage by Application")

app_usage = (
    filtered_df.groupby("app")["sessions"]
    .sum()
    .sort_values(ascending=False)
    )

st.bar_chart(app_usage)

query = """
SELECT
    company,
    app,
    COUNT(DISTINCT user_id) AS users,
    seat_cost_usd,
    COUNT(DISTINCT user_id) * seat_cost_usd AS estimated_cost
FROM usage_enriched
GROUP BY company, app
"""
df = pd.read_sql(query, conn)

st.title("SaaS Usage Intelligence Dashboard")

st.subheader("Estimated SaaS Spend by Application")

cost_by_app = df.groupby("app")["estimated_cost"].sum()

st.bar_chart(cost_by_app)

st.subheader("Usage Data")
st.dataframe(filtered_df.head())

conn.close()
