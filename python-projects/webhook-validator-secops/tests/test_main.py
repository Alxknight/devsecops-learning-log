import pytest
from fastapi.testclient import TestClient

from app.main import app, generate_signature

client = TestClient(app)


@pytest.fixture(autouse=True)
def default_test_environment(monkeypatch):
    """
    Each test starts in a safe local-like environment.
    """
    monkeypatch.setenv("APP_ENV", "development")
    monkeypatch.delenv("WEBHOOK_SECRET", raising=False)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "webhook-validator"


def test_ready_check_in_development():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["environment"] == "development"


def test_ready_check_fails_in_production_without_secret(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("WEBHOOK_SECRET", raising=False)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"


def test_request_id_header_is_returned():
    response = client.get(
        "/health",
        headers={"X-Request-ID": "test-request-123"},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request-123"


def test_webhook_accepts_valid_signature():
    payload = b'{"event":"payment.created","id":"evt_123"}'
    signature = generate_signature(payload, "dev-secret")

    response = client.post(
        "/webhook",
        content=payload,
        headers={"X-Webhook-Signature": signature},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Webhook accepted"


def test_webhook_rejects_missing_signature():
    payload = b'{"event":"payment.created","id":"evt_123"}'

    response = client.post(
        "/webhook",
        content=payload,
    )

    assert response.status_code == 401


def test_webhook_rejects_invalid_signature():
    payload = b'{"event":"payment.created","id":"evt_123"}'

    response = client.post(
        "/webhook",
        content=payload,
        headers={"X-Webhook-Signature": "sha256=invalid"},
    )

    assert response.status_code == 403


def test_webhook_requires_secret_in_production(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("WEBHOOK_SECRET", raising=False)

    payload = b'{"event":"payment.created","id":"evt_123"}'

    response = client.post(
        "/webhook",
        content=payload,
        headers={"X-Webhook-Signature": "sha256=anything"},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "Webhook secret is not configured"


def test_webhook_accepts_custom_secret_from_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("WEBHOOK_SECRET", "super-secret-for-test")

    payload = b'{"event":"payment.created","id":"evt_123"}'
    signature = generate_signature(payload, "super-secret-for-test")

    response = client.post(
        "/webhook",
        content=payload,
        headers={"X-Webhook-Signature": signature},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Webhook accepted"