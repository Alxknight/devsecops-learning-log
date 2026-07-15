# Kubernetes Manifests - Webhook Validator

This folder contains Kubernetes manifests for the Webhook Validator SecOps project.

## Files

| File | Purpose |
|---|---|
| `namespace.yaml` | Creates the `webhook-validator` namespace |
| `secret.example.yaml` | Example secret manifest, not for production secrets |
| `deployment.yaml` | Runs the FastAPI webhook validator container |
| `service.yaml` | Exposes the app inside the cluster using ClusterIP |

## Security Notes

The application expects `WEBHOOK_SECRET` to come from a Kubernetes Secret.

Do not commit real production secrets to Git.

Create the local development secret with:

```bash
kubectl create secret generic webhook-validator-secret \
  --namespace webhook-validator \
  --from-literal=WEBHOOK_SECRET=dev-secret
