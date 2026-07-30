import os
from typing import Any

from flask import Flask, jsonify
import requests_unixsocket

app = Flask(__name__)
session = requests_unixsocket.Session()
DOCKER_API = "http+unix://%2Fvar%2Frun%2Fdocker.sock"
COMPOSE_PROJECT = os.getenv("COMPOSE_PROJECT", "depends_on_health_demo")
MANAGED_SERVICES = {
    s.strip() for s in os.getenv("MANAGED_SERVICES", "api,delayed-ui").split(",") if s.strip()
}


def docker_get(path: str):
    return session.get(f"{DOCKER_API}{path}", timeout=2)


def docker_post(path: str):
    return session.post(f"{DOCKER_API}{path}", timeout=2)


def list_compose_containers() -> list[dict[str, Any]]:
    resp = docker_get("/containers/json?all=1")
    resp.raise_for_status()
    return resp.json()


def find_container(service: str) -> dict[str, Any] | None:
    for container in list_compose_containers():
        labels = container.get("Labels", {})
        if (
            labels.get("com.docker.compose.project") == COMPOSE_PROJECT
            and labels.get("com.docker.compose.service") == service
        ):
            return container
    return None


def service_state(service: str) -> dict[str, Any]:
    match = find_container(service)
    if not match:
        return {
            "service": service,
            "project": COMPOSE_PROJECT,
            "found": False,
            "container_status": "not-created",
            "running": False,
            "health": "none",
        }

    container_id = match.get("Id")
    inspect_resp = docker_get(f"/containers/{container_id}/json")
    inspect_resp.raise_for_status()
    inspect_data = inspect_resp.json()

    state = inspect_data.get("State", {})
    health = state.get("Health", {})

    return {
        "service": service,
        "project": COMPOSE_PROJECT,
        "found": True,
        "container_id": container_id,
        "container_name": inspect_data.get("Name", "").lstrip("/"),
        "container_status": state.get("Status", "unknown"),
        "running": bool(state.get("Running", False)),
        "health": health.get("Status", "none"),
    }


@app.get("/containers")
def all_states():
    try:
        states = {service: service_state(service) for service in sorted(MANAGED_SERVICES)}
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    return jsonify(states)


@app.get("/containers/<service>")
def state_for_service(service: str):
    try:
        return jsonify(service_state(service))
    except Exception as exc:
        return jsonify({"service": service, "error": str(exc), "found": False}), 500


@app.post("/containers/<service>/<action>")
def service_action(service: str, action: str):
    if service not in MANAGED_SERVICES:
        return jsonify({"error": "service not allowed", "service": service}), 400

    if action not in {"start", "stop", "restart"}:
        return jsonify({"error": "invalid action", "action": action}), 400

    try:
        before = service_state(service)
        if not before.get("found"):
            return jsonify({"ok": False, "error": "container not found", "before": before}), 404

        container_id = before["container_id"]
        action_path = f"/containers/{container_id}/{action}"
        if action in {"stop", "restart"}:
            action_path = f"{action_path}?t=1"

        resp = docker_post(action_path)
        if resp.status_code not in {204, 304}:
            return (
                jsonify(
                    {
                        "ok": False,
                        "service": service,
                        "action": action,
                        "docker_status": resp.status_code,
                        "docker_body": resp.text,
                        "before": before,
                    }
                ),
                500,
            )

        after = service_state(service)
        return jsonify(
            {
                "ok": True,
                "service": service,
                "action": action,
                "docker_status": resp.status_code,
                "before": before,
                "after": after,
            }
        )
    except Exception as exc:
        return jsonify({"ok": False, "service": service, "action": action, "error": str(exc)}), 500


# Backward-compatible route used by the existing status UI path.
@app.get("/delayed-ui")
def delayed_ui_state():
    return state_for_service("delayed-ui")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
