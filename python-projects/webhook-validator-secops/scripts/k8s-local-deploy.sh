#!/usr/bin/env bash

set -euo pipefail

APP_NAME="webhook-validator"
NAMESPACE="webhook-validator"
IMAGE_NAME="${IMAGE_NAME:-webhook-validator:local}"
WEBHOOK_SECRET_VALUE="${WEBHOOK_SECRET:-dev-secret}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Webhook Validator local Kubernetes deployment"
echo "Project root: ${PROJECT_ROOT}"
echo "Image: ${IMAGE_NAME}"
echo "Namespace: ${NAMESPACE}"

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

echo "==> Checking required tools"

if ! command_exists docker; then
  echo "ERROR: docker is not installed or not available in PATH."
  exit 1
fi

if ! command_exists kubectl; then
  echo "ERROR: kubectl is not installed or not available in PATH."
  exit 1
fi

if ! command_exists minikube; then
  echo "ERROR: minikube is not installed or not available in PATH."
  exit 1
fi

echo "==> Checking Minikube status"

if ! minikube status 2>/dev/null | grep -q "host: Running"; then
  echo "Minikube is not running. Starting Minikube..."
  minikube start --driver=docker --cpus=2 --memory=3072 --disk-size=10g
else
  echo "Minikube is already running."
fi

echo "==> Building Docker image"

docker build -t "${IMAGE_NAME}" "${PROJECT_ROOT}"

echo "==> Loading image into Minikube"

minikube image load "${IMAGE_NAME}"

echo "==> Applying Kubernetes namespace"

kubectl apply -f "${PROJECT_ROOT}/k8s/namespace.yaml"

echo "==> Creating or updating Kubernetes secret"

kubectl create secret generic webhook-validator-secret \
  --namespace "${NAMESPACE}" \
  --from-literal=WEBHOOK_SECRET="${WEBHOOK_SECRET_VALUE}" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "==> Applying Kubernetes manifests"

kubectl apply -f "${PROJECT_ROOT}/k8s/deployment.yaml"
kubectl apply -f "${PROJECT_ROOT}/k8s/service.yaml"

echo "==> Restarting deployment to use the latest local image"

kubectl rollout restart deployment/"${APP_NAME}" -n "${NAMESPACE}"

echo "==> Waiting for rollout to complete"

kubectl rollout status deployment/"${APP_NAME}" -n "${NAMESPACE}" --timeout=120s

echo "==> Current Kubernetes resources"

kubectl get all -n "${NAMESPACE}"

echo
echo "Deployment completed successfully."
echo
echo "To test locally, run:"
echo
echo "  kubectl port-forward svc/${APP_NAME} 8080:80 -n ${NAMESPACE}"
echo
echo "Then, in another terminal:"
echo
echo "  curl http://localhost:8080/health"
echo "  curl http://localhost:8080/ready"
echo