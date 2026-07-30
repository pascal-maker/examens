"""
Gradio frontend for the Robot Management System.
Run with:  python gradio_app.py
Make sure the FastAPI backend is already running on http://localhost:8000
"""
import gradio as gr
import requests

API = "http://localhost:8000/api"


# ─────────────────────────────────────────────────────────────
# HTTP helpers
# ─────────────────────────────────────────────────────────────
def _get(path):
    try:
        r = requests.get(API + path, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the API. Is the backend running?"
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e)) if e.response else str(e)
        return None, detail


def _post(path, payload):
    try:
        r = requests.post(API + path, json=payload, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the API. Is the backend running?"
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e)) if e.response else str(e)
        return None, detail


def _patch(path, params=None):
    try:
        r = requests.patch(API + path, params=params, timeout=5)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot reach the API. Is the backend running?"
    except requests.exceptions.HTTPError as e:
        detail = e.response.json().get("detail", str(e)) if e.response else str(e)
        return None, detail


# ─────────────────────────────────────────────────────────────
# Tab 1 — Overview (with location filter)
# ─────────────────────────────────────────────────────────────
def load_overview(location_filter=""):
    path = "/robots/"
    if location_filter and location_filter.strip():
        path += f"?location={location_filter.strip()}"
    robots, err = _get(path)
    if err:
        return f"**Error:** {err}"
    if not robots:
        msg = f"No robots found in **{location_filter}**." if location_filter.strip() else "No robots found."
        return msg
    lines = [
        "| ID | Name | Location | IP Address | Current Functionality |",
        "|----|------|----------|------------|----------------------|",
    ]
    for r in robots:
        func = r.get("functionality") or {}
        func_name = func.get("name", "—") if func else "—"
        lines.append(
            f"| {r['id']} | {r['name']} | {r.get('location') or '—'} "
            f"| `{r.get('ip_address') or '—'}` | {func_name} |"
        )
    return "\n".join(lines)


def get_location_choices():
    robots, _ = _get("/robots/")
    if not robots:
        return [""]
    locs = sorted({r.get("location") for r in robots if r.get("location")})
    return [""] + locs


# ─────────────────────────────────────────────────────────────
# Tab 2 — Create new functionality
# ─────────────────────────────────────────────────────────────
def create_functionality(name, description):
    name = (name or "").strip()
    if not name:
        return "**Error:** Name is required."
    data, err = _post("/functionalities/", {"name": name, "description": description or None})
    if err:
        return f"**Error:** {err}"
    return f"✓ Created functionality **#{data['id']}: {data['name']}**"


def get_functionality_choices():
    funcs, _ = _get("/functionalities/")
    if not funcs:
        return ["— none —"]
    return ["— none —"] + [f"{f['id']}: {f['name']}" for f in funcs]


# ─────────────────────────────────────────────────────────────
# Tab 3 — Create new robot
# ─────────────────────────────────────────────────────────────
def create_robot(name, location, ip_address, func_choice):
    name = (name or "").strip()
    if not name:
        return "**Error:** Robot name is required."
    func_id = None
    if func_choice and func_choice != "— none —":
        func_id = int(func_choice.split(":")[0])
    payload = {
        "name": name,
        "location": location or None,
        "ip_address": ip_address or None,
        "current_functionality_id": func_id,
    }
    data, err = _post("/robots/", payload)
    if err:
        return f"**Error:** {err}"
    func_name = (data.get("functionality") or {}).get("name", "none")
    return f"✓ Created robot **#{data['id']}: {data['name']}** — functionality: {func_name}"


# ─────────────────────────────────────────────────────────────
# Tab 4 — Manage robot functionality
# ─────────────────────────────────────────────────────────────
def get_robot_choices():
    robots, _ = _get("/robots/")
    if not robots:
        return []
    return [f"{r['id']}: {r['name']}" for r in robots]


def show_current_assignment(robot_choice):
    """Return a summary of the robot's current state when selected."""
    if not robot_choice:
        return ""
    robot_id = int(robot_choice.split(":")[0])
    robot, err = _get(f"/robots/{robot_id}")
    if err:
        return f"**Error:** {err}"
    func = robot.get("functionality") or {}
    func_name = func.get("name", "none") if func else "none"
    return (
        f"**{robot['name']}** — "
        f"location: {robot.get('location') or '—'} | "
        f"IP: `{robot.get('ip_address') or '—'}` | "
        f"current functionality: **{func_name}**"
    )


def assign_functionality(robot_choice, func_choice):
    if not robot_choice:
        return "Please select a robot."
    robot_id = int(robot_choice.split(":")[0])

    if func_choice and func_choice != "— none —":
        func_id = int(func_choice.split(":")[0])
        data, err = _patch(
            f"/robots/{robot_id}/functionality/set",
            params={"functionality_id": func_id},
        )
    else:
        data, err = _patch(f"/robots/{robot_id}/functionality/clear")

    if err:
        return f"**Error:** {err}"
    func_name = (data.get("functionality") or {}).get("name", "none")
    return f"✓ **{data['name']}** — current functionality is now: **{func_name}**"


# ─────────────────────────────────────────────────────────────
# Build the Gradio app
# ─────────────────────────────────────────────────────────────
with gr.Blocks(title="Robot Dashboard") as app:
    gr.Markdown("# Robot Management Dashboard")

    # ── Tab 1: Overview ──────────────────────────────────────
    with gr.Tab("Overview"):
        gr.Markdown("### All robots and their current functionality")
        with gr.Row():
            loc_filter = gr.Dropdown(
                label="Filter by location",
                choices=get_location_choices(),
                value="",
                allow_custom_value=True,
            )
            refresh_btn = gr.Button("Refresh", scale=0)
        overview_md = gr.Markdown(value=load_overview())

        loc_filter.change(fn=load_overview, inputs=loc_filter, outputs=overview_md)
        refresh_btn.click(
            fn=lambda loc: (load_overview(loc), gr.update(choices=get_location_choices())),
            inputs=loc_filter,
            outputs=[overview_md, loc_filter],
        )

    # ── Tab 2: Create Functionality ──────────────────────────
    with gr.Tab("Create new functionality"):
        gr.Markdown("### Add a new functionality")
        func_name_in = gr.Textbox(label="Name *", placeholder="e.g. Navigate")
        func_desc_in = gr.Textbox(label="Description", placeholder="What does it do?", lines=2)
        func_submit  = gr.Button("Create")
        func_result  = gr.Markdown()
        func_submit.click(
            fn=create_functionality,
            inputs=[func_name_in, func_desc_in],
            outputs=func_result,
        )

    # ── Tab 3: Create Robot ───────────────────────────────────
    with gr.Tab("Create new robot"):
        gr.Markdown("### Add a new robot")
        robot_name_in = gr.Textbox(label="Name *",        placeholder="e.g. Nova")
        robot_loc_in  = gr.Textbox(label="Location",      placeholder="e.g. Lab 3")
        robot_ip_in   = gr.Textbox(label="IP Address",    placeholder="e.g. 10.0.1.30")
        robot_func_dd = gr.Dropdown(
            label="Current Functionality",
            choices=get_functionality_choices(),
            value="— none —",
        )
        with gr.Row():
            robot_refresh = gr.Button("Refresh functionality list", scale=0)
            robot_submit  = gr.Button("Create Robot")
        robot_result = gr.Markdown()

        robot_refresh.click(
            fn=lambda: gr.update(choices=get_functionality_choices()),
            outputs=robot_func_dd,
        )
        robot_submit.click(
            fn=create_robot,
            inputs=[robot_name_in, robot_loc_in, robot_ip_in, robot_func_dd],
            outputs=robot_result,
        )

    # ── Tab 4: Manage Robot Functionality ────────────────────
    with gr.Tab("Manage robot functionality"):
        gr.Markdown("### Assign or clear a robot's current functionality")
        manage_robot_dd = gr.Dropdown(label="Select robot", choices=get_robot_choices())
        current_info    = gr.Markdown()   # shows current assignment on robot select
        manage_func_dd  = gr.Dropdown(
            label="New functionality (select '— none —' to clear)",
            choices=get_functionality_choices(),
            value="— none —",
        )
        with gr.Row():
            manage_refresh = gr.Button("Refresh lists", scale=0)
            manage_submit  = gr.Button("Apply")
        manage_result = gr.Markdown()

        # Show current assignment when a robot is chosen
        manage_robot_dd.change(
            fn=show_current_assignment,
            inputs=manage_robot_dd,
            outputs=current_info,
        )
        manage_refresh.click(
            fn=lambda: (
                gr.update(choices=get_robot_choices()),
                gr.update(choices=get_functionality_choices()),
            ),
            outputs=[manage_robot_dd, manage_func_dd],
        )
        manage_submit.click(
            fn=assign_functionality,
            inputs=[manage_robot_dd, manage_func_dd],
            outputs=manage_result,
        )


if __name__ == "__main__":
    app.launch()
