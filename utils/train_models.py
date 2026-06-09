import pandas as pd
import joblib

import sys
import os

# Add project root to path (IMPORTANT FIX)
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from utils.preprocessing import preprocess_data

from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression


# Load dataset
df = pd.read_csv("data/customers.csv")

# Preprocess
df = preprocess_data(df)

# ----------------------------
# CHURN MODEL
# ----------------------------
X_churn = df[['Age', 'Gender', 'Annual_Income', 'Monthly_Spending', 'Purchase_Frequency']]
y_churn = df['Churn']

churn_model = RandomForestClassifier(n_estimators=100, random_state=42)
churn_model.fit(X_churn, y_churn)

joblib.dump(churn_model, "models/churn_model.pkl")


# ----------------------------
# SPENDING MODEL
# ----------------------------
X_spend = df[['Age', 'Gender', 'Annual_Income', 'Purchase_Frequency']]
y_spend = df['Monthly_Spending']

spending_model = LinearRegression()
spending_model.fit(X_spend, y_spend)

joblib.dump(spending_model, "models/spending_model.pkl")


# ----------------------------
# SEGMENTATION MODEL (K-MEANS)
# ----------------------------
X_cluster = df[['Age', 'Annual_Income', 'Monthly_Spending']]

kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(X_cluster)

joblib.dump(kmeans, "models/segmentation_model.pkl")

print("Models trained and saved successfully!")