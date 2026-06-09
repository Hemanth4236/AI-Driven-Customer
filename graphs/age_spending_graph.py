import plotly.express as px

def age_spending_graph(df):

    fig = px.scatter(
        df,
        x="Age",
        y="Monthly_Spending",
        color="Gender",
        size="Annual_Income",
        title="Age vs Spending"
    )

    return fig