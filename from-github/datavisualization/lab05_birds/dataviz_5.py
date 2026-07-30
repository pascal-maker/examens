import gradio as gr
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# We use Gapminder as placeholder data, but you can load your JSON here!
#import json
#with open("78494874.json", "r") as f:
#    data = json.load(f)
#df = pd.DataFrame(data)

df = px.data.gapminder()

# --- DESIGN TOKENS ---
# This is how you match exact colors from a design!
# You find the Hex codes (#RRGGBB) used in the design and apply them.
DESIGN_BG_COLOR = "#FAF9F6"           # Off-white background
DESIGN_FONT_COLOR = "#333333"         # Dark gray text
DESIGN_GRID_COLOR = "#E0E0E0"         # faint gray grid lines
DESIGN_COLORS = [
    "#FF5A5F", # Red/Pink
    "#00A699", # Teal
    "#FC642D", # Orange
    "#484848", # Dark Charcoal
    "#767676"  # Light Gray
]

def apply_design(fig):
    """
    This helper function ensures every chart exactly matches the design template!
    It strips away Plotly's default styles and overrides them with our custom design variables.
    """
    fig.update_layout(
        plot_bgcolor=DESIGN_BG_COLOR,
        paper_bgcolor=DESIGN_BG_COLOR,
        font=dict(color=DESIGN_FONT_COLOR, family="Arial, sans-serif"),
        colorway=DESIGN_COLORS, # Forces the chart to use our exact palette in order
        margin=dict(l=40, r=40, t=60, b=40)
    )
    # Updating the grid lines to match the design flawlessly
    fig.update_xaxes(showgrid=True, gridcolor=DESIGN_GRID_COLOR, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=DESIGN_GRID_COLOR, zeroline=False)
    return fig

# --- VIZ 1: Line Chart ---
def viz_1():
    # Filter data to make the line chart clean
    data = df[df["country"].isin(["Belgium", "France", "Germany"])]
    fig = px.line(data, x="year", y="lifeExp", color="country", title="Life Expectancy Over Time")
    
    # Apply our custom design!
    return apply_design(fig)

# --- VIZ 2: Bar Chart ---
def viz_2():
    data = df[df["year"] == 2007].nlargest(5, "pop")
    fig = px.bar(data, x="country", y="pop", title="Top 5 Populations in 2007", text_auto='.2s')
    
    # We can even override the color of specific bars internally if the design requires it:
    fig.update_traces(marker_color=DESIGN_COLORS[1]) 
    return apply_design(fig)

# --- VIZ 3: Scatter Plot ---
def viz_3():
    data = df[df["year"] == 2007]
    fig = px.scatter(data, x="gdpPercap", y="lifeExp", size="pop", color="continent", 
                     title="GDP vs Life Expectancy (2007)", size_max=40, log_x=True)
    return apply_design(fig)

# --- VIZ 4: Histogram ---
def viz_4():
    data = df[df["year"] == 2007]
    fig = px.histogram(data, x="lifeExp", nbins=15, title="Global Life Expectancy Distribution")
    # For histograms, adding a border to the bins often matches professional designs better
    fig.update_traces(marker_line_color=DESIGN_BG_COLOR, marker_line_width=2, marker_color=DESIGN_COLORS[2])
    return apply_design(fig)

# --- VIZ 5: Multiple Traces (Combo Chart) ---
def viz_5():
    # Say the design requires a line overlapping a bar chart
    fig = go.Figure()
    
    years = [2000, 2001, 2002, 2003, 2004]
    revenue = [10, 15, 13, 17, 20]
    profit = [2, 3, 2.5, 4, 5]
    
    fig.add_trace(go.Bar(x=years, y=revenue, name="Revenue", marker_color=DESIGN_COLORS[0]))
    fig.add_trace(go.Scatter(x=years, y=profit, name="Profit Margin", mode="lines+markers", 
                             line=dict(color=DESIGN_COLORS[3], width=3)))
    
    fig.update_layout(title="Revenue vs Profit Overlay")
    return apply_design(fig)

# --- UI Setup ---
CHARTS = {
    "1. Styled Line": viz_1,
    "2. Styled Bar": viz_2,
    "3. Styled Scatter": viz_3,
    "4. Styled Histogram": viz_4,
    "5. Combo Chart": viz_5
}

def update_plot(chart_name):
    return CHARTS[chart_name]()

with gr.Blocks() as app:
    gr.Markdown("# 🎨 Custom Designed Dashboard\nDemonstrating exact color matching and layout modifications.")
    tabs = gr.Radio(choices=list(CHARTS.keys()), value="1. Styled Line", label="Select Custom Chart")
    plot = gr.Plot(value=viz_1())

    tabs.change(fn=update_plot, inputs=tabs, outputs=plot)

# Uncomment to run standalone
if __name__ == "__main__":
    app.launch()