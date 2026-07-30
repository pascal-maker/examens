import json
import gradio as gr
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ─────────────────────────────────────────────────────────────────────
# DATASET 1: Hemianopsia  (inline – real patient data from the assignment)
# ─────────────────────────────────────────────────────────────────────
HEMIANOPSIA_DATA = {
    "time": 1709550269540,
    "id": "Hemianopsia-396373",
    "fakePercent": 0,
    "unSeenPoints": [
        {"z": 55.138145446777344, "x": -20.06864356994629, "y": -6.167179107666016}
    ],
    "fixationPercent": 100,
    "reactionTimes": [
        682.70, 391.75, 362.61, 306.42, 291.98, 265.01, 374.38, 343.15,
        334.64, 290.01, 321.00, 320.36, 306.85, 347.71, 320.56,
        292.50, 583.44, 376.84, 457.56
    ],
    "seenPoints": [
        {"y": -19.20852279663086,  "z": 54.938087463378906,  "x": -9.687067985534668},
        {"y": -6.167180061340332,  "z": 57.78535842895508,   "x": 10.189117431640625},
        {"x": -10.168876647949219, "z": 57.67055892944336,   "y": 7.1902923583984375},
        {"x": 10.168876647949219,  "z": 57.67055892944336,   "y": 7.1902923583984375},
        {"y": -6.167180061340332,  "z": 57.78535842895508,   "x": -10.189117431640625},
        {"y": -6.167180061340332,  "z": 58.67679214477539,   "x": 0},
        {"z": 55.02861022949219,   "x": 20.028778076171875,  "y": 7.190291404724121},
        {"y": 20.17919158935547,   "z": 54.599578857421875,  "x": -9.627378463745117},
        {"z": 55.441864013671875,  "y": 20.179189682006836,  "x": 0},
        {"y": 7.190291881561279,   "z": 58.56022262573242,   "x": 0},
        {"y": -19.20852279663086,  "x": 9.687067985534668,   "z": 54.938087463378906},
        {"z": 52.42131042480469,   "y": -19.20852279663086,  "x": 19.079801559448242},
        {"y": 7.190291404724121,   "z": 55.02861022949219,   "x": -20.028778076171875},
        {"y": 20.17919158935547,   "z": 54.599578857421875,  "x": 9.627378463745117},
        {"z": 55.138145446777344,  "y": -6.167179107666016,  "x": 20.06864356994629},
        {"x": -19.079801559448242, "y": -19.20852279663086,  "z": 52.42131042480469},
        {"z": 52.09830856323242,   "y": 20.179189682006836,  "x": 18.96223258972168},
        {"z": 52.09830856323242,   "y": 20.179189682006836,  "x": -18.96223258972168},
        {"x": 0,                   "z": 55.78559494018555,   "y": -19.208520889282227}
    ],
    "settings": {
        "speed": 2, "stimuliCount": 10,
        "fakeChance": 0.2, "verticalFOV": 40,
        "delay": 1, "horizontalFOV": 40
    }
}

# ─────────────────────────────────────────────────────────────────────
# DATASET 2: Motor Amplification  (load from json files)
# ─────────────────────────────────────────────────────────────────────
def load_motor_data(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Could not load {path}: {e}")
        return None

motor_005774 = load_motor_data("005774.json")
motor_479379 = load_motor_data("479379.json")
motor_926818 = load_motor_data("926818.json")
star_341980  = load_motor_data("341980.json")

# ─────────────────────────────────────────────────────────────────────
# CHART 1: Hemianopsia 3D Scatter
# ─────────────────────────────────────────────────────────────────────
def make_hemianopsia_chart():
    d = HEMIANOPSIA_DATA
    seen       = d["seenPoints"]
    unseen     = d["unSeenPoints"]
    rt         = d["reactionTimes"]
    settings   = d["settings"]
    fix_pct    = d["fixationPercent"]

    fig = go.Figure()

    # Seen points – colored by reaction time (Viridis scale)
    fig.add_trace(go.Scatter3d(
        x=[p["x"] for p in seen],
        y=[p["y"] for p in seen],
        z=[p["z"] for p in seen],
        mode="markers",
        name="Seen points",
        marker=dict(
            size=8,
            color=rt,
            colorscale="Viridis",
            colorbar=dict(title="Reaction time (ms)", x=1.05),
            opacity=0.9,
            line=dict(color="white", width=0.5),
        ),
        text=[f"Reaction: {r:.1f} ms" for r in rt],
        hovertemplate="<b>Seen</b><br>x=%{x:.2f}  y=%{y:.2f}  z=%{z:.2f}<br>%{text}<extra></extra>",
    ))

    # Unseen points – red diamonds
    fig.add_trace(go.Scatter3d(
        x=[p["x"] for p in unseen],
        y=[p["y"] for p in unseen],
        z=[p["z"] for p in unseen],
        mode="markers",
        name="Unseen points",
        marker=dict(size=10, color="#FF4444", symbol="diamond", opacity=0.95,
                    line=dict(color="white", width=1)),
        hovertemplate="<b>Unseen</b><br>x=%{x:.2f}  y=%{y:.2f}  z=%{z:.2f}<extra></extra>",
    ))

    # Fixation point at origin (0, 0) projected to mean z
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[55],
        mode="markers+text",
        name="Fixation point",
        marker=dict(size=12, color="black", symbol="cross"),
        text=["Fixation (0,0)"],
        textposition="top center",
        hovertemplate="<b>Fixation point</b><extra></extra>",
    ))

    fig.update_layout(
        title=dict(
            text=f"<b>Hemianopsia Visual Field</b><br>"
                 f"<sup>ID: {d['id']} | Fixation: {fix_pct}% | "
                 f"FOV {settings['horizontalFOV']}°H × {settings['verticalFOV']}°V | "
                 f"Stimuli seen: {len(seen)} | Unseen: {len(unseen)}</sup>",
            x=0.5
        ),
        scene=dict(
            xaxis=dict(title="Horizontal (x)", backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),
            yaxis=dict(title="Vertical (y)",   backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),
            zaxis=dict(title="Depth (z)",       backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),
            bgcolor="#f8f9fa",
        ),
        legend=dict(x=0, y=1),
        height=720,
        paper_bgcolor="#ffffff",
    )
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 2: Motor Amplification – Horizontal path (one hand)
# ─────────────────────────────────────────────────────────────────────
def extract_coords(coord_list, axis):
    return [pt[axis] for pt in coord_list]

def make_motor_horizontal(data, title_suffix=""):
    if data is None:
        return go.Figure().add_annotation(text="Data not loaded", showarrow=False)

    fig = go.Figure()
    colors = {"LEFT":  {"actual": "#3A86FF", "adapted": "#FF006E"},
              "RIGHT": {"actual": "#8338EC", "adapted": "#FB5607"}}

    hand_key     = "handData"     if "handData"     in data else None
    adapted_key  = "adaptedHandData" if "adaptedHandData" in data else None

    sources = []
    if hand_key:    sources.append((data[hand_key],    "Actual",  False))
    if adapted_key: sources.append((data[adapted_key], "Adapted", True))

    for hand_data, label, dashed in sources:
        for entry in hand_data:
            hand  = entry.get("hand", "?")
            hcoords = entry.get("horizontalCoordinates", [])
            if not hcoords:
                continue
            x_vals = extract_coords(hcoords, "x")
            c = colors.get(hand, {"actual": "#aaa", "adapted": "#333"})
            col = c["adapted"] if dashed else c["actual"]

            fig.add_trace(go.Scatter(
                x=list(range(len(x_vals))),
                y=x_vals,
                mode="lines",
                name=f"{label} – {hand} (x)",
                line=dict(color=col, dash="dash" if dashed else "solid", width=2),
                hovertemplate=f"<b>{label} {hand} – x</b><br>step=%{{x}}<br>x=%{{y:.3f}}<extra></extra>",
            ))

    fig.update_layout(
        title=f"<b>Motor Amplification – Horizontal Movement{title_suffix}</b>",
        xaxis_title="Frame",
        yaxis_title="X coordinate (m)",
        height=500,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8f9fa",
        legend=dict(orientation="h", y=-0.2),
    )
    fig.update_xaxes(gridcolor="#dee2e6")
    fig.update_yaxes(gridcolor="#dee2e6", zeroline=True, zerolinecolor="#adb5bd")
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 3: Motor Amplification – Vertical path
# ─────────────────────────────────────────────────────────────────────
def make_motor_vertical(data, title_suffix=""):
    if data is None:
        return go.Figure().add_annotation(text="Data not loaded", showarrow=False)

    fig = go.Figure()
    colors = {"LEFT":  {"actual": "#3A86FF", "adapted": "#FF006E"},
              "RIGHT": {"actual": "#8338EC", "adapted": "#FB5607"}}

    hand_key    = "handData"        if "handData"        in data else None
    adapted_key = "adaptedHandData" if "adaptedHandData" in data else None

    sources = []
    if hand_key:    sources.append((data[hand_key],    "Actual",  False))
    if adapted_key: sources.append((data[adapted_key], "Adapted", True))

    for hand_data, label, dashed in sources:
        for entry in hand_data:
            hand    = entry.get("hand", "?")
            vcoords = entry.get("verticalCoordinates", [])
            if not vcoords:
                continue
            y_vals = extract_coords(vcoords, "y")
            col = colors.get(hand, {}).get("adapted" if dashed else "actual", "#999")

            fig.add_trace(go.Scatter(
                x=list(range(len(y_vals))),
                y=y_vals,
                mode="lines",
                name=f"{label} – {hand} (y)",
                line=dict(color=col, dash="dash" if dashed else "solid", width=2),
                hovertemplate=f"<b>{label} {hand} – y</b><br>step=%{{x}}<br>y=%{{y:.3f}}<extra></extra>",
            ))

    fig.update_layout(
        title=f"<b>Motor Amplification – Vertical Movement{title_suffix}</b>",
        xaxis_title="Frame",
        yaxis_title="Y coordinate (m) – height",
        height=500,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8f9fa",
        legend=dict(orientation="h", y=-0.2),
    )
    fig.update_xaxes(gridcolor="#dee2e6")
    fig.update_yaxes(gridcolor="#dee2e6", zeroline=True, zerolinecolor="#adb5bd")
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 4: Motor – 2D top-down path overlay (scatter)
# ─────────────────────────────────────────────────────────────────────
def make_motor_topdown(data, title_suffix=""):
    if data is None:
        return go.Figure().add_annotation(text="Data not loaded", showarrow=False)

    fig = go.Figure()
    colors = {"LEFT":  {"actual": "#3A86FF", "adapted": "#FF006E"},
              "RIGHT": {"actual": "#8338EC", "adapted": "#FB5607"}}

    hand_key    = "handData"        if "handData"        in data else None
    adapted_key = "adaptedHandData" if "adaptedHandData" in data else None

    sources = []
    if hand_key:    sources.append((data[hand_key],    "Actual",  False))
    if adapted_key: sources.append((data[adapted_key], "Adapted", True))

    for hand_data, label, dashed in sources:
        for entry in hand_data:
            hand    = entry.get("hand", "?")
            hcoords = entry.get("horizontalCoordinates", [])
            if not hcoords:
                continue
            xs = extract_coords(hcoords, "x")
            zs = extract_coords(hcoords, "z")
            col = colors.get(hand, {}).get("adapted" if dashed else "actual", "#999")

            fig.add_trace(go.Scatter(
                x=xs, y=zs,
                mode="lines+markers",
                name=f"{label} – {hand}",
                line=dict(color=col, dash="dash" if dashed else "solid", width=2),
                marker=dict(size=4),
                hovertemplate=f"<b>{label} {hand}</b><br>x=%{{x:.3f}}<br>z=%{{y:.3f}}<extra></extra>",
            ))

    fig.add_shape(type="circle", xref="x", yref="y",
                  x0=-0.02, y0=-0.02, x1=0.02, y1=0.02,
                  line_color="#2dc653", fillcolor="#2dc653", opacity=0.4)

    fig.update_layout(
        title=f"<b>Motor Amplification – Top-Down Path (x vs z){title_suffix}</b>",
        xaxis_title="X coordinate (horizontal)",
        yaxis_title="Z coordinate (depth)",
        height=520,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8f9fa",
        legend=dict(orientation="h", y=-0.2),
        yaxis=dict(scaleanchor="x", scaleratio=1),
    )
    fig.update_xaxes(gridcolor="#dee2e6", zeroline=True, zerolinecolor="#adb5bd")
    fig.update_yaxes(gridcolor="#dee2e6", zeroline=True, zerolinecolor="#adb5bd")
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 5: Star Cancellation – 3D scatter of all objects
# ─────────────────────────────────────────────────────────────────────
def make_star_cancellation_3d():
    if star_341980 is None:
        return go.Figure().add_annotation(text="341980.json not loaded", showarrow=False)

    objects = star_341980.get("objects", [])
    fig = go.Figure()

    # Group objects by type and selected status
    groups = {}
    for obj in objects:
        otype = obj["cancellationObjectType"]
        sel   = obj["selected"]
        key   = (otype, sel)
        if key not in groups:
            groups[key] = {"x": [], "y": [], "z": [], "ids": [], "quads": []}
        c = obj["coordinate"]
        groups[key]["x"].append(c["x"])
        groups[key]["y"].append(c["y"])
        groups[key]["z"].append(c["z"])
        groups[key]["ids"].append(obj["id"])
        groups[key]["quads"].append(obj["quadrant"])

    # Color/symbol mapping
    style = {
        ("SMALL_STAR", True):   {"color": "#2dc653", "symbol": "diamond",    "size": 8,  "name": "Small Star ✓ Selected"},
        ("SMALL_STAR", False):  {"color": "#FF4444", "symbol": "diamond",    "size": 8,  "name": "Small Star ✗ Missed"},
        ("BIG_STAR", True):     {"color": "#3A86FF", "symbol": "circle",     "size": 6,  "name": "Big Star ✓ Selected"},
        ("BIG_STAR", False):    {"color": "#adb5bd", "symbol": "circle",     "size": 6,  "name": "Big Star ✗ (distractor)"},
        ("WORD", True):         {"color": "#FB5607", "symbol": "square",     "size": 6,  "name": "Word ✓ Selected"},
        ("WORD", False):        {"color": "#dee2e6", "symbol": "square",     "size": 6,  "name": "Word ✗ (distractor)"},
    }

    for key, pts in groups.items():
        s = style.get(key, {"color": "#999", "symbol": "circle", "size": 5, "name": str(key)})
        fig.add_trace(go.Scatter3d(
            x=pts["x"], y=pts["y"], z=pts["z"],
            mode="markers",
            name=s["name"],
            marker=dict(size=s["size"], color=s["color"], symbol=s["symbol"],
                        opacity=0.85, line=dict(color="white", width=0.5)),
            text=[f"{oid} ({q})" for oid, q in zip(pts["ids"], pts["quads"])],
            hovertemplate="<b>%{text}</b><br>x=%{x:.3f}<br>y=%{y:.3f}<br>z=%{z:.3f}<extra></extra>",
        ))

    fig.update_layout(
        title=dict(
            text=f"<b>Star Cancellation Test</b><br>"
                 f"<sup>ID: {star_341980.get('id','')} | "
                 f"Objects: {len(objects)} | "
                 f"Selected: {sum(1 for o in objects if o['selected'])}/{len(objects)}</sup>",
            x=0.5
        ),
        scene=dict(
            xaxis=dict(title="X", backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),
            yaxis=dict(title="Y (height)", backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),
            zaxis=dict(title="Z (depth)", backgroundcolor="#f8f9fa", gridcolor="#dee2e6"),
            bgcolor="#f8f9fa",
        ),
        height=700,
        paper_bgcolor="#ffffff",
        legend=dict(x=0, y=1),
    )
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 6: Star Cancellation – Quadrant stats bar chart
# ─────────────────────────────────────────────────────────────────────
def make_star_quadrant_bar():
    if star_341980 is None:
        return go.Figure().add_annotation(text="341980.json not loaded", showarrow=False)

    qstats = star_341980.get("quadrantStats", [])
    quads  = [q["quadrantType"].replace("_", " ").title() for q in qstats]
    selected = [q["selectedAmountOfObjects"] for q in qstats]
    total    = [q["totalAmountOfObjects"] for q in qstats]
    pcts     = [q["selectedPercentage"] for q in qstats]

    colors_bar = ["#3A86FF", "#8338EC", "#FF006E", "#FB5607"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=quads, y=total, name="Total objects",
        marker_color="#dee2e6",
        text=total, textposition="auto",
    ))
    fig.add_trace(go.Bar(
        x=quads, y=selected, name="Selected",
        marker_color=colors_bar,
        text=[f"{s} ({p}%)" for s, p in zip(selected, pcts)],
        textposition="auto",
    ))

    fig.update_layout(
        title="<b>Star Cancellation – Selection per Quadrant</b>",
        xaxis_title="Quadrant",
        yaxis_title="Number of objects",
        barmode="overlay",
        height=450,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#f8f9fa",
        legend=dict(orientation="h", y=-0.15),
    )
    fig.update_xaxes(gridcolor="#dee2e6")
    fig.update_yaxes(gridcolor="#dee2e6")
    return fig

# ─────────────────────────────────────────────────────────────────────
# CHART 7: Star Cancellation – Object type breakdown (pie)
# ─────────────────────────────────────────────────────────────────────
def make_star_type_pie():
    if star_341980 is None:
        return go.Figure().add_annotation(text="341980.json not loaded", showarrow=False)

    ostats = star_341980.get("objectStats", [])
    labels = []
    values = []
    for s in ostats:
        lbl = s["cancellationObjectType"].replace("_", " ").title()
        d = s.get("direction", "")
        if d and d != "DIRECTION_UNSPECIFIED":
            lbl += f" ({d.title()})"
        labels.append(lbl)
        values.append(s["selectedAmountOfObjects"])

    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        marker=dict(colors=["#adb5bd", "#dee2e6", "#2dc653", "#FF006E"]),
        textinfo="label+value+percent",
        hole=0.35,
    ))
    fig.update_layout(
        title="<b>Star Cancellation – Selected Objects by Type</b>",
        height=450,
        paper_bgcolor="#ffffff",
    )
    return fig


# ─────────────────────────────────────────────────────────────────────
# GRADIO APP
# ─────────────────────────────────────────────────────────────────────
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
# 🏥 XRehab Data Visualization
### Lab exercise — Hemianopsia, Motor Amplification & Star Cancellation
---
""")

    with gr.Tab("👁️ Hemianopsia"):
        gr.Markdown("""
**Hemianopsia Visual Field Test**

Each point represents a stimulus shown in the 40°×40° visual field.
- 🟢 **Seen points** — colored by reaction time (ms). Darker = faster.
- 🔴 **Unseen points** — the patient did not react to these stimuli.
- ⬛ **Fixation point** — the center (0,0) where the patient must keep looking.

Rotate the 3D chart with your mouse!
""")
        hemi_plot = gr.Plot(value=make_hemianopsia_chart())

    with gr.Tab("💪 Motor – 005774"):
        gr.Markdown("""
**Motor Amplification — Patient 005774**

This file contains `handData` only (no adapted data).
- **Solid lines** = actual hand movement
""")
        with gr.Row():
            gr.Plot(value=make_motor_horizontal(motor_005774, " (005774)"))
            gr.Plot(value=make_motor_vertical(motor_005774,   " (005774)"))
        gr.Plot(value=make_motor_topdown(motor_005774, " (005774)"))

    with gr.Tab("💪 Motor – 479379"):
        gr.Markdown("""
**Motor Amplification — Patient 479379**

This file contains both `handData` AND `adaptedHandData`.
- **Solid lines** = actual hand position
- **Dashed lines** = adapted / amplified target position

Compare the gap between where the patient moved and where the app wanted them to reach.
""")
        with gr.Row():
            gr.Plot(value=make_motor_horizontal(motor_479379, " (479379)"))
            gr.Plot(value=make_motor_vertical(motor_479379,   " (479379)"))
        gr.Plot(value=make_motor_topdown(motor_479379, " (479379)"))

    with gr.Tab("💪 Motor – 926818"):
        gr.Markdown("""
**Motor Amplification — Patient 926818**

Another patient dataset with `handData`.
""")
        with gr.Row():
            gr.Plot(value=make_motor_horizontal(motor_926818, " (926818)"))
            gr.Plot(value=make_motor_vertical(motor_926818,   " (926818)"))
        gr.Plot(value=make_motor_topdown(motor_926818, " (926818)"))

    with gr.Tab("⭐ Star Cancellation"):
        gr.Markdown("""
**Star Cancellation Test — 341980**

This neuropsychological test checks for visual neglect.
The patient must find and select all **small stars** among distractors (big stars, words).
- 🟢 **Green diamonds** = small stars the patient found
- 🔴 **Red diamonds** = small stars the patient missed
- 🔵 / ⚪ = big stars and words (distractors)
""")
        gr.Plot(value=make_star_cancellation_3d())
        with gr.Row():
            gr.Plot(value=make_star_quadrant_bar())
            gr.Plot(value=make_star_type_pie())

if __name__ == "__main__":
    demo.launch()
