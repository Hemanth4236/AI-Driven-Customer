import streamlit as st
import pandas as pd
import joblib
from functools import lru_cache
from pathlib import Path

from utils.project_paths import project_path

st.set_page_config(
    page_title="AI Customer Intelligence System",
    layout="wide"
)

st.title("🤖 AI Driven Customer Intelligence Platform")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Select Module",
    [
        "Dashboard",
        "Customer Segmentation",
        "Churn Prediction",
        "Spending Prediction",
        "Recommendations",
        "Customer Search"
    ]
)

@lru_cache(maxsize=1)
def load_dataframe() -> pd.DataFrame:
    data_path = project_path("data", "customers.csv")
    return pd.read_csv(data_path)


@lru_cache(maxsize=None)
def load_model(model_name: str):
    model_path = project_path("models", model_name)
    if not Path(model_path).exists():
        raise FileNotFoundError(f"Missing model file: {model_path}")
    return joblib.load(model_path)


try:
    df = load_dataframe()
except Exception as error:
    st.error(f"Failed to load data/customers.csv: {error}")
    st.stop()

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.subheader("📊 Dashboard Overview")

    st.metric("Total Customers", len(df))
    st.metric("Average Income", f"₹{int(df['Annual_Income'].mean())}")
    st.metric("Average Spending", f"₹{int(df['Monthly_Spending'].mean())}")
    st.metric("Churn Rate", f"{round(df['Churn'].mean()*100,2)}%")
# ---------------- SEGMENTATION ----------------
elif page == "Customer Segmentation":
    st.subheader("🧠 Customer Segmentation (K-Means)")

    st.write("Customers grouped based on Age, Income, Spending")

    st.dataframe(df)

    st.success("Load segmentation_model.pkl and show cluster graph here")

# ---------------- CHURN PREDICTION ----------------
elif page == "Churn Prediction":

    st.subheader("🔴 Churn Prediction")

    try:
        model = load_model("churn_model.pkl")
    except Exception as error:
        st.error(f"Failed to load churn model: {error}")
        st.stop()

    age = st.slider("Age", 18, 70, 30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    income = st.number_input("Annual Income", 100000, 2000000, 500000)
    salary = st.number_input("Monthly Salary", 10000, 200000, 40000)
    frequency = st.slider("Purchase Frequency", 1, 20, 5)

    gender_val = 1 if gender == "Male" else 0

    if st.button("Predict Churn"):

        result = model.predict([[age, gender_val, income, salary, frequency]])[0]

        if result == 1:
            st.error("🔴 High Risk: Customer WILL CHURN")
        else:
            st.success("🟢 Low Risk: Customer WILL STAY")

# ---------------- SPENDING PREDICTION ----------------
elif page == "Spending Prediction":

    st.subheader("💰 Spending Prediction")

    try:
        model = load_model("spending_model.pkl")
    except Exception as error:
        st.error(f"Failed to load spending model: {error}")
        st.stop()

    age = st.slider("Age", 18, 70, 30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    income = st.number_input("Annual Income", 100000, 2000000, 500000)
    frequency = st.slider("Purchase Frequency", 1, 20, 5)

    gender_val = 1 if gender == "Male" else 0

    if st.button("Predict Spending"):

        result = model.predict([[age, gender_val, income, frequency]])[0]

        st.info(f"💰 Predicted Monthly Spending: ₹{int(result)}")

# ---------------- RECOMMENDATIONS ----------------
elif page == "Recommendations":

    st.subheader("🎯 AI Recommendation Engine")

    try:
        churn_model = load_model("churn_model.pkl")
        spend_model = load_model("spending_model.pkl")
    except Exception as error:
        st.error(f"Failed to load recommendation models: {error}")
        st.stop()

    age = st.slider("Age", 18, 70, 30)
    salary = st.number_input("Monthly Salary", 10000, 200000, 40000)
    income = st.number_input("Annual Income", 100000, 2000000, 500000)
    frequency = st.slider("Purchase Frequency", 1, 20, 5)
    gender = st.selectbox("Gender", ["Male", "Female"])

    gender_val = 1 if gender == "Male" else 0

    if st.button("Analyze Customer"):

        churn = churn_model.predict([[age, gender_val, income, salary, frequency]])[0]
        spending = spend_model.predict([[age, gender_val, income, frequency]])[0]

        st.markdown("## 📊 Results")

        if churn == 1:
            st.error("🔴 High Churn Risk")
        else:
            st.success("🟢 Loyal Customer")

        st.info(f"💰 Predicted Spending: ₹{int(spending)}")

        st.markdown("## 💡 Business Insight")

        if spending > salary * 0.7:
            st.warning("⚠️ High spender → Risk customer, give offers")
        elif spending < salary * 0.3:
            st.success("💡 Low spender → Upsell opportunity")
        else:
            st.info("🎯 Balanced customer → Premium targeting")

# ---------------- CUSTOMER SEARCH ----------------
elif page == "Customer Search":

    st.subheader("🔍 Customer Search + AI Prediction")

    try:
        churn_model = load_model("churn_model.pkl")
        spend_model = load_model("spending_model.pkl")
    except Exception as error:
        st.error(f"Failed to load search models: {error}")
        st.stop()

    # FILTERS
    age_min, age_max = st.slider("Age Range", 18, 70, (25, 40))
    salary_min, salary_max = st.slider("Monthly Salary Range", 10000, 200000, (30000, 80000))

    filtered_df = df[
        (df["Age"] >= age_min) &
        (df["Age"] <= age_max) &
        (df["Monthly_Salary"] >= salary_min) &
        (df["Monthly_Salary"] <= salary_max)
    ]

    st.markdown("## 👥 Matching Customers")
    st.dataframe(filtered_df)

    if len(filtered_df) > 0:

        results = []

        for _, row in filtered_df.iterrows():

            gender_val = 1 if row["Gender"] == "Male" else 0

            churn = churn_model.predict([[
                row["Age"],
                gender_val,
                row["Annual_Income"],
                row["Monthly_Salary"],
                row["Purchase_Frequency"]
            ]])[0]

            spending = spend_model.predict([[
                row["Age"],
                gender_val,
                row["Annual_Income"],
                row["Purchase_Frequency"]
            ]])[0]

            results.append({
                "Name": row["Name"],
                "Age": row["Age"],
                "Salary": row["Monthly_Salary"],
                "Churn Risk": "Yes" if churn == 1 else "No",
                "Predicted Spending": int(spending)
            })

        result_df = pd.DataFrame(results)

        st.markdown("## 📊 AI Prediction Results")
        st.dataframe(result_df)

        st.markdown("## 💡 Insights")

        risk = result_df[result_df["Churn Risk"] == "Yes"]

        if len(risk) > 0:
            st.error(f"⚠️ {len(risk)} high-risk customers found")
        else:
            st.success("🟢 No major churn risk")

        st.info(f"💰 Avg Spending: ₹{int(result_df['Predicted Spending'].mean())}")

    else:
        st.warning("No customers found for selected filters")