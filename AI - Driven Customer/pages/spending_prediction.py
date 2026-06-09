import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/customers.csv")

X = df[['Age','Monthly_Salary']]
y = df['Monthly_Spending']

model = LinearRegression()
model.fit(X,y)

st.title("Monthly Spending Prediction")

age = st.slider("Age",18,70,25)
salary = st.number_input("Monthly Salary",10000,200000,50000)

pred = model.predict([[age,salary]])

if st.button("Predict Spending"):
    st.success(f"Expected Spending = ₹{int(pred[0])}")