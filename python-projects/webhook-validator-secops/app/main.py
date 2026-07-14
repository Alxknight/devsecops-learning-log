import hashlib
import hmac
import logging
import os

from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(title="Webhook Validator API")

logger = logging.getLogger("webhook-validator")


def get_webhook_secret() -> str:
    """
    Returns the webhook secret.

    In development/test/local environments, a default secret is allowed
    to keep local testing simple.

    In production-like environments, WEBHOOK_SECRET must be explicitly set.
    """
    secret = os.getenv("WEBHOOK_SECRET")
    environment = os.getenv("APP_ENV", "development").lower()

    if secret:
        return secret

    if environment in {"development", "test", "local"}:
        return "dev-secret"

    raise RuntimeError(
        "WEBHOOK_SECRET environment variable is required outside development/test/local"
    )


def generate_signature(payload: bytes, secret: str) -> str:
    """
    Generates an HMAC SHA-256 signature for the incoming payload.
    """
    digest = hmac.new(
        key=secret.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()

    return f"sha256={digest}"


def verify_signature(payload: bytes, received_signature: str, secret: str) -> bool:
    """
    Safely compares the expected signature with the received signature.
    """
    expected_signature = generate_signature(payload, secret)
    return hmac.compare_digest(expected_signature, received_signature)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "webhook-validator",
    }


@app.post("/webhook")
async def validate_webhook(
    request: Request,
    x_webhook_signature: str = Header(default=""),
):
    payload = await request.body()

    if not x_webhook_signature:
        logger.warning("Webhook rejected: missing signature")
        raise HTTPException(
            status_code=401,
            detail="Missing webhook signature",
        )

    try:
        webhook_secret = get_webhook_secret()
    except RuntimeError:
        logger.error("Webhook secret is not configured for this environment")
        raise HTTPException(
            status_code=500,
            detail="Webhook secret is not configured",
        )

    is_valid = verify_signature(
        payload=payload,
        received_signature=x_webhook_signature,
        secret=webhook_secret,
    )

    if not is_valid:
        logger.warning("Webhook rejected: invalid signature")
        raise HTTPException(
            status_code=403,
            detail="Invalid webhook signature",
        )

    logger.info("Webhook accepted")

    return {
        "message": "Webhook accepted",
        "payload_size": len(payload),
    }