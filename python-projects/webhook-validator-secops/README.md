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
- Documentación de hallazgos en `SECURITY_AUDIT.md`.
- Triage de CVE y remediación de dependencias.
- Reducción de superficie de ataque mediante imagen base Alpine.
- Despliegue futuro en Kubernetes usando K3s o Minikube dentro de una instancia EC2 en AWS.
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
CVE triage
   ↓
Remediación o documentación de riesgo
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
| Día 5 | Completado | Trivy, CVE triage, actualización de dependencias, `SECURITY_AUDIT.md` y cambio de imagen base a Alpine. |
| Día 6 | Próximo | Preparación segura de EC2 en AWS para laboratorio Kubernetes barato. |
| Día 7 | Pendiente | Instalación de K3s o Minikube en EC2. |
| Día 8 | Pendiente | Creación de manifiestos Kubernetes: Deployment, Service y Secrets. |
| Día 9 | Pendiente | Despliegue de la aplicación en Kubernetes. |
| Día 10 | Pendiente | Documentación final, evidencias, diagrama de arquitectura y retrospectiva técnica. |

> Nota actual: el proyecto ya cuenta con CI funcional, build Docker, smoke test, Trivy, documentación de seguridad, triage de CVE y una imagen Alpine que redujo los hallazgos HIGH/CRITICAL en el escaneo probado.

---

## Arquitectura actual

```text
┌─────────────────────┐
│ Cliente / curl      │
└──────────┬──────────┘
           │
           │ HTTP POST /webhook
           │ Header: X-Webhook-Signature
           │ Optional: X-Request-ID
           ▼
┌─────────────────────────────┐
│ FastAPI Webhook Validator   │
│                             │
│ - Lee el payload            │
│ - Calcula HMAC SHA-256      │
│ - Compara la firma          │
│ - Registra evento seguro    │
│ - Acepta o rechaza          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Docker Container            │
│ python:3.12-alpine          │
│ non-root user               │
│ Docker HEALTHCHECK          │
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
Trivy image scan
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
   ↓
Readiness/Liveness Probes
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
| Imagen base actual | `python:3.12-alpine` |
| CI/CD | GitHub Actions |
| Build de contenedor en CI | Docker Buildx + docker/build-push-action |
| Smoke test | `curl --fail http://localhost:8000/health` |
| Escaneo de seguridad | Trivy |
| Auditoría local | `scripts/local-security-audit.sh` |
| Reporte de seguridad | `SECURITY_AUDIT.md` |
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
        ├── scripts/
        │   ├── local-security-audit.sh
        │   └── audit_recommender.py
        ├── .dockerignore
        ├── .env.example
        ├── .gitignore
        ├── Dockerfile
        ├── pyproject.toml
        ├── requirements.txt
        ├── SECURITY_AUDIT.md
        └── README.md
```

---

## Endpoints disponibles

### Health Check / Liveness

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

Este endpoint confirma que el proceso de la aplicación está vivo.

---

### Readiness Check

```http
GET /ready
```

Respuesta esperada en ambiente listo:

```json
{
  "status": "ready",
  "service": "webhook-validator",
  "environment": "development"
}
```

En ambientes production-like, `/ready` valida que `WEBHOOK_SECRET` esté configurado.

---

### Validación de Webhook

```http
POST /webhook
```

Header requerido:

```http
X-Webhook-Signature: sha256=<firma_hmac>
```

Header opcional para trazabilidad:

```http
X-Request-ID: <request-id>
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

Respuesta sin firma:

```json
{
  "detail": "Missing webhook signature"
}
```

---

## Seguridad de secretos

El microservicio usa un secreto definido por variable de entorno:

```text
WEBHOOK_SECRET
```

Para ambientes locales de desarrollo se permite un secreto de prueba. Para ambientes production-like, el secreto debe estar definido explícitamente.

Esto prepara el proyecto para usar un futuro `Secret` de Kubernetes.

Variables documentadas:

```env
APP_ENV=development
WEBHOOK_SECRET=dev-secret
```

---

## Validación HMAC

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

## Observabilidad básica

El proyecto incluye:

- Logging seguro de webhooks aceptados/rechazados.
- No se imprimen secretos.
- No se imprimen firmas.
- No se imprimen payloads completos.
- Se registra `payload_size`.
- Se propaga o genera `X-Request-ID`.

Ejemplo:

```text
Webhook rejected: invalid signature | request_id=<id> | payload_size=<size>
```

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
9 passed
```

### 4. Levantar la API localmente

```bash
APP_ENV=development uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Probar health check:

```bash
curl http://localhost:8000/health
```

Probar readiness:

```bash
curl http://localhost:8000/ready
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
  -H "X-Request-ID: local-test-123" \
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
curl http://localhost:8000/ready
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
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production

WORKDIR /app

RUN addgroup -S appgroup && adduser -S -G appgroup appuser

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).read()" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## GitHub Actions CI

El proyecto cuenta con un workflow en:

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
Build, scan, and smoke test Docker image
```

### Pipeline esperado

```text
Checkout repository
   ↓
Set up Python
   ↓
Install dependencies
   ↓
Run Pytest
   ↓
Build Docker image
   ↓
Run Trivy vulnerability scan
   ↓
Run container
   ↓
Smoke test /health
   ↓
Clean up container
```

### Nota sobre actualización de GitHub Actions

Durante el Día 4 apareció una annotation de deprecación relacionada con Node.js 20 en GitHub Actions. Se actualizó el workflow para usar versiones compatibles con Node 24:

```text
actions/checkout@v5
actions/setup-python@v6
```

Esto mantiene el pipeline más limpio y evita depender de versiones próximas a quedar obsoletas.

---

## Trivy y CVE Triage

Durante el escaneo con Trivy se encontraron dos grupos de hallazgos:

```text
1. Dependencias Python, especialmente Starlette.
2. Paquetes del sistema operativo heredados de la imagen base Debian slim.
```

### Starlette

Trivy reportó hallazgos HIGH en `starlette` con versiones corregidas disponibles.

Acciones realizadas:

- Se actualizó FastAPI.
- Se fijó Starlette directamente como remediación temporal de seguridad.
- Se ejecutó `pip check`.
- Se ejecutó Pytest.
- Se reconstruyó la imagen.
- Se volvió a ejecutar Trivy.

### Paquetes del sistema operativo

Trivy también reportó HIGH/CRITICAL en paquetes heredados de `python:3.12-slim`, como:

- `perl-base`
- `util-linux`
- `gzip`
- `ncurses`
- `libblkid`
- `libmount`
- `libuuid`

Varios hallazgos no tenían `FixedVersion`.

Decisión:

- Se documentó el análisis en `SECURITY_AUDIT.md`.
- Se probó una imagen base alternativa.
- Se cambió de `python:3.12-slim` a `python:3.12-alpine`.

Resultado:

```text
La imagen Alpine no arrojó findings HIGH ni CRITICAL en el escaneo probado.
```

---

## Auditoría local de seguridad

El proyecto incluye un flujo local para auditoría:

```bash
./scripts/local-security-audit.sh
```

Este script puede ejecutar:

- Pytest
- Bandit
- pip-audit
- Docker build
- Trivy image scan
- Generación de resumen con recomendaciones

Los reportes se guardan en:

```text
audit-reports/
```

Esta carpeta está ignorada por Git.

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
- Producción requiere `WEBHOOK_SECRET` explícito.
- Logging seguro sin secretos, firmas ni payloads completos.
- `X-Request-ID` permite trazabilidad por request.

### Seguridad de contenedor

- Imagen base actual: `python:3.12-alpine`.
- No se ejecuta la aplicación como root.
- Se usa `.dockerignore` para evitar copiar archivos innecesarios.
- Se usa `pip install --no-cache-dir` para reducir basura en la imagen.
- Se agregó Docker `HEALTHCHECK`.
- Se redujo superficie de ataque al migrar desde Debian slim a Alpine.

### Calidad y CI/CD

- Pruebas automatizadas con Pytest.
- Separación entre código de aplicación y pruebas.
- Configuración de `pyproject.toml` para facilitar imports en Pytest.
- GitHub Actions ejecuta pruebas automáticamente.
- El pipeline construye la imagen Docker desde cero.
- El pipeline levanta el contenedor y ejecuta un smoke test contra `/health`.
- El job de Docker depende del job de pruebas mediante `needs: test`.
- Se aplican permisos mínimos en el workflow con `permissions: contents: read`.
- Trivy se usa para validar vulnerabilidades en la imagen.
- Repositorio versionado con Git y trabajo por branches.

---

## Lecciones aprendidas durante el proyecto

### Branch management

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

---

### Vulnerability triage

El escaneo de seguridad no termina cuando una herramienta reporta vulnerabilidades.

Proceso aplicado:

```text
Trivy finding
   ↓
Identificar paquete afectado
   ↓
Distinguir app dependency vs OS base image
   ↓
Revisar si existe FixedVersion
   ↓
Remediar si hay fix disponible
   ↓
Documentar si no hay fix
   ↓
Probar alternativa de base image
   ↓
Validar funcionalidad y volver a escanear
```

---

## Próximos sprints diarios de 2 horas

Como los Días 1 al 5 ya están completados, el plan continúa desde el Día 6.

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

Escanear imagen con Trivy:

```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image \
  --scanners vuln \
  --severity HIGH,CRITICAL \
  webhook-validator:local
```

---

## Cómo explicar este proyecto en entrevista

Este proyecto demuestra que puedo tomar una aplicación pequeña y llevarla por un flujo moderno de entrega segura.

La API en sí es simple: valida webhooks usando HMAC SHA-256. Pero el propósito real es mostrar prácticas DevSecOps/SRE:

- Controlé costos antes de crear infraestructura en AWS.
- Escribí una API con validación de seguridad básica.
- Agregué pruebas automatizadas para comprobar comportamiento esperado.
- Empaqueté la aplicación en Docker.
- Evité correr el contenedor como root.
- Agregué healthcheck, readiness y request IDs.
- Configuré GitHub Actions para ejecutar pruebas automáticamente.
- Extendí el pipeline para construir la imagen Docker.
- Agregué un smoke test para confirmar que el contenedor arranca y responde en `/health`.
- Integré Trivy para analizar vulnerabilidades.
- Investigué hallazgos CVE y diferencié dependencias Python de paquetes heredados de la imagen base.
- Remedié Starlette cuando existía fix disponible.
- Cambié la imagen base a Alpine para reducir la superficie de ataque.
- El siguiente paso será desplegar la aplicación en Kubernetes usando una alternativa barata a EKS.

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
