import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from utils.project_paths import project_path

df = pd.read_csv(project_path("data", "customers.csv"))

X = df[['Age','Annual_Income','Monthly_Spending','Purchase_Frequency']]
y = df['Churn']

model = RandomForestClassifier()

model.fit(X,y)

st.title("Customer Churn Prediction")

age = st.slider("Age",18,70,30)
income = st.number_input("Annual Income",100000,2000000,500000)
spending = st.number_input("Monthly Spending",1000,100000,20000)
frequency = st.slider("Purchase Frequency",1,20,8)

prediction = model.predict([[age,income,spending,frequency]])

if st.button("Predict"):
    if prediction[0]==1:
        st.error("Customer likely to churn")
    else:
        st.success("Customer likely to stay")