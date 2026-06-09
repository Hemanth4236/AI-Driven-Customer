import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Customer Intelligence Dashboard",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.title {
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:#1f4e79;
}

.subtitle {
    text-align:center;
    color:gray;
    font-size:18px;
    margin-bottom:20px;
}

.section {
    background:white;
    padding:15px;
    border-radius:10px;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    "<div class='title'>🤖 AI Customer Intelligence Dashboard</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Customer Search, Prediction and Business Analytics</div>",
    unsafe_allow_html=True
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    df = pd.read_csv("data/customers.csv")

    churn_model = joblib.load("models/churn_model.pkl")
    spend_model = joblib.load("models/spending_model.pkl")
    segment_model = joblib.load("models/segmentation_model.pkl")

except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# --------------------------------------------------
# SEARCH SECTION
# --------------------------------------------------

st.subheader("🔍 Search Customer")

search_type = st.radio(
    "Search Customer By",
    ["Age", "Monthly Salary"],
    horizontal=True
)

if search_type == "Age":

    search_value = st.number_input(
        "Enter Age",
        min_value=18,
        max_value=70,
        value=30
    )

    filtered_df = df[df["Age"] == search_value]

else:

    search_value = st.number_input(
        "Enter Monthly Salary",
        min_value=10000,
        max_value=200000,
        value=40000
    )

    filtered_df = df[
        df["Monthly_Salary"] == search_value
    ]

# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button("🚀 Analyze Customer"):

    if filtered_df.empty:

        st.warning("No customer found.")

    else:

        st.success(
            f"{len(filtered_df)} customer(s) found."
        )

        for _, row in filtered_df.iterrows():

            gender_val = (
                1 if row["Gender"] == "Male" else 0
            )

            # --------------------------------------
            # PREDICTIONS
            # --------------------------------------

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

            segment = segment_model.predict([[
                row["Age"],
                row["Annual_Income"],
                spending
            ]])[0]

            segment_names = {
                0: "Budget Customer",
                1: "Regular Customer",
                2: "Premium Customer",
                3: "High Value Customer"
            }

            # --------------------------------------
            # CUSTOMER DETAILS TABLE
            # --------------------------------------

            st.subheader("👤 Customer Details")

            customer_details = pd.DataFrame({
                "Attribute": [
                    "Customer Name",
                    "Age",
                    "Gender",
                    "Annual Income",
                    "Monthly Salary",
                    "Purchase Frequency"
                ],
                "Value": [
                    row["Name"],
                    row["Age"],
                    row["Gender"],
                    f"₹{row['Annual_Income']:,}",
                    f"₹{row['Monthly_Salary']:,}",
                    row["Purchase_Frequency"]
                ]
            })

            st.dataframe(
                customer_details,
                use_container_width=True,
                hide_index=True
            )

            # --------------------------------------
            # PREDICTION TABLE
            # --------------------------------------

            st.subheader("📊 Prediction Results")

            prediction_table = pd.DataFrame({
                "Metric": [
                    "Predicted Spending",
                    "Customer Segment",
                    "Churn Risk"
                ],
                "Result": [
                    f"₹{int(spending):,}",
                    segment_names.get(segment, str(segment)),
                    "High Risk" if churn == 1 else "Low Risk"
                ]
            })

            st.dataframe(
                prediction_table,
                use_container_width=True,
                hide_index=True
            )

            # --------------------------------------
            # COMPLETE ANALYSIS TABLE
            # --------------------------------------

            st.subheader("📋 Complete Customer Analysis")

            analysis_table = pd.DataFrame({
                "Field": [
                    "Customer Name",
                    "Age",
                    "Gender",
                    "Annual Income",
                    "Monthly Salary",
                    "Purchase Frequency",
                    "Predicted Spending",
                    "Customer Segment",
                    "Churn Risk"
                ],
                "Value": [
                    row["Name"],
                    row["Age"],
                    row["Gender"],
                    f"₹{row['Annual_Income']:,}",
                    f"₹{row['Monthly_Salary']:,}",
                    row["Purchase_Frequency"],
                    f"₹{int(spending):,}",
                    segment_names.get(segment, str(segment)),
                    "High Risk" if churn == 1 else "Low Risk"
                ]
            })

            st.dataframe(
                analysis_table,
                use_container_width=True,
                hide_index=True
            )

            # --------------------------------------
            # BAR CHART
            # --------------------------------------

            st.subheader("📈 Financial Analysis")

            graph_df = pd.DataFrame({
                "Metric": [
                    "Annual Income",
                    "Monthly Salary",
                    "Predicted Spending"
                ],
                "Value": [
                    row["Annual_Income"],
                    row["Monthly_Salary"],
                    int(spending)
                ]
            })

            fig1 = px.bar(
                graph_df,
                x="Metric",
                y="Value",
                title=f"{row['Name']} Financial Analysis"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            # --------------------------------------
            # PIE CHART
            # --------------------------------------

            pie_df = pd.DataFrame({
                "Category": [
                    "Salary",
                    "Predicted Spending"
                ],
                "Amount": [
                    row["Monthly_Salary"],
                    int(spending)
                ]
            })

            fig2 = px.pie(
                pie_df,
                names="Category",
                values="Amount",
                title="Salary vs Spending"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

            # --------------------------------------
            # AI INSIGHTS
            # --------------------------------------

            st.subheader("💡 AI Insights")

            if spending > row["Monthly_Salary"] * 0.7:

                st.warning(
                    "Customer spends a large portion of salary. Consider retention offers and loyalty rewards."
                )

            elif spending < row["Monthly_Salary"] * 0.3:

                st.info(
                    "Customer spending is relatively low. Upselling and targeted marketing may be effective."
                )

            else:

                st.success(
                    "Customer shows balanced spending behavior. Premium products can be recommended."
                )

            st.divider()