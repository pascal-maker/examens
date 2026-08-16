import signal
import socket
import subprocess
import sys
import time
from urllib.request import Request, urlopen

from app_config import ENV_EXAMPLE_PATH, ENV_PATH, ROOT_DIR, get_settings

BACKEND_DIR = ROOT_DIR / "backend"
PRIMARY_COMPOSE_PATH = ROOT_DIR / "compose.yaml"
FALLBACK_COMPOSE_PATH = BACKEND_DIR / "compose.yaml"


def _start_postgres(settings):
    if not settings.launch_postgres_docker:
        print("Skipping Docker PostgreSQL because LAUNCH_POSTGRES_DOCKER is false.")
        return

    compose_path = PRIMARY_COMPOSE_PATH if PRIMARY_COMPOSE_PATH.exists() else FALLBACK_COMPOSE_PATH
    env_file = ENV_PATH if ENV_PATH.exists() else ENV_EXAMPLE_PATH
    command = [
        "docker",
        "compose",
        "--env-file",
        str(env_file),
        "-f",
        str(compose_path),
        "up",
        "-d",
        "db",
    ]
    print(f"Starting PostgreSQL with Docker Compose from {compose_path.name}...")
    subprocess.run(command, cwd=ROOT_DIR, check=True)


def _wait_for_tcp(host, port, service_name, timeout_seconds=60):
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"{service_name} is reachable on {host}:{port}.")
                return
        except OSError:
            time.sleep(1)
    raise RuntimeError(f"{service_name} did not become reachable on {host}:{port} within {timeout_seconds} seconds.")


def _wait_for_http(url, timeout_seconds=60):
    deadline = time.time() + timeout_seconds
    request = Request(url, method="GET")
    while time.time() < deadline:
        try:
            with urlopen(request, timeout=3) as response:  # noqa: S310
                if 200 <= response.status < 500:
                    print(f"Backend healthcheck is reachable at {url}.")
                    return
        except Exception:
            time.sleep(1)
    raise RuntimeError(f"Backend did not become healthy at {url} within {timeout_seconds} seconds.")


def _start_processes(settings):
    backend_command = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.main:app",
        "--host",
        settings.backend_host,
        "--port",
        str(settings.backend_port),
    ]
    frontend_command = [
        sys.executable,
        "-m",
        "frontend.main",
    ]

    print(f"Starting backend on http://{settings.backend_host}:{settings.backend_port}")
    backend = subprocess.Popen(backend_command, cwd=ROOT_DIR)
    _wait_for_http(f"http://{settings.backend_host}:{settings.backend_port}/health")

    print(f"Starting frontend on http://{settings.frontend_host}:{settings.frontend_port}")
    frontend = subprocess.Popen(frontend_command, cwd=ROOT_DIR)
    return [backend, frontend]


def _stop_processes(processes):
    for process in processes:
        if process.poll() is None:
            process.send_signal(signal.SIGTERM)
    for process in processes:
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def main():
    settings = get_settings()
    if not ENV_PATH.exists():
        print(f"Using {ENV_EXAMPLE_PATH.name} because .env is missing.")
    _start_postgres(settings)
    _wait_for_tcp(settings.postgres_host, settings.postgres_port, "PostgreSQL")
    processes = _start_processes(settings)

    print("Application is running. Press Ctrl+C to stop backend and frontend.")
    try:
        while True:
            for process in processes:
                if process.poll() is not None:
                    raise RuntimeError(f"A launched process exited with code {process.returncode}.")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping application...")
    finally:
        _stop_processes(processes)


if __name__ == "__main__":
    main()
