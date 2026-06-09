import plotly.express as px

def churn_graph(df):

    churn_counts = df["Churn"].value_counts()

    fig = px.pie(
        values=churn_counts.values,
        names=["Stay", "Churn"],
        title="Customer Churn Distribution"
    )

    return fig