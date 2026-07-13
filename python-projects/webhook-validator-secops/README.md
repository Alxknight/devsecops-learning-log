# Webhook Validator DevSecOps Project

Microservicio sencillo en Python para validar webhooks mediante firma **HMAC SHA-256**.

El valor principal de este proyecto no está en la complejidad del código Python, sino en construir un flujo **End-to-End DevSecOps/SRE** realista:

- API en Python con FastAPI.
- Pruebas automatizadas con Pytest.
- Imagen Docker optimizada.
- CI/CD con GitHub Actions.
- Build automático de imagen Docker en CI.
- Smoke test automático del contenedor.
- Escaneo de vulnerabilidades con Trivy.
- Despliegue en Kubernetes usando K3s o Minikube dentro de una instancia EC2 en AWS.
- Control de costos desde el inicio con AWS Budgets.

---

## Objetivo profesional del proyecto

Este proyecto forma parte de mi transición de **InfoSec GRC** hacia roles técnicos de **DevSecOps / Site Reliability Engineering (SRE)**.

El objetivo es demostrar que entiendo cómo una aplicación pasa por un ciclo moderno de entrega segura:

```text
Código local
   ↓
Pruebas automatizadas
   ↓
Contenedor Docker
   ↓
Pipeline CI/CD
   ↓
Build y smoke test automático
   ↓
Escaneo de seguridad
   ↓
Infraestructura cloud
   ↓
Kubernetes
   ↓
Despliegue controlado
```

---

## Problema que resuelve

Muchas plataformas externas envían eventos automáticos a una API mediante **webhooks**.

Ejemplos:

- Un pago creado.
- Una orden actualizada.
- Un usuario registrado.
- Un evento de seguridad recibido.

El problema es que una API pública no debe confiar en cualquier petición entrante. Este microservicio valida que el webhook venga firmado correctamente usando un secreto compartido.

Flujo lógico:

```text
Cliente externo envía payload + firma
   ↓
La API recibe el payload
   ↓
La API recalcula la firma con el secreto interno
   ↓
Compara ambas firmas de forma segura
   ↓
Acepta o rechaza el webhook
```

---

## Estado actual del proyecto

| Día | Estado | Descripción |
|---|---:|---|
| Día 1 | Completado | Configuración de AWS Budget de $5 USD y estructura base del repositorio. |
| Día 2 | Completado | API local con FastAPI, pruebas con Pytest, Dockerfile, `.dockerignore` e imagen Docker funcional. |
| Día 3 | Completado | GitHub Actions ejecuta pruebas automáticamente en cada push y pull request. |
| Día 4 | Completado | GitHub Actions construye la imagen Docker, levanta el contenedor y ejecuta smoke test contra `/health`. |
| Día 5 | Próximo | Integración de Trivy para escaneo de vulnerabilidades en la imagen Docker antes de desplegar. |
| Día 6 | Pendiente | Preparación segura de EC2 en AWS para laboratorio Kubernetes barato. |
| Día 7 | Pendiente | Instalación de K3s o Minikube en EC2. |
| Día 8 | Pendiente | Creación de manifiestos Kubernetes: Deployment, Service y Secrets. |
| Día 9 | Pendiente | Despliegue de la aplicación en Kubernetes. |
| Día 10 | Pendiente | Documentación final, evidencias, diagrama de arquitectura y retrospectiva técnica. |

> Nota actual: el proyecto ya cuenta con CI funcional para pruebas Python y validación básica de contenedor. El siguiente bloque de trabajo debe comenzar en el **Día 5: Trivy**.

---

## Arquitectura actual

```text
┌─────────────────────┐
│ Cliente / curl      │
└──────────┬──────────┘
           │
           │ HTTP POST /webhook
           │ Header: X-Webhook-Signature
           ▼
┌─────────────────────────────┐
│ FastAPI Webhook Validator   │
│                             │
│ - Lee el payload            │
│ - Calcula HMAC SHA-256      │
│ - Compara la firma          │
│ - Acepta o rechaza          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Docker Container            │
│ python:3.12-slim            │
│ non-root user               │
└─────────────────────────────┘
```

Arquitectura actual del pipeline:

```text
Developer
   ↓
git push / pull request
   ↓
GitHub Actions
   ↓
Job 1: Run Python tests
   ↓
Job 2: Build Docker image
   ↓
Run container
   ↓
Smoke test: curl /health
   ↓
CI Success / Failure
```

Arquitectura futura:

```text
GitHub Repository
   ↓
GitHub Actions
   ↓
Pytest
   ↓
Docker Build
   ↓
Trivy Scan
   ↓
AWS EC2
   ↓
K3s / Minikube
   ↓
Kubernetes Deployment
```

---

## Stack técnico

| Área | Herramienta |
|---|---|
| Lenguaje | Python |
| Framework API | FastAPI |
| Servidor ASGI | Uvicorn |
| Testing | Pytest |
| Cliente de pruebas | HTTPX / FastAPI TestClient |
| Contenedores | Docker |
| CI/CD | GitHub Actions |
| Build de contenedor en CI | Docker Buildx + docker/build-push-action |
| Smoke test | `curl --fail http://localhost:8000/health` |
| Escaneo de seguridad | Trivy |
| Cloud | AWS EC2 |
| Orquestación | Kubernetes con K3s o Minikube |
| Control de costos | AWS Budgets |

---

## Estructura del proyecto

Si este proyecto vive dentro del monorepo `devsecops-learning-log`, la estructura relevante es:

```text
devsecops-learning-log/
├── .github/
│   └── workflows/
│       └── webhook-validator-ci.yml
└── python-projects/
    └── webhook-validator-secops/
        ├── app/
        │   ├── __init__.py
        │   └── main.py
        ├── tests/
        │   └── test_main.py
        ├── .dockerignore
        ├── Dockerfile
        ├── pyproject.toml
        ├── requirements.txt
        └── README.md
```

---

## Endpoints disponibles

### Health Check

```http
GET /health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "service": "webhook-validator"
}
```

### Validación de Webhook

```http
POST /webhook
```

Header requerido:

```http
X-Webhook-Signature: sha256=<firma_hmac>
```

Respuesta con firma válida:

```json
{
  "message": "Webhook accepted",
  "payload_size": 42
}
```

Respuesta con firma inválida:

```json
{
  "detail": "Invalid webhook signature"
}
```

---

## Código principal de la API

El microservicio usa un secreto definido por variable de entorno:

```python
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dev-secret")
```

Para desarrollo local se usa `dev-secret`. Para producción, este valor debe venir de una variable de entorno segura o de un `Secret` de Kubernetes.

La firma se genera usando HMAC SHA-256:

```python
hmac.new(
    key=secret.encode("utf-8"),
    msg=payload,
    digestmod=hashlib.sha256,
).hexdigest()
```

La comparación se hace con:

```python
hmac.compare_digest(expected_signature, received_signature)
```

Esto evita comparaciones inseguras entre strings.

---

## Cómo correr el proyecto localmente

### 1. Crear entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Ejecutar pruebas

```bash
pytest
```

Resultado esperado:

```text
4 passed
```

### 4. Levantar la API localmente

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Probar health check:

```bash
curl http://localhost:8000/health
```

Para detener `uvicorn`:

```text
CTRL + C
```

---

## Cómo probar el webhook con firma válida

```bash
PAYLOAD='{"event":"payment.created","id":"evt_123"}'
SECRET='dev-secret'

SIGNATURE="sha256=$(printf '%s' "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | awk '{print $2}')"

echo "$SIGNATURE"

curl -i -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: $SIGNATURE" \
  -d "$PAYLOAD"
```

Respuesta esperada:

```text
HTTP/1.1 200 OK
```

```json
{
  "message": "Webhook accepted",
  "payload_size": 42
}
```

---

## Cómo probar el webhook con firma inválida

```bash
curl -i -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=wrong" \
  -d "$PAYLOAD"
```

Respuesta esperada:

```text
HTTP/1.1 403 Forbidden
```

```json
{
  "detail": "Invalid webhook signature"
}
```

---

## Cómo construir la imagen Docker

```bash
docker build -t webhook-validator:local .
```

Verificar que la imagen existe:

```bash
docker images | grep webhook-validator
```

---

## Cómo correr la API con Docker

```bash
docker run --rm -p 8000:8000 -e WEBHOOK_SECRET=dev-secret webhook-validator:local
```

Probar:

```bash
curl http://localhost:8000/health
```

Respuesta esperada:

```json
{
  "status": "ok",
  "service": "webhook-validator"
}
```

Para detener el contenedor:

```text
CTRL + C
```

Si el contenedor corre en segundo plano:

```bash
docker ps
docker rm -f <container_id_or_name>
```

---

## Dockerfile actual

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## GitHub Actions CI

El proyecto ya cuenta con un workflow en:

```text
.github/workflows/webhook-validator-ci.yml
```

Este workflow corre cuando hay cambios en:

```text
python-projects/webhook-validator-secops/**
.github/workflows/webhook-validator-ci.yml
```

Eventos soportados:

- `push`
- `pull_request`
- `workflow_dispatch`

Jobs actuales:

```text
Run Python tests
   ↓
Build and smoke test Docker image
```

### Workflow actual esperado

```yaml
name: Webhook Validator CI

on:
  push:
    branches:
      - main
      - "feature/**"
      - "security/**"
    paths:
      - "python-projects/webhook-validator-secops/**"
      - ".github/workflows/webhook-validator-ci.yml"

  pull_request:
    branches:
      - main
    paths:
      - "python-projects/webhook-validator-secops/**"
      - ".github/workflows/webhook-validator-ci.yml"

  workflow_dispatch:

permissions:
  contents: read

jobs:
  test:
    name: Run Python tests
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: python-projects/webhook-validator-secops

    steps:
      - name: Checkout repository
        uses: actions/checkout@v5

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.12"
          cache: "pip"
          cache-dependency-path: "python-projects/webhook-validator-secops/requirements.txt"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: python -m pytest -v

  docker-build:
    name: Build and smoke test Docker image
    runs-on: ubuntu-latest
    needs: test

    steps:
      - name: Checkout repository
        uses: actions/checkout@v5

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v6
        with:
          context: ./python-projects/webhook-validator-secops
          file: ./python-projects/webhook-validator-secops/Dockerfile
          push: false
          load: true
          tags: webhook-validator:ci

      - name: Run container
        run: |
          docker run -d \
            --name webhook-validator-ci \
            -p 8000:8000 \
            -e WEBHOOK_SECRET=dev-secret \
            webhook-validator:ci

      - name: Smoke test health endpoint
        run: |
          sleep 5
          curl --fail http://localhost:8000/health

      - name: Clean up container
        if: always()
        run: |
          docker rm -f webhook-validator-ci || true
```

### Nota sobre actualización de GitHub Actions

Durante el Día 4 apareció una annotation de deprecación relacionada con Node.js 20 en GitHub Actions. Se actualizó el workflow para usar versiones compatibles con Node 24:

```text
actions/checkout@v5
actions/setup-python@v6
```

Esto mantiene el pipeline más limpio y evita depender de versiones próximas a quedar obsoletas.

---

## Buenas prácticas ya aplicadas

### Seguridad financiera

- Se configuró un AWS Budget mensual de $5 USD.
- Se evita crear infraestructura cloud antes de tener control de costos.
- Aún no se ha creado ninguna instancia EC2 para evitar cargos innecesarios.

### Seguridad de aplicación

- El endpoint `/webhook` requiere firma HMAC.
- Se rechazan peticiones sin firma.
- Se rechazan peticiones con firma inválida.
- Se usa `hmac.compare_digest()` para comparar firmas de forma segura.
- El secreto se carga mediante variable de entorno.

### Seguridad de contenedor

- Imagen base ligera: `python:3.12-slim`.
- No se ejecuta la aplicación como root.
- Se usa `.dockerignore` para evitar copiar archivos innecesarios.
- Se usa `pip install --no-cache-dir` para reducir basura en la imagen.

### Calidad y CI/CD

- Pruebas automatizadas con Pytest.
- Separación entre código de aplicación y pruebas.
- Configuración de `pyproject.toml` para facilitar imports en Pytest.
- GitHub Actions ejecuta pruebas automáticamente.
- El pipeline construye la imagen Docker desde cero.
- El pipeline levanta el contenedor y ejecuta un smoke test contra `/health`.
- El job de Docker depende del job de pruebas mediante `needs: test`.
- Se aplican permisos mínimos en el workflow con `permissions: contents: read`.
- Repositorio versionado con Git y trabajo por branches.

---

## Lección de Git aprendida durante el Día 4

Durante la actualización del workflow, una branch anterior quedó desfasada respecto a `main`.

El hallazgo fue que la branch vieja podía eliminar el job `docker-build` si se mergeaba después de que `main` ya tenía el Día 4 completado.

Comandos útiles para detectar esto:

```bash
git fetch --all --prune
git diff --name-only main..origin/feature/webhook-validator-ci
git diff main..origin/feature/webhook-validator-ci -- .github/workflows/webhook-validator-ci.yml
```

Conclusión práctica:

```text
No se debe mergear una branch vieja sin compararla contra main.
main debe conservar el workflow completo con:
- Run Python tests
- Build and smoke test Docker image
```

Para limpiar una branch remota obsoleta:

```bash
git push origin --delete feature/webhook-validator-ci
```

Para borrarla localmente:

```bash
git branch -D feature/webhook-validator-ci
```

---

## Próximos sprints diarios de 2 horas

Como los Días 1 al 4 ya están completados, el plan continúa desde el Día 5.

### Día 5 — Trivy: escaneo de vulnerabilidades

Objetivo:

- Integrar Trivy en GitHub Actions.
- Escanear la imagen Docker antes de considerarla lista para despliegue.

Concepto:

Trivy funcionará como un scanner de seguridad para detectar vulnerabilidades conocidas en paquetes del sistema, librerías y dependencias dentro de la imagen.

Criterio de éxito:

- El pipeline ejecuta Trivy.
- El resultado aparece dentro de GitHub Actions.
- Se define una política inicial para fallar el build ante vulnerabilidades críticas.

---

### Día 6 — AWS EC2: preparación segura y barata

Objetivo:

- Crear una instancia EC2 pequeña para laboratorio.
- Acceder por SSH.
- Verificar costos y apagar recursos cuando no se usen.

Concepto:

EC2 será nuestro servidor barato para simular un ambiente cloud real sin usar EKS, que sería más costoso para este nivel de laboratorio.

Criterio de éxito:

- Existe una instancia EC2 funcionando.
- Se puede acceder por SSH.
- Se documenta cómo detenerla para evitar costos innecesarios.

---

### Día 7 — Kubernetes ligero con K3s o Minikube

Objetivo:

- Instalar K3s o Minikube dentro de la instancia EC2.
- Verificar que `kubectl` funciona.

Concepto:

Kubernetes será el orquestador. En lugar de correr el contenedor manualmente con `docker run`, Kubernetes se encargará de mantener la aplicación viva mediante objetos declarativos.

Criterio de éxito:

- `kubectl get nodes` muestra un nodo activo.
- El clúster local dentro de EC2 está listo.

---

### Día 8 — Manifiestos Kubernetes

Objetivo:

- Crear archivos YAML para `Deployment`, `Service` y `Secret`.

Concepto:

Los manifiestos YAML son instrucciones declarativas. En lugar de decirle manualmente al servidor qué hacer paso por paso, describimos el estado deseado.

Criterio de éxito:

- Existen archivos Kubernetes organizados en una carpeta `k8s/`.
- La app puede desplegarse con `kubectl apply -f k8s/`.

---

### Día 9 — Despliegue en Kubernetes

Objetivo:

- Desplegar la API dentro del clúster.
- Probar el endpoint `/health` desde Kubernetes.

Concepto:

Este será el paso donde la app deja de ser solo un contenedor manual y pasa a correr como workload orquestado.

Criterio de éxito:

- `kubectl get pods` muestra el pod corriendo.
- `kubectl get svc` muestra el servicio.
- `/health` responde desde el despliegue Kubernetes.

---

### Día 10 — Documentación final y evidencias de portafolio

Objetivo:

- Actualizar README final.
- Agregar diagrama de arquitectura.
- Agregar screenshots o comandos de evidencia.
- Escribir una explicación tipo entrevista.

Concepto:

Un proyecto de portafolio no solo debe funcionar; también debe poder explicarse. Este día convierte el trabajo técnico en una historia profesional clara.

Criterio de éxito:

- README completo.
- Arquitectura documentada.
- Flujo DevSecOps explicado.
- Proyecto listo para compartir en GitHub o LinkedIn.

---

## Comandos útiles de control

Ver estado de Git:

```bash
git status
```

Ejecutar pruebas:

```bash
pytest
```

Construir imagen:

```bash
docker build -t webhook-validator:local .
```

Correr contenedor:

```bash
docker run --rm -p 8000:8000 -e WEBHOOK_SECRET=dev-secret webhook-validator:local
```

Ver contenedores corriendo:

```bash
docker ps
```

Detener un contenedor:

```bash
docker stop <container_id>
```

Ver historial de commits:

```bash
git log --oneline
```

Comparar una branch con `main`:

```bash
git diff --name-only main..origin/<branch-name>
```

---

## Cómo explicar este proyecto en entrevista

Este proyecto demuestra que puedo tomar una aplicación pequeña y llevarla por un flujo moderno de entrega segura.

La API en sí es simple: valida webhooks usando HMAC SHA-256. Pero el propósito real es mostrar prácticas DevSecOps/SRE:

- Controlé costos antes de crear infraestructura en AWS.
- Escribí una API con validación de seguridad básica.
- Agregué pruebas automatizadas para comprobar comportamiento esperado.
- Empaqueté la aplicación en Docker usando una imagen ligera.
- Evité correr el contenedor como root.
- Configuré GitHub Actions para ejecutar pruebas automáticamente.
- Extendí el pipeline para construir la imagen Docker.
- Agregué un smoke test para confirmar que el contenedor arranca y responde en `/health`.
- Actualicé las acciones de GitHub para evitar deprecaciones relacionadas con Node.js 20.
- El siguiente paso será escanear la imagen con Trivy antes del despliegue.
- Finalmente, la app se desplegará en Kubernetes usando una alternativa barata a EKS.

En términos profesionales, este proyecto conecta conocimientos de seguridad, automatización, infraestructura y confiabilidad operacional.

---

## Estado de costos

- AWS Budget configurado: sí.
- Límite mensual objetivo: $5 USD.
- Recursos AWS creados hasta este punto: ninguno.
- Riesgo actual de costo cloud: bajo.

---

## Licencia

Proyecto de aprendizaje personal para portafolio DevSecOps/SRE.
