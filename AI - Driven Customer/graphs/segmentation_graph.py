import plotly.express as px

def segmentation_graph(df):

    fig = px.scatter(
        df,
        x="Annual_Income",
        y="Monthly_Spending",
        color="Cluster",
        hover_name="Name",
        size="Age",
        title="Customer Segmentation"
    )

    return fig