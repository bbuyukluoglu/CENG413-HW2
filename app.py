"""Tiny demo web service for CENG413 HW-2 (two services with Docker Compose).

Endpoints
  GET /health        -> {"status": "ok"}            (stateless)
  GET /greet?name=X  -> {"message": "Hello, X!"}    (stateless)
  GET /info          -> course info from env        (stateless)
  GET /visit         -> {"visits": N}               (state lives in PostgreSQL,
                        NOT on the app container's disk)

Configuration comes from environment variables (12-factor style):
  APP_GREETING  default "Hello"
  COURSE_NAME   default "CENG413"
  DB_HOST       default "db"   (the Compose service name, not an IP / localhost)
  DB_PORT       default "5432"
  DB_NAME, DB_USER, DB_PASSWORD   (required, come from .env via compose.yaml)
"""
import os

import psycopg
from flask import Flask, jsonify, request

app = Flask(__name__)

GREETING = os.environ.get("APP_GREETING", "Hello")


def _connect():
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=os.environ.get("DB_PORT", "5432"),
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
    )


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/greet")
def greet():
    name = request.args.get("name", "world")
    return jsonify(message=f"{GREETING}, {name}!")


@app.get("/visit")
def visit():
    # One atomic upsert: safe even when several app copies run at once.
    with _connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS counters ("
            " name TEXT PRIMARY KEY, value INTEGER NOT NULL)"
        )
        row = conn.execute(
            "INSERT INTO counters (name, value) VALUES ('visits', 1) "
            "ON CONFLICT (name) DO UPDATE SET value = counters.value + 1 "
            "RETURNING value"
        ).fetchone()
    return jsonify(visits=row[0])


@app.get("/info")
def info():
    course = os.environ.get("COURSE_NAME", "CENG413")
    return jsonify(message="This is the new endpoint!", course=course)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
