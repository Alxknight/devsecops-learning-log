#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPORT_DIR="$PROJECT_ROOT/audit-reports"
IMAGE_NAME="webhook-validator:local"

mkdir -p "$REPORT_DIR"

echo "========================================"
echo "Local Security Audit - Webhook Validator"
echo "========================================"

cd "$PROJECT_ROOT"

echo ""
echo "[1/5] Running Python tests..."
python -m pytest -v

echo ""
echo "[2/5] Running Bandit SAST scan..."
if command -v bandit >/dev/null 2>&1; then
  bandit -r app \
    -f json \
    -o "$REPORT_DIR/bandit.json" || true
else
  echo "Bandit not installed. Install with: python -m pip install bandit"
fi

echo ""
echo "[3/5] Running pip-audit dependency scan..."
if command -v pip-audit >/dev/null 2>&1; then
  pip-audit -r requirements.txt \
    -f json \
    -o "$REPORT_DIR/pip-audit.json" || true
else
  echo "pip-audit not installed. Install with: python -m pip install pip-audit"
fi

echo ""
echo "[4/5] Building Docker image..."
docker build -t "$IMAGE_NAME" .

echo ""
echo "[5/5] Running Trivy image scan..."
if command -v trivy >/dev/null 2>&1; then
  trivy image \
    --format json \
    --output "$REPORT_DIR/trivy-image.json" \
    "$IMAGE_NAME" || true
else
  echo "Trivy CLI not installed locally."
  echo "Using Docker-based Trivy scan instead..."

  docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$REPORT_DIR:/reports" \
    aquasec/trivy image \
    --format json \
    --output /reports/trivy-image.json \
    "$IMAGE_NAME" || true
fi

echo ""
echo "========================================"
echo "Security audit completed."
echo "Reports saved in:"
echo "$REPORT_DIR"
echo "========================================"