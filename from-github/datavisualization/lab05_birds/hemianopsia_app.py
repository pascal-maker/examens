import json
import gradio as gr
import plotly.graph_objects as go

# We attempt to load the json. If it's missing or empty, we use fallback data so the app doesn't crash!
try:
    with open("hemianopsia.json", "r") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print("Warning: hemianopsia.json not found or empty. Using dummy data!")
    data = {
        "seenPoints": [{"x": 10, "y": 10, "z": 50}, {"x": -20, "y": 5, "z": 45}],
        "unSeenPoints": [{"x": 30, "y": -10, "z": 40}, {"x": 15, "y": 20, "z": 55}],
        "reactionTimes": [250.5, 320.1]
    }

def make_hemianopsia_chart():
    seen = data.get("seenPoints", [])
    unseen = data.get("unSeenPoints", [])
    reaction_times = data.get("reactionTimes", [])

    fig = go.Figure()

    # seen points
    if seen:
        fig.add_trace(
            go.Scatter3d(
                x=[p["x"] for p in seen],
                y=[p["y"] for p in seen],
                z=[p["z"] for p in seen],
                mode="markers",
                name="Seen points",
                marker=dict(
                    size=6,
                    color=reaction_times,
                    colorscale="Viridis",
                    colorbar=dict(title="Reaction time (ms)"),
                ),
                text=[f"Reaction: {rt:.1f} ms" for rt in reaction_times],
                hovertemplate="x=%{x}<br>y=%{y}<br>z=%{z}<br>%{text}<extra></extra>",
            )
        )

    # unseen points
    if unseen:
        fig.add_trace(
            go.Scatter3d(
                x=[p["x"] for p in unseen],
                y=[p["y"] for p in unseen],
                z=[p["z"] for p in unseen],
                mode="markers",
                name="Unseen points",
                marker=dict(size=8, color="red", symbol="diamond"),
                hovertemplate="x=%{x}<br>y=%{y}<br>z=%{z}<br>Unseen<extra></extra>",
            )
        )

    # fixation center
    fig.add_trace(
        go.Scatter3d(
            x=[0],
            y=[0],
            z=[55],
            mode="markers+text",
            name="Fixation point",
            marker=dict(size=10, color="black"),
            text=["Fixation"],
            textposition="top center",
        )
    )

    fig.update_layout(
        title="Hemianopsia Visual Field",
        scene=dict(
            xaxis_title="Horizontal",
            yaxis_title="Vertical",
            zaxis_title="Depth",
        ),
        height=700,
    )
    return fig

with gr.Blocks() as demo:
    gr.Markdown("# Hemianopsia Visualization")
    gr.Markdown("This 3D chart maps seen vs unseen points in the visual field, including reaction times.")
    plot = gr.Plot(value=make_hemianopsia_chart())

if __name__ == "__main__":
    demo.launch()
