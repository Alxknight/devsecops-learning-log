# Kubernetes Manifests - Webhook Validator

This folder contains Kubernetes manifests for the **Webhook Validator SecOps** project.

The purpose of this folder is to prepare the FastAPI webhook validator to run inside a Kubernetes environment using a local Minikube cluster.

This is part of the project’s DevSecOps/SRE learning path:

```text
Python API
   ↓
Docker image
   ↓
Kubernetes manifests
   ↓
Local Minikube deployment
   ↓
Health/readiness validation
   ↓
Future AWS/K3s deployment
```

---

## Files

| File | Purpose |
|---|---|
| `namespace.yaml` | Creates the `webhook-validator` namespace |
| `secret.example.yaml` | Provides an example Kubernetes Secret manifest |
| `deployment.yaml` | Runs the FastAPI webhook validator container |
| `service.yaml` | Exposes the application inside the cluster using ClusterIP |

The project also includes helper scripts outside this folder:

| Script | Purpose |
|---|---|
| `scripts/k8s-local-deploy.sh` | Builds the image, loads it into Minikube, applies manifests, creates the local Secret, and waits for rollout |
| `scripts/k8s-local-cleanup.sh` | Deletes the local Kubernetes namespace and all related resources |

---

## Kubernetes Concepts Used

This project introduces the following Kubernetes objects:

| Concept | Meaning in This Project |
|---|---|
| Namespace | Logical space where all project resources live |
| Secret | Stores `WEBHOOK_SECRET` for the application |
| Deployment | Defines how the API container should run |
| Pod | The actual running instance of the container |
| Service | Stable internal network address for the app |
| Readiness Probe | Checks if the app is ready to receive traffic |
| Liveness Probe | Checks if the app is still alive |
| Resource Requests/Limits | Defines expected and maximum CPU/memory usage |
| Security Context | Applies basic runtime security controls |

---

## Local Requirements

Before deploying locally, the following tools must be installed and working:

```bash
docker --version
kubectl version --client
minikube version
```

Minikube should be able to run using the Docker driver:

```bash
minikube start --driver=docker --cpus=2 --memory=3072 --disk-size=10g
```

Verify the local cluster:

```bash
minikube status
kubectl get nodes
```

Expected result:

```text
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   ...
```

---

## Security Notes

The application requires a secret value called:

```text
WEBHOOK_SECRET
```

This secret is used by the FastAPI application to validate incoming webhook signatures using HMAC SHA-256.

Do not commit real production secrets to Git.

The file:

```text
secret.example.yaml
```

is only an example.

For local development, create the real Kubernetes Secret with:

```bash
kubectl create secret generic webhook-validator-secret \
  --namespace webhook-validator \
  --from-literal=WEBHOOK_SECRET=dev-secret
```

Or use the automated deployment script, which creates/updates the local Secret automatically.

---

## One-Command Local Deployment

This project includes a helper script to automate the local Minikube deployment flow.

From the project folder:

```bash
./scripts/k8s-local-deploy.sh
```

The script performs the following actions:

1. Checks that Docker, kubectl, and Minikube are available.
2. Starts Minikube if it is not already running.
3. Builds the local Docker image.
4. Loads the image into Minikube.
5. Applies the Kubernetes namespace.
6. Creates or updates the local development Secret.
7. Applies the Deployment and Service manifests.
8. Restarts the Deployment.
9. Waits for the rollout to complete.
10. Prints the current Kubernetes resources.

After deployment, use port-forwarding to test the service:

```bash
kubectl port-forward svc/webhook-validator 8080:80 -n webhook-validator
```

Then test the health endpoints from another terminal:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/ready
```

---

## Manual Local Deployment Flow

The automated script is recommended, but the deployment can also be performed manually.

### 1. Build the Docker image

From the project folder:

```bash
docker build -t webhook-validator:local .
```

### 2. Load the image into Minikube

```bash
minikube image load webhook-validator:local
```

Verify that Minikube has the image:

```bash
minikube image ls | grep webhook-validator
```

### 3. Apply the namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### 4. Create the local Secret

```bash
kubectl create secret generic webhook-validator-secret \
  --namespace webhook-validator \
  --from-literal=WEBHOOK_SECRET=dev-secret \
  --dry-run=client -o yaml | kubectl apply -f -
```

### 5. Apply the Deployment and Service

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 6. Wait for the rollout

```bash
kubectl rollout status deployment/webhook-validator -n webhook-validator --timeout=120s
```

Expected result:

```text
deployment "webhook-validator" successfully rolled out
```

### 7. Check Kubernetes resources

```bash
kubectl get all -n webhook-validator
```

Expected resources:

```text
pod/webhook-validator-xxxxx
service/webhook-validator
deployment.apps/webhook-validator
replicaset.apps/webhook-validator-xxxxx
```

---

## Testing the Application Through Kubernetes

To access the application locally, use port-forwarding:

```bash
kubectl port-forward svc/webhook-validator 8080:80 -n webhook-validator
```

Keep that terminal open.

In another terminal, test:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/ready
```

Expected `/health` response:

```json
{
  "status": "ok",
  "service": "webhook-validator"
}
```

Expected `/ready` response:

```json
{
  "status": "ready",
  "service": "webhook-validator",
  "environment": "production"
}
```

---

## Testing a Valid Webhook Signature

With the port-forward still running, test a valid webhook request:

```bash
PAYLOAD='{"event":"payment.created","id":"evt_123"}'
SECRET='dev-secret'

SIGNATURE="sha256=$(printf '%s' "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')"

curl -i -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: $SIGNATURE" \
  -d "$PAYLOAD"
```

Expected result:

```text
HTTP/1.1 200 OK
```

Expected response body:

```json
{
  "message": "Webhook accepted",
  "payload_size": 42
}
```

---

## Testing an Invalid Webhook Signature

```bash
curl -i -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=wrong" \
  -d "$PAYLOAD"
```

Expected result:

```text
HTTP/1.1 403 Forbidden
```

Expected response body:

```json
{
  "detail": "Invalid webhook signature"
}
```

---

## Local Cleanup

To remove the local Kubernetes resources:

```bash
./scripts/k8s-local-cleanup.sh
```

This deletes the `webhook-validator` namespace and all resources inside it.

Manual cleanup:

```bash
kubectl delete namespace webhook-validator --ignore-not-found=true
```

To stop Minikube without deleting the cluster:

```bash
minikube stop
```

To delete the entire local Minikube cluster:

```bash
minikube delete
```

---

## Troubleshooting

### Pod is stuck in `ImagePullBackOff`

This means Kubernetes cannot find the image.

Fix:

```bash
docker build -t webhook-validator:local .
minikube image load webhook-validator:local
kubectl rollout restart deployment/webhook-validator -n webhook-validator
```

Then check:

```bash
kubectl get pods -n webhook-validator
```

---

### Pod is stuck in `CreateContainerConfigError`

Check the Pod events:

```bash
kubectl describe pod -n webhook-validator
```

If the error says:

```text
secret "webhook-validator-secret" not found
```

Create the Secret:

```bash
kubectl create secret generic webhook-validator-secret \
  --namespace webhook-validator \
  --from-literal=WEBHOOK_SECRET=dev-secret \
  --dry-run=client -o yaml | kubectl apply -f -
```

Then restart the Deployment:

```bash
kubectl rollout restart deployment/webhook-validator -n webhook-validator
```

---

### Error: `container has runAsNonRoot and image has non-numeric user`

This means Kubernetes cannot verify that the container user is non-root.

The Dockerfile should use a numeric UID/GID:

```dockerfile
RUN addgroup -S -g 10001 appgroup \
    && adduser -S -D -H -u 10001 -G appgroup appuser

USER 10001:10001
```

This keeps the security control enabled instead of disabling `runAsNonRoot`.

---

### `/ready` returns an error

The readiness endpoint depends on correct runtime configuration.

Check that the Secret exists:

```bash
kubectl get secrets -n webhook-validator
```

Restart the Deployment after creating or updating the Secret:

```bash
kubectl rollout restart deployment/webhook-validator -n webhook-validator
```

---

### View logs

```bash
kubectl logs deployment/webhook-validator -n webhook-validator
```

---

### Describe the Deployment

```bash
kubectl describe deployment webhook-validator -n webhook-validator
```

---

### Describe a specific Pod

First get the Pod name:

```bash
kubectl get pods -n webhook-validator
```

Then describe it:

```bash
kubectl describe pod <pod-name> -n webhook-validator
```

---

## DevSecOps/SRE Value

This Kubernetes improvement demonstrates:

- Basic Kubernetes deployment workflow.
- Local Kubernetes testing with Minikube.
- Use of Secrets instead of hardcoded sensitive values.
- Readiness and liveness probes.
- Non-root container execution.
- Numeric UID/GID compatibility with Kubernetes.
- Basic container security context.
- Resource requests and limits.
- Cluster-internal service exposure using ClusterIP.
- Reproducible local deployment through Bash automation.
- Troubleshooting using `kubectl describe`, `kubectl logs`, and rollout status.

---

## What This Project Now Demonstrates

Before this improvement, the application could run as a Docker container.

After this improvement, the application can run inside Kubernetes locally.

Current flow:

```text
Source code
   ↓
Dockerfile
   ↓
Docker image
   ↓
Minikube image load
   ↓
Kubernetes Namespace
   ↓
Kubernetes Secret
   ↓
Kubernetes Deployment
   ↓
Pod
   ↓
Service
   ↓
Port-forward
   ↓
HTTP validation
```

This is a realistic first step toward cloud deployment with K3s or Minikube on AWS EC2.

---

## Interview Explanation

A clear way to explain this improvement:

> I added Kubernetes manifests to deploy the Webhook Validator API into a local Minikube cluster. The Deployment uses a Kubernetes Secret for `WEBHOOK_SECRET`, liveness and readiness probes for `/health` and `/ready`, resource requests and limits, and a basic security context. During testing, Kubernetes rejected the image because it used a named non-root user. Instead of disabling the security control, I updated the Dockerfile to use a numeric UID/GID so Kubernetes could verify that the container runs as non-root. I also automated the local deployment flow with Bash scripts to make the Kubernetes test environment reproducible.

---

## Next Improvements

Possible next steps:

1. Add Kubernetes manifest validation to CI.
2. Add `kubectl --dry-run=client` checks in GitHub Actions.
3. Add kube-linter or kube-score.
4. Add Kubernetes security scanning.
5. Push the Docker image to GHCR.
6. Deploy to K3s or Minikube on AWS EC2.
7. Add Ingress for controlled external access.
8. Add basic monitoring and logging.
9. Add a deployment architecture diagram.
10. Document screenshots or command evidence for portfolio use.