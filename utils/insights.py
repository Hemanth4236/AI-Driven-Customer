import pandas as pd

def generate_insights(df):

    insights = []

    avg_income = df['Annual_Income'].mean()

    avg_spending = df['Monthly_Spending'].mean()

    churn_rate = (
        df['Churn'].sum()
        / len(df)
    ) * 100

    insights.append(
        f"Average Annual Income: ₹{avg_income:,.0f}"
    )

    insights.append(
        f"Average Monthly Spending: ₹{avg_spending:,.0f}"
    )

    insights.append(
        f"Customer Churn Rate: {churn_rate:.2f}%"
    )

    highest_spender = df.loc[
        df['Monthly_Spending'].idxmax()
    ]

    insights.append(
        f"Top spender: {highest_spender['Name']}"
    )

    return insights