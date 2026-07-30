# .dockerignore demo

This demo shows what gets copied into an image with and without `.dockerignore`.

## Run

```bash
cd dockerignore_demo
docker compose up --build
```

## What to look for

- `without-ignore` includes `/app/secret.env` and `/app/tmp/debug.log`.
- `with-ignore` only includes `/app/.dockerignore`, `/app/Dockerfile`, and `/app/src/app.txt`.

## Why this matters

- Keep secrets out of images.
- Shrink build contexts and improve build speed.
- Avoid unnecessary cache invalidation from temporary files.
