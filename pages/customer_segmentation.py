import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans

from utils.project_paths import project_path

df = pd.read_csv(project_path("data", "customers.csv"))

X = df[['Age','Annual_Income','Monthly_Spending']]

kmeans = KMeans(n_clusters=3, random_state=42)

df['Cluster'] = kmeans.fit_predict(X)

st.title("Customer Segmentation")

fig = px.scatter(
    df,
    x="Annual_Income",
    y="Monthly_Spending",
    color="Cluster",
    hover_name="Name",
    size="Age"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(df)