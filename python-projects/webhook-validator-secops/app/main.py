import hashlib
import hmac
import logging
import os
import uuid

from fastapi import FastAPI, Header, HTTPException, Request, Response

SERVICE_NAME = "webhook-validator"
SAFE_LOCAL_ENVIRONMENTS = {"development", "test", "local"}

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(SERVICE_NAME)

app = FastAPI(title="Webhook Validator API")


def get_app_environment() -> str:
    """
    Returns the current application environment.
    """
    return os.getenv("APP_ENV", "development").lower()


def get_webhook_secret() -> str:
    """
    Returns the webhook secret.

    In development/test/local environments, a default secret is allowed
    to keep local testing simple.

    In production-like environments, WEBHOOK_SECRET must be explicitly set.
    """
    secret = os.getenv("WEBHOOK_SECRET")
    environment = get_app_environment()

    if secret:
        return secret

    if environment in SAFE_LOCAL_ENVIRONMENTS:
        return "dev-secret"

    raise RuntimeError(
        "WEBHOOK_SECRET environment variable is required outside development/test/local"
    )


def is_configuration_ready() -> bool:
    """
    Readiness rule:
    - Local-like environments are ready even with the development default.
    - Production-like environments require WEBHOOK_SECRET.
    """
    environment = get_app_environment()
    secret = os.getenv("WEBHOOK_SECRET")

    if environment in SAFE_LOCAL_ENVIRONMENTS:
        return True

    return bool(secret)


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


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """
    Adds a request ID to every response.

    If the client sends X-Request-ID, we reuse it.
    Otherwise, we generate a new one.
    """
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response


@app.get("/health")
def health_check():
    """
    Liveness endpoint.

    This only confirms that the application process is alive.
    """
    return {
        "status": "ok",
        "service": SERVICE_NAME,
    }


@app.get("/ready")
def readiness_check(response: Response):
    """
    Readiness endpoint.

    This confirms whether the app is correctly configured to receive traffic.
    """
    if not is_configuration_ready():
        response.status_code = 503
        return {
            "status": "not_ready",
            "service": SERVICE_NAME,
            "reason": "WEBHOOK_SECRET is required outside development/test/local",
        }

    return {
        "status": "ready",
        "service": SERVICE_NAME,
        "environment": get_app_environment(),
    }


@app.post("/webhook")
async def validate_webhook(
    request: Request,
    x_webhook_signature: str = Header(default=""),
):
    payload = await request.body()
    request_id = getattr(request.state, "request_id", "unknown")

    if not x_webhook_signature:
        logger.warning(
            "Webhook rejected: missing signature | request_id=%s | payload_size=%s",
            request_id,
            len(payload),
        )
        raise HTTPException(
            status_code=401,
            detail="Missing webhook signature",
        )

    try:
        webhook_secret = get_webhook_secret()
    except RuntimeError:
        logger.error(
            "Webhook secret is not configured | request_id=%s | environment=%s",
            request_id,
            get_app_environment(),
        )
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
        logger.warning(
            "Webhook rejected: invalid signature | request_id=%s | payload_size=%s",
            request_id,
            len(payload),
        )
        raise HTTPException(
            status_code=403,
            detail="Invalid webhook signature",
        )

    logger.info(
        "Webhook accepted | request_id=%s | payload_size=%s",
        request_id,
        len(payload),
    )

    return {
        "message": "Webhook accepted",
        "payload_size": len(payload),
    }