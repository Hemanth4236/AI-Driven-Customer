import streamlit as st

from utils.project_paths import project_path

st.title("AI Recommendation Engine")

income = st.number_input("Monthly Salary",10000,200000,50000)
spending = st.number_input("Monthly Spending",1000,100000,20000)

if st.button("Generate Recommendation"):

    ratio = spending/income

    if ratio > 0.6:
        st.warning(
            "Offer discount coupons and cashback."
        )

    elif ratio > 0.4:
        st.info(
            "Recommend premium products."
        )

    else:
        st.success(
            "Recommend luxury and high-end products."
        )