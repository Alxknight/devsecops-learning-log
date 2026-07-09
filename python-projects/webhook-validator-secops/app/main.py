import hashlib
import hmac
import os

from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(title="Webhook Validator API")

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev-secret")


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
        raise HTTPException(
            status_code=401,
            detail="Missing webhook signature",
        )

    is_valid = verify_signature(
        payload=payload,
        received_signature=x_webhook_signature,
        secret=WEBHOOK_SECRET,
    )

    if not is_valid:
        raise HTTPException(
            status_code=403,
            detail="Invalid webhook signature",
        )

    return {
        "message": "Webhook accepted",
        "payload_size": len(payload),
    }