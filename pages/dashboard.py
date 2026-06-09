import streamlit as st
import pandas as pd
import plotly.express as px

from utils.project_paths import project_path

df = pd.read_csv(project_path("data", "customers.csv"))

st.title("Dashboard")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Customers", len(df))
col2.metric("Avg Age", round(df['Age'].mean(),1))
col3.metric("Avg Income", f"₹{int(df['Annual_Income'].mean())}")
col4.metric("Avg Spending", f"₹{int(df['Monthly_Spending'].mean())}")

fig = px.bar(
    df,
    x='Name',
    y='Monthly_Spending',
    title="Customer Spending Comparison"
)

st.plotly_chart(fig, use_container_width=True)