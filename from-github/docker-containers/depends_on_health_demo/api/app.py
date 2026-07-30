import os
import time

from flask import Flask, jsonify

app = Flask(__name__)
STARTED_AT = time.time()
WARMUP_SECONDS = int(os.getenv("WARMUP_SECONDS", "20"))


def is_healthy() -> bool:
    return (time.time() - STARTED_AT) >= WARMUP_SECONDS


@app.get("/health")
def health():
    elapsed = int(time.time() - STARTED_AT)
    remaining = max(WARMUP_SECONDS - elapsed, 0)

    if is_healthy():
        return jsonify({"status": "healthy", "uptime_seconds": elapsed}), 200

    return jsonify({"status": "starting", "remaining_seconds": remaining}), 503


@app.get("/message")
def message():
    elapsed = int(time.time() - STARTED_AT)
    return jsonify(
        {
            "message": "Hello from API",
            "healthy": is_healthy(),
            "uptime_seconds": elapsed,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
