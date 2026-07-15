#!/usr/bin/env bash

set -euo pipefail

NAMESPACE="webhook-validator"

echo "==> Cleaning local Kubernetes resources"
echo "Namespace: ${NAMESPACE}"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "ERROR: kubectl is not installed or not available in PATH."
  exit 1
fi

kubectl delete namespace "${NAMESPACE}" --ignore-not-found=true

echo "Cleanup completed."
