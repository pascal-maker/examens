import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
ENV_PATH = ROOT_DIR / ".env"
ENV_EXAMPLE_PATH = ROOT_DIR / ".env.example"


def _load_env_file(path):
    values = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _parse_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    student_name: str
    backend_host: str
    backend_port: int
    frontend_host: str
    frontend_port: int
    garage_api_base_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    adminer_port: int
    launch_postgres_docker: bool
    env_file_used: str

    @property
    def sqlalchemy_database_url(self) -> str:
        return (
            "postgresql+psycopg://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


def load_settings(force_reload: bool = False) -> Settings:
    if force_reload:
        get_settings.cache_clear()
    return get_settings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    file_path = ENV_PATH if ENV_PATH.exists() else ENV_EXAMPLE_PATH
    env = os.environ.copy()
    env.update(_load_env_file(file_path))

    student_name = env.get("STUDENT_NAME", "Your Name")
    backend_host = env.get("BACKEND_HOST", "127.0.0.1")
    backend_port = int(env.get("BACKEND_PORT", "8000"))
    frontend_host = env.get("FRONTEND_HOST", "127.0.0.1")
    frontend_port = int(env.get("FRONTEND_PORT", "7860"))
    garage_api_base_url = env.get(
        "GARAGE_API_BASE_URL",
        f"http://{backend_host}:{backend_port}",
    )

    return Settings(
        student_name=student_name,
        backend_host=backend_host,
        backend_port=backend_port,
        frontend_host=frontend_host,
        frontend_port=frontend_port,
        garage_api_base_url=garage_api_base_url,
        postgres_user=env.get("POSTGRES_USER", "postgres"),
        postgres_password=env.get("POSTGRES_PASSWORD", "postgres"),
        postgres_db=env.get("POSTGRES_DB", "garage_management"),
        postgres_host=env.get("POSTGRES_HOST", "127.0.0.1"),
        postgres_port=int(env.get("POSTGRES_PORT", "5432")),
        adminer_port=int(env.get("ADMINER_PORT", "8080")),
        launch_postgres_docker=_parse_bool(env.get("LAUNCH_POSTGRES_DOCKER"), True),
        env_file_used=str(file_path),
    )
