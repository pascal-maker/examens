from typing import Any

import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app_config import get_settings
from frontend.api_client import ApiClientError, client


settings = get_settings()

CAR_COLUMNS = [
    "id",
    "license_plate",
    "brand",
    "model",
    "owner_name",
    "kilometrage",
    "maintenance_threshold",
    "open_warning_count",
    "assigned_bay_name",
]
CAR_WARNING_COLUMNS = [
    "car_id",
    "license_plate",
    "owner_name",
    "kilometrage",
    "maintenance_threshold",
    "warning_repair_id",
    "created_at",
]
REPAIR_COLUMNS = [
    "id",
    "car_id",
    "car_license_plate",
    "repair_type",
    "mechanic",
    "status",
    "cost_estimate",
    "final_cost",
    "service_bay_id",
    "service_bay_name",
    "created_at",
    "completed_at",
]
REPAIR_WARNING_COLUMNS = [
    "repair_id",
    "car_id",
    "license_plate",
    "repair_type",
    "created_at",
]
BAY_COLUMNS = [
    "id",
    "bay_name",
    "bay_type",
    "available",
    "notes",
    "current_car_id",
    "current_license_plate",
    "active_repair_id",
]
LOG_COLUMNS = [
    "timestamp",
    "entity_type",
    "entity_id",
    "action",
    "message",
    "old_value_json",
    "new_value_json",
]


def _df(rows, columns):
    if not rows:
        return pd.DataFrame(columns=columns)
    frame = pd.DataFrame(rows)
    for column in columns:
        if column not in frame.columns:
            frame[column] = None
    return frame[columns]


def _empty_figure(title):
    figure = go.Figure()
    figure.update_layout(title=title, template="plotly_white")
    figure.add_annotation(text="No data available yet", showarrow=False, x=0.5, y=0.5, xref="paper", yref="paper")
    return figure


def _build_repairs_per_day_chart(rows):
    if not rows:
        return _empty_figure("Repairs Per Day")
    frame = pd.DataFrame(rows)
    return px.bar(frame, x="date", y="count", title="Repairs Per Day", text="count")


def _build_status_cost_chart(rows):
    if not rows:
        return _empty_figure("Repair Cost by Status")
    frame = pd.DataFrame(rows)
    return px.pie(frame, names="label", values="value", title="Repair Cost by Status", hole=0.4)


def _build_bay_usage_chart(rows):
    if not rows:
        return _empty_figure("Service Bay Occupancy")
    frame = pd.DataFrame(rows)
    return px.bar(frame, x="label", y="value", title="Service Bay Occupancy", labels={"label": "Service Bay", "value": "Occupied Slots"})


def _require_int(value, label):
    if value is None:
        raise gr.Error(f"{label} is required.")
    return int(value)


def refresh_dashboard() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, go.Figure, go.Figure, go.Figure]:
    cars = client.get("/api/v1/cars")
    car_warnings = client.get("/api/v1/cars/warnings")
    repairs = client.get("/api/v1/repairs")
    repair_warnings = client.get("/api/v1/repairs/warnings")
    bays = client.get("/api/v1/service-bays")
    logs = client.get("/api/v1/logs")
    repairs_per_day = client.get("/api/v1/analytics/repairs-per-day")
    repair_status_costs = client.get("/api/v1/analytics/repair-status-costs")
    bay_usage = client.get("/api/v1/analytics/bay-usage")
    return (
        _df(cars, CAR_COLUMNS),
        _df(car_warnings, CAR_WARNING_COLUMNS),
        _df(repairs, REPAIR_COLUMNS),
        _df(repair_warnings, REPAIR_WARNING_COLUMNS),
        _df(bays, BAY_COLUMNS),
        _df(logs, LOG_COLUMNS),
        _build_repairs_per_day_chart(repairs_per_day),
        _build_status_cost_chart(repair_status_costs),
        _build_bay_usage_chart(bay_usage),
    )


def refresh_logs(entity_type: str, action: str, limit: float | None) -> pd.DataFrame:
    params: dict[str, Any] = {"limit": int(limit or 200)}
    if entity_type.strip():
        params["entity_type"] = entity_type.strip()
    if action.strip():
        params["action"] = action.strip()
    logs = client.get("/api/v1/logs", params=params)
    return _df(logs, LOG_COLUMNS)


def _successful_refresh(message):
    gr.Success(message)
    return refresh_dashboard()


def create_car(license_plate: str, brand: str, model: str, owner_name: str, kilometrage: float | None, maintenance_threshold: float | None):
    client.post(
        "/api/v1/cars",
        {
            "license_plate": license_plate,
            "brand": brand,
            "model": model,
            "owner_name": owner_name,
            "kilometrage": _require_int(kilometrage, "Kilometrage"),
            "maintenance_threshold": _require_int(maintenance_threshold, "Maintenance threshold"),
        },
    )
    return _successful_refresh("Car created successfully.")


def update_car(car_id: float | None, license_plate: str, brand: str, model: str, owner_name: str, kilometrage: float | None, maintenance_threshold: float | None):
    car_id_value = _require_int(car_id, "Car ID")
    payload: dict[str, Any] = {}
    if license_plate:
        payload["license_plate"] = license_plate
    if brand:
        payload["brand"] = brand
    if model:
        payload["model"] = model
    if owner_name:
        payload["owner_name"] = owner_name
    if kilometrage is not None:
        payload["kilometrage"] = int(kilometrage)
    if maintenance_threshold is not None:
        payload["maintenance_threshold"] = int(maintenance_threshold)
    if not payload:
        raise gr.Error("Provide at least one field to update the car.")
    client.patch(f"/api/v1/cars/{car_id_value}", payload)
    return _successful_refresh(f"Car {car_id_value} updated successfully.")


def delete_car(car_id: float | None):
    car_id_value = _require_int(car_id, "Car ID")
    client.delete(f"/api/v1/cars/{car_id_value}")
    return _successful_refresh(f"Car {car_id_value} deleted successfully.")


def assign_car_to_bay(car_id: float | None, bay_id: float | None):
    car_id_value = _require_int(car_id, "Car ID")
    bay_id_value = _require_int(bay_id, "Bay ID")
    client.post(f"/api/v1/cars/{car_id_value}/assign-bay", {"bay_id": bay_id_value})
    return _successful_refresh(f"Car {car_id_value} assigned to bay {bay_id_value}.")


def create_repair(
    car_id: float | None,
    repair_type: str,
    mechanic: str,
    status_value: str,
    cost_estimate: float | None,
    final_cost: float | None,
    service_bay_id: float | None,
):
    payload: dict[str, Any] = {
        "car_id": _require_int(car_id, "Car ID"),
        "repair_type": repair_type,
        "mechanic": mechanic or None,
        "status": status_value,
        "cost_estimate": cost_estimate,
        "final_cost": final_cost,
        "service_bay_id": int(service_bay_id) if service_bay_id is not None else None,
    }
    client.post("/api/v1/repairs", payload)
    return _successful_refresh("Repair created successfully.")


def update_repair(
    repair_id: float | None,
    repair_type: str,
    mechanic: str,
    status_value: str | None,
    cost_estimate: float | None,
    final_cost: float | None,
    service_bay_id: float | None,
):
    repair_id_value = _require_int(repair_id, "Repair ID")
    payload: dict[str, Any] = {}
    if repair_type:
        payload["repair_type"] = repair_type
    if mechanic:
        payload["mechanic"] = mechanic
    if status_value:
        payload["status"] = status_value
    if cost_estimate is not None:
        payload["cost_estimate"] = cost_estimate
    if final_cost is not None:
        payload["final_cost"] = final_cost
    if service_bay_id is not None:
        payload["service_bay_id"] = int(service_bay_id)
    if not payload:
        raise gr.Error("Provide at least one field to update the repair.")
    client.patch(f"/api/v1/repairs/{repair_id_value}", payload)
    return _successful_refresh(f"Repair {repair_id_value} updated successfully.")


def start_repair(repair_id: float | None):
    repair_id_value = _require_int(repair_id, "Repair ID")
    client.post(f"/api/v1/repairs/{repair_id_value}/start")
    return _successful_refresh(f"Repair {repair_id_value} started.")


def complete_repair(repair_id: float | None, final_cost: float | None):
    repair_id_value = _require_int(repair_id, "Repair ID")
    client.post(f"/api/v1/repairs/{repair_id_value}/complete", {"final_cost": final_cost})
    return _successful_refresh(f"Repair {repair_id_value} completed.")


def delete_repair(repair_id: float | None):
    repair_id_value = _require_int(repair_id, "Repair ID")
    client.delete(f"/api/v1/repairs/{repair_id_value}")
    return _successful_refresh(f"Repair {repair_id_value} deleted.")


def assign_repair_to_bay(repair_id: float | None, bay_id: float | None):
    repair_id_value = _require_int(repair_id, "Repair ID")
    bay_id_value = _require_int(bay_id, "Bay ID")
    client.post(f"/api/v1/repairs/{repair_id_value}/assign-bay", {"bay_id": bay_id_value})
    return _successful_refresh(f"Repair {repair_id_value} assigned to bay {bay_id_value}.")


def create_bay(bay_name: str, bay_type: str, available: bool, notes: str):
    client.post(
        "/api/v1/service-bays",
        {
            "bay_name": bay_name,
            "bay_type": bay_type,
            "available": available,
            "notes": notes or None,
        },
    )
    return _successful_refresh("Service bay created successfully.")


def delete_bay(bay_id: float | None):
    bay_id_value = _require_int(bay_id, "Bay ID")
    client.delete(f"/api/v1/service-bays/{bay_id_value}")
    return _successful_refresh(f"Service bay {bay_id_value} deleted.")


def assign_bay_car(bay_id: float | None, car_id: float | None):
    bay_id_value = _require_int(bay_id, "Bay ID")
    car_id_value = _require_int(car_id, "Car ID")
    client.post(f"/api/v1/service-bays/{bay_id_value}/assign-car", {"car_id": car_id_value})
    return _successful_refresh(f"Bay {bay_id_value} assigned to car {car_id_value}.")


def release_bay(bay_id: float | None):
    bay_id_value = _require_int(bay_id, "Bay ID")
    client.post(f"/api/v1/service-bays/{bay_id_value}/release")
    return _successful_refresh(f"Service bay {bay_id_value} released.")


def guarded_refresh():
    try:
        return refresh_dashboard()
    except ApiClientError as exc:
        raise gr.Error(str(exc)) from exc


def _wrap_action(action):
    def runner(*args):
        try:
            return action(*args)
        except (ApiClientError, ValueError, TypeError) as exc:
            raise gr.Error(str(exc)) from exc

    return runner


with gr.Blocks(title=f"Garage Management - {settings.student_name}", theme=gr.themes.Soft()) as demo:
    gr.Markdown(f"# Garage Management System - {settings.student_name}")
    gr.Markdown(
        "Production-style FastAPI + PostgreSQL + Gradio stack. "
        f"Backend API base URL: `{settings.garage_api_base_url}`"
    )

    with gr.Tab("Cars"):
        gr.Markdown("Manage vehicles, kilometrage updates, warnings, and bay assignments.")
        with gr.Row():
            with gr.Column():
                license_plate_input = gr.Textbox(label="License Plate")
                brand_input = gr.Textbox(label="Brand")
                model_input = gr.Textbox(label="Model")
                owner_name_input = gr.Textbox(label="Owner Name")
                kilometrage_input = gr.Number(label="Kilometrage", value=0, precision=0)
                maintenance_threshold_input = gr.Number(label="Maintenance Threshold", value=0, precision=0)
                create_car_button = gr.Button("Add Car", variant="primary")
            with gr.Column():
                update_car_id_input = gr.Number(label="Car ID to Update", precision=0)
                update_license_plate_input = gr.Textbox(label="New License Plate")
                update_brand_input = gr.Textbox(label="New Brand")
                update_model_input = gr.Textbox(label="New Model")
                update_owner_name_input = gr.Textbox(label="New Owner Name")
                update_kilometrage_input = gr.Number(label="New Kilometrage", precision=0)
                update_threshold_input = gr.Number(label="New Maintenance Threshold", precision=0)
                update_car_button = gr.Button("Update Car")
        with gr.Row():
            delete_car_id_input = gr.Number(label="Car ID to Delete", precision=0)
            delete_car_button = gr.Button("Delete Car", variant="stop")
            assign_car_id_input = gr.Number(label="Car ID for Bay Assignment", precision=0)
            assign_car_bay_input = gr.Number(label="Bay ID", precision=0)
            assign_car_button = gr.Button("Assign Car to Bay")
        refresh_cars_button = gr.Button("Refresh Cars Data")
        gr.Markdown("### Fleet Overview")
        cars_table = gr.Dataframe(label="Cars", interactive=False)
        gr.Markdown("### Maintenance Warning Queue")
        car_warnings_table = gr.Dataframe(label="Maintenance Warnings", interactive=False)

    with gr.Tab("Repairs"):
        gr.Markdown("Handle repair creation, status workflow, pricing, and mechanic assignments.")
        with gr.Row():
            with gr.Column():
                repair_car_id_input = gr.Number(label="Car ID", precision=0)
                repair_type_input = gr.Textbox(label="Repair Type")
                repair_mechanic_input = gr.Textbox(label="Mechanic")
                repair_status_input = gr.Dropdown(
                    label="Status",
                    choices=["warning", "pending", "in_progress", "completed"],
                    value="pending",
                )
                repair_cost_estimate_input = gr.Number(label="Cost Estimate")
                repair_final_cost_input = gr.Number(label="Final Cost")
                repair_bay_input = gr.Number(label="Service Bay ID")
                create_repair_button = gr.Button("Create Repair", variant="primary")
            with gr.Column():
                update_repair_id_input = gr.Number(label="Repair ID to Update", precision=0)
                update_repair_type_input = gr.Textbox(label="New Repair Type")
                update_repair_mechanic_input = gr.Textbox(label="New Mechanic")
                update_repair_status_input = gr.Dropdown(
                    label="New Status",
                    choices=["warning", "pending", "in_progress", "completed"],
                    value=None,
                )
                update_repair_cost_estimate_input = gr.Number(label="New Cost Estimate")
                update_repair_final_cost_input = gr.Number(label="New Final Cost")
                update_repair_bay_input = gr.Number(label="New Service Bay ID")
                update_repair_button = gr.Button("Update Repair")
        with gr.Row():
            start_repair_id_input = gr.Number(label="Repair ID to Start", precision=0)
            start_repair_button = gr.Button("Start Repair")
            complete_repair_id_input = gr.Number(label="Repair ID to Complete", precision=0)
            complete_repair_final_cost_input = gr.Number(label="Completion Final Cost")
            complete_repair_button = gr.Button("Complete Repair")
        with gr.Row():
            delete_repair_id_input = gr.Number(label="Repair ID to Delete", precision=0)
            delete_repair_button = gr.Button("Delete Repair", variant="stop")
            assign_repair_id_input = gr.Number(label="Repair ID for Bay Assignment", precision=0)
            assign_repair_bay_input = gr.Number(label="Bay ID", precision=0)
            assign_repair_button = gr.Button("Assign Repair to Bay")
        refresh_repairs_button = gr.Button("Refresh Repairs Data")
        gr.Markdown("### Repair Pipeline")
        repairs_table = gr.Dataframe(label="Repairs", interactive=False)
        gr.Markdown("### Warning Repairs")
        repair_warnings_table = gr.Dataframe(label="Repair Warnings", interactive=False)

    with gr.Tab("Service Bays"):
        gr.Markdown("Monitor capacity, create or remove bays, and release occupied bays.")
        with gr.Row():
            bay_name_input = gr.Textbox(label="Bay Name")
            bay_type_input = gr.Textbox(label="Bay Type")
            bay_available_input = gr.Checkbox(label="Available", value=True)
            bay_notes_input = gr.Textbox(label="Notes")
            create_bay_button = gr.Button("Add Service Bay", variant="primary")
        with gr.Row():
            delete_bay_id_input = gr.Number(label="Bay ID to Delete", precision=0)
            delete_bay_button = gr.Button("Delete Bay", variant="stop")
            assign_bay_id_input = gr.Number(label="Bay ID to Assign", precision=0)
            assign_bay_car_id_input = gr.Number(label="Car ID", precision=0)
            assign_bay_button = gr.Button("Assign Car")
            release_bay_id_input = gr.Number(label="Bay ID to Release", precision=0)
            release_bay_button = gr.Button("Release Bay")
        refresh_bays_button = gr.Button("Refresh Service Bay Data")
        gr.Markdown("### Bay Usage")
        bays_table = gr.Dataframe(label="Service Bays", interactive=False)

    with gr.Tab("Analytics"):
        gr.Markdown("Live Plotly analytics built from backend data.")
        refresh_analytics_button = gr.Button("Refresh Analytics")
        repairs_per_day_plot = gr.Plot(label="Repairs Per Day")
        repair_status_cost_plot = gr.Plot(label="Repair Cost by Status")
        bay_usage_plot = gr.Plot(label="Service Bay Occupancy")

    with gr.Tab("Logs"):
        gr.Markdown("Optional audit trail with entity and action filtering.")
        with gr.Row():
            log_entity_filter = gr.Textbox(label="Filter by Entity Type")
            log_action_filter = gr.Textbox(label="Filter by Action")
            log_limit_filter = gr.Number(label="Limit", value=200, precision=0)
            filter_logs_button = gr.Button("Filter Logs")
        logs_table = gr.Dataframe(label="Audit Logs", interactive=False)

    refresh_outputs = [
        cars_table,
        car_warnings_table,
        repairs_table,
        repair_warnings_table,
        bays_table,
        logs_table,
        repairs_per_day_plot,
        repair_status_cost_plot,
        bay_usage_plot,
    ]

    demo.load(guarded_refresh, outputs=refresh_outputs)
    create_car_button.click(
        _wrap_action(create_car),
        inputs=[
            license_plate_input,
            brand_input,
            model_input,
            owner_name_input,
            kilometrage_input,
            maintenance_threshold_input,
        ],
        outputs=refresh_outputs,
    )
    update_car_button.click(
        _wrap_action(update_car),
        inputs=[
            update_car_id_input,
            update_license_plate_input,
            update_brand_input,
            update_model_input,
            update_owner_name_input,
            update_kilometrage_input,
            update_threshold_input,
        ],
        outputs=refresh_outputs,
    )
    delete_car_button.click(_wrap_action(delete_car), inputs=[delete_car_id_input], outputs=refresh_outputs)
    assign_car_button.click(
        _wrap_action(assign_car_to_bay),
        inputs=[assign_car_id_input, assign_car_bay_input],
        outputs=refresh_outputs,
    )
    refresh_cars_button.click(guarded_refresh, outputs=refresh_outputs)

    create_repair_button.click(
        _wrap_action(create_repair),
        inputs=[
            repair_car_id_input,
            repair_type_input,
            repair_mechanic_input,
            repair_status_input,
            repair_cost_estimate_input,
            repair_final_cost_input,
            repair_bay_input,
        ],
        outputs=refresh_outputs,
    )
    update_repair_button.click(
        _wrap_action(update_repair),
        inputs=[
            update_repair_id_input,
            update_repair_type_input,
            update_repair_mechanic_input,
            update_repair_status_input,
            update_repair_cost_estimate_input,
            update_repair_final_cost_input,
            update_repair_bay_input,
        ],
        outputs=refresh_outputs,
    )
    start_repair_button.click(_wrap_action(start_repair), inputs=[start_repair_id_input], outputs=refresh_outputs)
    complete_repair_button.click(
        _wrap_action(complete_repair),
        inputs=[complete_repair_id_input, complete_repair_final_cost_input],
        outputs=refresh_outputs,
    )
    delete_repair_button.click(_wrap_action(delete_repair), inputs=[delete_repair_id_input], outputs=refresh_outputs)
    assign_repair_button.click(
        _wrap_action(assign_repair_to_bay),
        inputs=[assign_repair_id_input, assign_repair_bay_input],
        outputs=refresh_outputs,
    )
    refresh_repairs_button.click(guarded_refresh, outputs=refresh_outputs)

    create_bay_button.click(
        _wrap_action(create_bay),
        inputs=[bay_name_input, bay_type_input, bay_available_input, bay_notes_input],
        outputs=refresh_outputs,
    )
    delete_bay_button.click(_wrap_action(delete_bay), inputs=[delete_bay_id_input], outputs=refresh_outputs)
    assign_bay_button.click(
        _wrap_action(assign_bay_car),
        inputs=[assign_bay_id_input, assign_bay_car_id_input],
        outputs=refresh_outputs,
    )
    release_bay_button.click(_wrap_action(release_bay), inputs=[release_bay_id_input], outputs=refresh_outputs)
    refresh_bays_button.click(guarded_refresh, outputs=refresh_outputs)
    refresh_analytics_button.click(guarded_refresh, outputs=refresh_outputs)

    filter_logs_button.click(
        _wrap_action(refresh_logs),
        inputs=[log_entity_filter, log_action_filter, log_limit_filter],
        outputs=[logs_table],
    )


if __name__ == "__main__":
    demo.launch(server_name=settings.frontend_host, server_port=settings.frontend_port)
