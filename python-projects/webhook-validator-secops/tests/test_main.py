from fastapi.testclient import TestClient

from app.main import app, generate_signature

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


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