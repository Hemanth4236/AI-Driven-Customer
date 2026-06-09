import plotly.express as px

def revenue_graph(df):

    df["Revenue"] = (
        df["Monthly_Spending"] * 12
    )

    fig = px.bar(
        df,
        x="Name",
        y="Revenue",
        title="Revenue by Customer"
    )

    return fig