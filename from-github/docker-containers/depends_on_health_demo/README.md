# depends_on + healthcheck demo

This demo shows two frontend behaviors against an API that is unhealthy for 20 seconds.

## Services

- `api`: Flask API with a 20-second warmup. `/health` returns `503` during warmup and `200` when healthy.
- `status-ui`: Always-on Nginx UI that polls the API continuously and shows:
  - Orange dot while API is not healthy.
  - Green dot when API becomes healthy.
- `state-api`: Internal service that reads and controls Docker Engine containers via `/var/run/docker.sock`.
  - `GET /containers/{service}` for runtime state.
  - `POST /containers/{service}/{action}` where action is `start|stop|restart`.
- `delayed-ui`: Separate frontend using `depends_on` with `condition: service_healthy`, so it starts only after API healthcheck succeeds.

## Run

```bash
cd depends_on_health_demo
docker compose up --build
```

## Open in browser

- Always-on polling UI: http://localhost:8090
- Delayed frontend: http://localhost:8091
- API health endpoint: http://localhost:8092/health

## Expected behavior

1. `status-ui` is available immediately and starts with an orange status dot.
2. API takes about 20 seconds to become healthy.
3. `delayed-ui` is not available until API healthcheck passes, then it starts.
4. `status-ui` dot turns green once the API is healthy.
5. `status-ui` also shows Docker runtime state for `api` and `delayed-ui`.
6. The control endpoints still exist in `state-api`, but controls are hidden in the status UI.

## Security note

`state-api` mounts the Docker socket with write access for demo controls. Treat Docker socket access as privileged in real environments.
