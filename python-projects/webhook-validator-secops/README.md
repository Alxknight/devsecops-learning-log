# Webhook Validator SecOps

> **Estado del proyecto:** Completo para el alcance técnico y educativo definido  
> **Estado de desarrollo:** Conservado como entregable final de aprendizaje; no se planean nuevas funciones en esta etapa

Microservicio en Python que valida webhooks mediante firmas **HMAC SHA-256** y demuestra un flujo local de entrega segura con FastAPI, Pytest, Docker, GitHub Actions, Trivy y Kubernetes.

La aplicación es deliberadamente pequeña. El objetivo principal del proyecto fue practicar cómo llevar un servicio desde el código hasta un entorno local orquestado, aplicando pruebas, controles de seguridad, automatización y troubleshooting.

---

## Propósito del proyecto

Un endpoint público no debe confiar automáticamente en cualquier petición que reciba. Un atacante podría intentar enviar un payload falso y hacerlo pasar por un evento legítimo de un sistema externo.

Este servicio exige una firma calculada con un secreto compartido:

```text
Cliente externo
    ↓
Payload + firma HMAC
    ↓
FastAPI recibe los bytes del payload
    ↓
El servicio recalcula la firma esperada
    ↓
Compara ambas firmas de forma segura
    ↓
Acepta o rechaza el webhook
```

El proyecto conecta esa validación con un ciclo DevSecOps local:

```text
Código
  ↓
Pruebas automatizadas
  ↓
Imagen Docker endurecida
  ↓
Pipeline de CI
  ↓
Escaneo de vulnerabilidades
  ↓
Smoke test
  ↓
Manifests Kubernetes
  ↓
Despliegue local reproducible
```

---

## Alcance final

La versión terminada incluye:

- API con FastAPI y Uvicorn
- Endpoint de liveness: `/health`
- Endpoint de readiness: `/ready`
- Endpoint protegido: `/webhook`
- Validación HMAC SHA-256
- Comparación segura con `hmac.compare_digest()`
- Configuración mediante variables de entorno
- Requerimiento explícito de `WEBHOOK_SECRET` en ambientes similares a producción
- Propagación o generación de `X-Request-ID`
- Logging sin secretos, firmas ni payloads completos
- Pruebas automatizadas con Pytest
- Imagen Docker basada en Alpine
- Ejecución con UID/GID numérico no-root
- Docker `HEALTHCHECK`
- GitHub Actions para pruebas, build, Trivy y smoke test
- Documentación de triage en `SECURITY_AUDIT.md`
- Namespace, Secret, Deployment y Service para Kubernetes
- Readiness y liveness probes
- Requests y limits de CPU/memoria
- Security context restrictivo
- Despliegue y limpieza local automatizados con Bash y Minikube

---

## Arquitectura

### Aplicación

```text
┌──────────────────────────┐
│ Cliente externo / curl   │
└────────────┬─────────────┘
             │ POST /webhook
             │ X-Webhook-Signature
             │ X-Request-ID opcional
             ▼
┌──────────────────────────┐
│ FastAPI                  │
│                          │
│ 1. Lee el payload        │
│ 2. Obtiene el secreto    │
│ 3. Calcula HMAC SHA-256  │
│ 4. Compara las firmas    │
│ 5. Registra el resultado │
└────────────┬─────────────┘
             │
             ▼
   200 aceptado / 403 rechazado
```

### Contenedor

```text
python:3.12-alpine
        ↓
Dependencias Python
        ↓
Código de la aplicación
        ↓
Usuario 10001:10001
        ↓
Uvicorn en puerto 8000
        ↓
HEALTHCHECK a /health
```

### Kubernetes local

```text
Docker build local
        ↓
minikube image load
        ↓
Namespace webhook-validator
        ↓
Kubernetes Secret
        ↓
Deployment
        ↓
Pod no-root
        ↓
Service ClusterIP
        ↓
kubectl port-forward
        ↓
Pruebas con curl
```

---

## Stack técnico

| Área | Tecnología |
|---|---|
| Lenguaje | Python 3 |
| API | FastAPI |
| Servidor | Uvicorn |
| Pruebas | Pytest y FastAPI TestClient |
| Firma | HMAC SHA-256 |
| Contenedores | Docker |
| Imagen base | `python:3.12-alpine` |
| CI/CD | GitHub Actions |
| Escaneo | Trivy |
| Kubernetes local | Minikube y kubectl |
| Automatización | Bash |
| Documentación de seguridad | `SECURITY_AUDIT.md` |

---

## Estructura del proyecto

```text
webhook-validator-secops/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── k8s/
│   ├── namespace.yaml
│   ├── secret.example.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── README.md
├── scripts/
│   ├── audit_recommender.py
│   ├── local-security-audit.sh
│   ├── k8s-local-deploy.sh
│   └── k8s-local-cleanup.sh
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

## Endpoints

## `GET /health`

Confirma que el proceso está vivo.

```json
{
  "status": "ok",
  "service": "webhook-validator"
}
```

Uso principal:

- Docker health check
- Kubernetes liveness probe
- Smoke test del contenedor

---

## `GET /ready`

Confirma que el servicio está configurado para recibir tráfico.

```json
{
  "status": "ready",
  "service": "webhook-validator",
  "environment": "production"
}
```

En ambientes similares a producción, la readiness depende de que `WEBHOOK_SECRET` exista.

Uso principal:

- Kubernetes readiness probe
- Separar “el proceso está vivo” de “el servicio está listo”

---

## `POST /webhook`

Header requerido:

```http
X-Webhook-Signature: sha256=<firma_hmac>
```

Header opcional:

```http
X-Request-ID: <identificador>
```

Respuesta esperada con una firma válida:

```json
{
  "message": "Webhook accepted",
  "payload_size": 42
}
```

Respuesta sin firma:

```json
{
  "detail": "Missing webhook signature"
}
```

Respuesta con firma inválida:

```json
{
  "detail": "Invalid webhook signature"
}
```

---

## Modelo de seguridad

### Firma HMAC

La firma esperada se calcula con el payload original y el secreto compartido:

```python
hmac.new(
    key=secret.encode("utf-8"),
    msg=payload,
    digestmod=hashlib.sha256,
).hexdigest()
```

La comparación usa:

```python
hmac.compare_digest(expected_signature, received_signature)
```

`compare_digest()` evita usar una comparación de strings convencional para un valor sensible.

### Secretos

El secreto se obtiene de:

```text
WEBHOOK_SECRET
```

Ejemplo local:

```env
APP_ENV=development
WEBHOOK_SECRET=dev-secret
```

No se deben incluir secretos reales en:

- El código
- El Dockerfile
- Los manifests versionados
- El historial de Git
- Los logs

En Kubernetes, el valor se inyecta mediante un Secret.

### Logging

El servicio registra información útil sin imprimir:

- El secreto
- La firma completa
- El payload completo

Puede registrar:

- Resultado aceptado o rechazado
- `request_id`
- Tamaño del payload

---

## Ejecución local sin Docker

Crear un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Ejecutar las pruebas:

```bash
pytest -v
```

Levantar la API:

```bash
APP_ENV=development \
WEBHOOK_SECRET=dev-secret \
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Validar endpoints:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
```

---

## Prueba de un webhook firmado

```bash
PAYLOAD='{"event":"payment.created","id":"evt_123"}'
SECRET='dev-secret'

SIGNATURE="sha256=$(printf '%s' "$PAYLOAD" \
  | openssl dgst -sha256 -hmac "$SECRET" \
  | awk '{print $2}')"

curl -i -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: local-test-123" \
  -H "X-Webhook-Signature: $SIGNATURE" \
  -d "$PAYLOAD"
```

Una firma incorrecta debe ser rechazada:

```bash
curl -i -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=wrong" \
  -d "$PAYLOAD"
```

---

## Docker

Construir la imagen:

```bash
docker build -t webhook-validator:local .
```

Ejecutar el contenedor:

```bash
docker run --rm \
  -p 8000:8000 \
  -e APP_ENV=production \
  -e WEBHOOK_SECRET=dev-secret \
  webhook-validator:local
```

Validar:

```bash
curl --fail http://localhost:8000/health
curl --fail http://localhost:8000/ready
```

### Controles aplicados al contenedor

- Imagen base Alpine
- Instalación sin caché de `pip`
- `.dockerignore`
- Usuario y grupo numéricos `10001:10001`
- Aplicación no-root
- Puerto documentado
- Docker `HEALTHCHECK`
- Sin secretos integrados en la imagen

---

## Pipeline de CI

El workflow se encuentra en:

```text
.github/workflows/webhook-validator-ci.yml
```

Flujo final:

```text
Push / Pull Request
        ↓
Checkout
        ↓
Configurar Python
        ↓
Instalar dependencias
        ↓
Ejecutar Pytest
        ↓
Construir imagen Docker
        ↓
Escanear con Trivy
        ↓
Levantar contenedor
        ↓
Smoke test a /health
        ↓
Eliminar contenedor
```

El job de la imagen depende de que las pruebas hayan pasado. Esto evita continuar con el empaquetado de una versión que ya falló en la validación básica.

El workflow utiliza permisos mínimos de lectura del repositorio cuando no necesita escribir contenido.

---

## Trivy y triage de vulnerabilidades

El proyecto no trata un escaneo como una lista automática de instrucciones. Los hallazgos se clasifican según su origen:

```text
Finding de Trivy
      ↓
¿Dependencia Python o paquete del sistema operativo?
      ↓
¿Existe una versión corregida?
      ↓
Actualizar y probar, o documentar la ausencia de fix
      ↓
Reconstruir la imagen
      ↓
Volver a escanear
```

Durante el proyecto se analizaron:

- Hallazgos en dependencias relacionadas con FastAPI y Starlette
- Vulnerabilidades heredadas de la imagen Debian slim
- Diferencias entre una base Debian y una base Alpine

La migración a `python:3.12-alpine` redujo a cero los hallazgos HIGH/CRITICAL en el escaneo probado de esa versión.

Ese resultado describe una ejecución concreta del escáner; no significa que la imagen sea permanentemente libre de vulnerabilidades.

El razonamiento y las decisiones se documentan en:

```text
SECURITY_AUDIT.md
```

---

## Auditoría local

El script:

```bash
./scripts/local-security-audit.sh
```

puede coordinar validaciones como:

- Pytest
- Bandit
- `pip-audit`
- Docker build
- Trivy
- Generación de un resumen de recomendaciones

Los reportes de máquina se almacenan localmente en:

```text
audit-reports/
```

La carpeta se ignora en Git para evitar versionar resultados temporales y ruidosos. El repositorio conserva el proceso reproducible y la documentación humana.

---

## Kubernetes local

Requisitos:

```bash
docker --version
kubectl version --client
minikube version
```

Iniciar el clúster:

```bash
minikube start \
  --driver=docker \
  --cpus=2 \
  --memory=3072 \
  --disk-size=10g
```

### Objetos utilizados

| Objeto | Propósito |
|---|---|
| Namespace | Aislar los recursos del proyecto |
| Secret | Entregar `WEBHOOK_SECRET` al contenedor |
| Deployment | Mantener el estado deseado del Pod |
| Pod | Ejecutar la imagen |
| Service | Proporcionar una dirección interna estable |
| Readiness probe | Retirar tráfico cuando la aplicación no está lista |
| Liveness probe | Detectar un proceso no saludable |
| Requests y limits | Controlar CPU y memoria |
| Security context | Reducir privilegios del contenedor |

### Despliegue automatizado

```bash
./scripts/k8s-local-deploy.sh
```

El flujo automatizado:

1. Comprueba las herramientas requeridas.
2. Inicia Minikube cuando es necesario.
3. Construye la imagen.
4. Carga la imagen en Minikube.
5. Aplica el Namespace.
6. Crea o actualiza el Secret local.
7. Aplica Deployment y Service.
8. Reinicia el Deployment para usar la imagen actual.
9. Espera el rollout.
10. Muestra los recursos resultantes.

Probar el servicio:

```bash
kubectl port-forward \
  svc/webhook-validator \
  8080:80 \
  -n webhook-validator
```

En otra terminal:

```bash
curl http://localhost:8080/health
curl http://localhost:8080/ready
```

### Limpieza

```bash
./scripts/k8s-local-cleanup.sh
```

O manualmente:

```bash
kubectl delete namespace webhook-validator --ignore-not-found=true
```

---

## Pruebas automatizadas

La suite final valida nueve comportamientos principales, entre ellos:

- Liveness
- Readiness en desarrollo
- Readiness en un ambiente similar a producción
- Propagación o generación de `X-Request-ID`
- Webhook con firma válida
- Webhook sin firma
- Webhook con firma inválida
- Lectura del secreto desde el ambiente
- Comportamiento esperado de configuración

Ejecutar:

```bash
pytest -v
```

---

## Troubleshooting documentado

### Usuario no numérico en Kubernetes

El contenedor funcionaba con Docker, pero Kubernetes mostró:

```text
container has runAsNonRoot and image has non-numeric user
```

La solución fue usar un UID/GID explícito:

```dockerfile
USER 10001:10001
```

No se eliminó `runAsNonRoot`. Se corrigió la imagen para que Kubernetes pudiera comprobar el control.

### Branch desactualizada

Una branch antigua podía sobrescribir trabajo más reciente del pipeline. La comparación contra `main` permitió identificar el riesgo antes del merge:

```bash
git fetch --all --prune
git diff --name-only main..origin/<branch>
git diff main..origin/<branch> -- .github/workflows/webhook-validator-ci.yml
```

La lección fue que una branch no debe evaluarse solo por sus cambios originales; también debe compararse con el estado actual de `main`.

---

## Decisiones técnicas principales

### Aplicación sencilla, pipeline más completo

La lógica de negocio se mantuvo pequeña para dedicar el esfuerzo al ciclo de entrega: pruebas, imagen, pipeline, escaneo, hardening, Kubernetes y troubleshooting.

### `/health` separado de `/ready`

Un proceso puede estar vivo pero no tener la configuración necesaria para recibir tráfico. Separar ambos endpoints representa mejor el estado operacional.

### Alpine después del análisis

La base Alpine no fue elegida únicamente por tamaño. Se probó como respuesta a hallazgos heredados de la imagen base anterior y se volvió a validar el funcionamiento.

### UID/GID numérico

El UID/GID numérico permite que Kubernetes compruebe de forma explícita que el proceso no se ejecuta como root.

### ClusterIP y port-forward

El servicio no se expone públicamente. Para el objetivo local, `ClusterIP` y `kubectl port-forward` reducen el alcance y permiten validar la aplicación sin agregar un ingress o load balancer.

---

## Limitaciones y elementos fuera de alcance

La versión final no pretende ser una plataforma de webhooks de producción.

No incluye:

- Protección contra replay mediante timestamp o nonce
- Persistencia de eventos
- Colas o procesamiento asíncrono
- Rate limiting
- Autenticación adicional
- Rotación automatizada de secretos
- Gestión de secretos mediante un proveedor externo
- Observabilidad con métricas y trazas distribuidas
- Publicación de la imagen en un registry
- Despliegue público en AWS, Azure o GCP
- Ingress, TLS o dominio público
- Alta disponibilidad multi-nodo

Estos puntos son oportunidades para proyectos futuros, no requisitos incompletos del alcance actual.

---

## Lecciones demostradas

- La validación de una firma depende de los bytes exactos del payload y de un secreto compartido.
- Liveness y readiness resuelven preguntas operacionales diferentes.
- Una imagen que funciona con `docker run` puede fallar bajo políticas de Kubernetes.
- Un escáner identifica riesgo potencial; el ingeniero todavía debe clasificar, remediar, probar y documentar.
- Reducir privilegios debe hacerse sin desactivar controles para evitar errores.
- El CI debe validar comportamiento, empaquetado y arranque, no solo sintaxis.
- Una arquitectura local reproducible puede enseñar conceptos reales sin crear infraestructura cloud innecesaria.

---

## Resumen para entrevista

> Construí una API en FastAPI que valida webhooks mediante HMAC SHA-256. Después implementé un flujo local de entrega segura con Pytest, Docker, un usuario no-root, GitHub Actions, Trivy, smoke tests y Kubernetes con Minikube. Separé liveness y readiness, agregué trazabilidad con request IDs y evité registrar secretos o payloads completos. Durante el proyecto hice triage de vulnerabilidades, migré la imagen base de Debian slim a Alpine y resolví un error real de Kubernetes relacionado con `runAsNonRoot` y un usuario no numérico. Finalmente automaticé el despliegue y la limpieza local con scripts Bash.

---

## Declaración final del proyecto

Webhook Validator SecOps está completo para el alcance definido en esta etapa: una API pequeña con un flujo DevSecOps local, reproducible y documentado desde las pruebas hasta Kubernetes.

La publicación en un registry y el despliegue cloud se excluyeron deliberadamente del cierre. Cualquier continuación se tratará como un proyecto separado con una metodología de aprendizaje más enfocada en evidencia de comprensión.

---

## Licencia

Proyecto personal de aprendizaje y portafolio. El contenido se comparte con fines educativos.
