# Webhook Validator DevSecOps Project

Microservicio simple en Python para validar webhooks mediante firma HMAC.

El valor principal del proyecto no es la complejidad de la API, sino el flujo DevSecOps completo:

- API en Python con FastAPI
- Contenedor Docker optimizado
- Pruebas automatizadas
- CI/CD con GitHub Actions
- Escaneo de seguridad con Trivy
- Despliegue en Kubernetes usando K3s o Minikube dentro de AWS EC2
- Control de costos con AWS Budgets

## Estado actual

- Día 1: AWS Budget configurado
- Día 2: API local y Docker