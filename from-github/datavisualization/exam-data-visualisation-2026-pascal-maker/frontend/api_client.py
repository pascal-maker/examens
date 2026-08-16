from dataclasses import dataclass
from typing import Any

import requests

from app_config import get_settings


settings = get_settings()


class ApiClientError(RuntimeError):
    pass


@dataclass
class GarageApiClient:
    base_url: str = settings.garage_api_base_url
    timeout_seconds: int = 30

    def _request(self, method, path, payload=None, params=None):
        url = f"{self.base_url.rstrip('/')}{path}"
        try:
            response = requests.request(
                method=method,
                url=url,
                json=payload,
                params=params,
                timeout=self.timeout_seconds,
            )
        except requests.RequestException as exc:
            raise ApiClientError(f"Could not connect to backend API at {self.base_url}. {exc}") from exc

        if response.status_code >= 400:
            detail = self._extract_error_detail(response)
            raise ApiClientError(detail)

        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    @staticmethod
    def _extract_error_detail(response):
        try:
            payload = response.json()
        except ValueError:
            return f"Request failed with status {response.status_code}: {response.text}"

        detail = payload.get("detail")
        if isinstance(detail, list):
            messages = []
            for item in detail:
                loc = " -> ".join(str(part) for part in item.get("loc", []))
                msg = item.get("msg", "Validation error")
                messages.append(f"{loc}: {msg}" if loc else msg)
            return "; ".join(messages)
        if isinstance(detail, dict):
            return str(detail)
        if detail:
            return str(detail)
        return f"Request failed with status {response.status_code}."

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, payload: dict[str, Any] | None = None) -> Any:
        return self._request("POST", path, payload=payload)

    def patch(self, path: str, payload: dict[str, Any] | None = None) -> Any:
        return self._request("PATCH", path, payload=payload)

    def delete(self, path: str) -> None:
        self._request("DELETE", path)


client = GarageApiClient()
