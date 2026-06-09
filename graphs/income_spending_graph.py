import plotly.express as px

def income_spending_graph(df):

    fig = px.bar(
        df,
        x="Name",
        y=["Monthly_Salary", "Monthly_Spending"],
        barmode="group",
        title="Salary vs Spending"
    )

    return fig