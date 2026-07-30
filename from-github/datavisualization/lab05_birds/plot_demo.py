import gradio as gr
import plotly.express as px
import plotly.graph_objects as go

df = px.data.gapminder()


def demo_fig_01():
    return px.bar(df[df["country"] == "Belgium"], x="year", y="pop", height=400)


def demo_fig_02():
    return px.line(x=["a", "b", "c"], y=[1, 3, 2])


def demo_fig_03():
    return px.scatter(
        df,
        x="gdpPercap",
        y="lifeExp",
        animation_frame="year",
        animation_group="country",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
        range_x=[100, 100000],
        range_y=[25, 90],
    )


def demo_fig_04():
    return px.histogram(df, x="lifeExp", nbins=30, title="Life Expectancy Histogram")


def demo_fig_05():
    return px.box(df, x="continent", y="lifeExp", title="Life Expectancy Box Plot")


def demo_fig_06():
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=df["gdpPercap"],
                y=df["lifeExp"],
                z=df["pop"],
                mode="markers",
                marker=dict(size=5, color=df["continent"].astype("category").cat.codes),
            )
        ]
    )
    fig.update_layout(title="3D GDP, Life Expectancy, Population", height=800)
    return fig


def demo_fig_07():
    return px.choropleth(
        df[df["year"] == 2007],
        locations="iso_alpha",
        color="lifeExp",
        hover_name="country",
        title="Life Expectancy by Country (2007)",
        color_continuous_scale=px.colors.sequential.Plasma,
    )


def demo_fig_08():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6], mode="lines", name="Line Trace"))
    fig.add_trace(go.Bar(x=[1, 2, 3], y=[7, 8, 9], name="Bar Trace"))
    return fig


CHARTS = {
    "Bar Plot": demo_fig_01,
    "Line Plot": demo_fig_02,
    "Scatter Plot": demo_fig_03,
    "Histogram": demo_fig_04,
    "Box Plot": demo_fig_05,
    "3D Scatter Plot": demo_fig_06,
    "Choropleth Map": demo_fig_07,
    "Multiple Traces": demo_fig_08,
}


def update_plot(chart_name):
    return CHARTS[chart_name]()


with gr.Blocks() as app:
    gr.Markdown("# 📊 Gapminder Dashboard")
    tabs = gr.Radio(
        choices=list(CHARTS.keys()),
        value="Bar Plot",
        label="Select Chart",
        interactive=True,
    )
    plot = gr.Plot(value=demo_fig_01())

    tabs.change(fn=update_plot, inputs=tabs, outputs=plot)

app.launch()