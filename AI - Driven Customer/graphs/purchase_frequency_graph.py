import plotly.express as px

def purchase_frequency_graph(df):

    fig = px.line(
        df,
        x="Name",
        y="Purchase_Frequency",
        markers=True,
        title="Purchase Frequency"
    )

    return fig