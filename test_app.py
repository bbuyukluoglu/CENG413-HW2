import importlib
import os

import pytest


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("APP_GREETING", "Hello")
    import app as app_module

    importlib.reload(app_module)
    return app_module.app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_greet_default(client):
    assert client.get("/greet").get_json() == {"message": "Hello, world!"}


def test_greet_name(client):
    assert client.get("/greet?name=Ada").get_json() == {"message": "Hello, Ada!"}


@pytest.mark.skipif("DB_PASSWORD" not in os.environ, reason="needs PostgreSQL")
def test_visit_counts_up(client):
    first = client.get("/visit").get_json()["visits"]
    assert client.get("/visit").get_json() == {"visits": first + 1}
