# EducaTYCs Backend

API para agregar oportunidades educativas gratuitas relevantes para Yucatán, México.

Proyecto de servicio social que recopila cursos, talleres y becas de múltiples fuentes públicas.

## Quick Start

```bash
# 1. Activar entorno virtual
source .venv/bin/activate

# 2. Iniciar servidor (incluye scheduler automático)
uvicorn app.main:app --reload

# 3. Ver documentación interactiva
open http://localhost:8000/docs
```

**Datos cargados:** 1,679+ cursos gratuitos de 8 fuentes.
**Actualización automática:** Cada 6 horas (configurable).

---

## Estado Actual

### ✅ Implementado

#### Arquitectura
- **FastAPI** como framework web
- **PostgreSQL + SQLAlchemy** para persistencia de datos en producción
- **SQLite** solo como origen opcional de migracion local
- **Playwright** (sync) para web scraping
- **Pydantic** para validación de datos
- **APScheduler** para actualización automática en background
- Configuración centralizada por `.env` con `pydantic-settings`
- Logging estructurado para startup/shutdown y eventos de rate limiting
- Estructura de carpetas limpia y mantenible

#### Base de Datos
- PostgreSQL recomendado para desarrollo compartido y produccion
- Modelo `OpportunityModel` con campos completos
- Deduplicación por URL (no se duplican cursos)
- Timestamps automáticos (created_at, updated_at)
- Campo `is_active` para soft delete
- Conexión configurable con `DATABASE_URL` (toma valor desde `.env`)
- Script de migracion desde SQLite: `scripts/migrate_sqlite_to_postgres.py`

#### Scheduler (Background Jobs)
- Actualización automática cada 6 horas (configurable)
- No bloquea la API mientras ejecuta
- Endpoints para monitorear y disparar manualmente

#### Scrapers Funcionales

| Scraper | Fuente | Cursos | Estado |
|---------|--------|--------|--------|
| `capacitate` | Capacítate para el Empleo (Fundación Slim) | ~43 | ✅ Funcional |
| `google` | Google Actívate/Grow | ~38 | ✅ Funcional |
| `conecta_empleo` | Conecta Empleo (Fundación Telefónica) | ~53 | ✅ Funcional |
| `edx` | edX cursos en español | ~4 | ✅ Funcional |
| `coursera` | Coursera cursos gratuitos | ~10 | ✅ Funcional |
| `khan` | Khan Academy español | ~1325 | ✅ Funcional (cargado) |
| `santander` | Santander Open Academy | ~50 | ✅ Funcional |
| `unam` | UNAM MOOC | ~156 | ✅ Funcional |

**No disponibles (protección anti-bot):**
- Aprende.mx (Cloudflare)
- Platzi (JS pesado)
- Becas Benito Juárez (Cloudflare)

#### Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/opportunities/` | Lista desde BD (con filtros) |
| GET | `/opportunities/{id}` | Obtener un curso por ID |
| POST | `/opportunities/` | Crear oportunidad manual (`X-Admin-Key`) |
| PATCH | `/opportunities/{id}` | Actualizar oportunidad (`X-Admin-Key`) |
| DELETE | `/opportunities/{id}` | Eliminar oportunidad (hard delete, `X-Admin-Key`) |
| POST | `/opportunities/refresh` | Scraping manual, bloquea hasta completar (`X-Admin-Key`) |
| POST | `/opportunities/refresh-async` | Scraping en background, retorna inmediatamente (`X-Admin-Key`) |
| GET | `/opportunities/sources` | Lista fuentes disponibles y sus conteos |
| GET | `/opportunities/stats` | Estadísticas de la base de datos |
| GET | `/opportunities/scheduler` | Estado del scheduler automático |

#### Filtros Implementados

```bash
GET /opportunities/?source=capacitate
GET /opportunities/?search=marketing
GET /opportunities/?is_free=true
GET /opportunities/?opportunity_type=course
GET /opportunities/?tag=santander
GET /opportunities/?limit=20&offset=40
```

**Nota de respuesta:** `GET /opportunities/` y `GET /opportunities/{id}` incluyen `id` de la oportunidad.

#### Rate Limiting
- Límite configurable por `RATE_LIMIT_PER_MINUTE`
- Ventana configurable por `RATE_LIMIT_WINDOW_SECONDS`
- Limpieza automática de contadores expirados en memoria

#### Seguridad y Errores
- CRUD manual y endpoints de refresh protegidos con header `X-Admin-Key`
- `ADMIN_API_KEY` obligatorio para habilitar operaciones de escritura y scraping
- Manejo global de excepciones no controladas con respuesta `500` estable

---

## 🔧 EN PROGRESO - Continuar desde aquí

### Scraper Santander (necesita arreglo)

**Archivo:** `app/scrapers/santander.py`

**Problema:** El scraper no extrae correctamente los títulos de los cursos. La página usa cards con estructura compleja.

**Lo que se intentó:**
1. Buscar links con `a[href*="/courses/"]`
2. Extraer títulos de `h3, h4, h2` dentro del link
3. Los títulos vienen genéricos ("Curso Santander")

**Pasos para arreglar:**
1. Explorar la estructura HTML de `https://www.santanderopenacademy.com/es/courses-quick-access.html`
2. Encontrar los selectores correctos para los títulos de cursos
3. Actualizar el método `scrape()` en `santander.py`

**Código actual del scraper:** Ver `app/scrapers/santander.py`

### Scrapers que NO funcionan (protección anti-bot)

| Sitio | URL | Problema |
|-------|-----|----------|
| Becas Benito Juárez | gob.mx/becasbenitojuarez | Cloudflare challenge |
| GOB.MX general | gob.mx/* | Cloudflare challenge |
| Yucatán gobierno | yucatan.gob.mx | Bloqueado |
| SEGEY becas | educacion.yucatan.gob.mx/becas | Página no existe |

### Scrapers potenciales (explorados pero no implementados)

| Sitio | URL | Estado |
|-------|-----|--------|
| SECIHTI (ex-CONAHCYT) | secihti.mx | Página en actualización |
| Platzi gratuitos | platzi.com/cursos-gratis | Requiere JS pesado |

---

## ❌ Pendiente por Implementar

### Prioridad Alta

#### 1. Arreglar scraper Santander
- [x] Explorar HTML de la página de cursos
- [x] Encontrar selectores correctos
- [x] Extraer títulos y descripciones
- [x] Cargar datos a la BD (50 cursos)

#### 2. Cargar datos de Khan Academy
- [x] Ejecutar `POST /opportunities/refresh?source=khan`
- [x] Khan Academy tiene ~1325 cursos disponibles (CARGADOS: 1325)

#### 3. Más Fuentes de Datos
- [x] **UNAM** - Cursos MOOC en Coursera (156 cursos)

### Prioridad Media

#### 4. Filtros Adicionales
- [x] Filtrar por `opportunity_type` (course, scholarship, workshop)
- [x] Filtrar por `tags`

#### 5. Normalización de Datos
- [x] Deduplicar (ya funciona por source_url único)
- [x] Normalizar nombres de proveedores (38 providers normalizados)

### Prioridad Baja

#### 6. Features Adicionales
- [x] Endpoint GET /opportunities/{id}
- [x] CRUD manual: POST/PATCH/DELETE en `/opportunities`
- [x] Variables de entorno (.env)
- [x] CORS configurado (ver notas below)
- [x] Rate limiting
- [x] Docker + docker-compose

#### 7. Pendiente para Frontend
- [ ] Autenticación (JWT/OAuth) - Opcional si los cursos son públicos
- [ ] Conectar Frontend (Flutter/Vue/Nuxt)
- [ ] Desplegar Docker en producción (Gunicorn + Nginx + HTTPS)

---

## Notas de Configuración para Frontend

### CORS
El backend ya tiene CORS configurado. Para conectar un frontend, configura `ALLOWED_ORIGINS` en `.env`:

```bash
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### Autenticación (Opcional)
Si necesitás proteger endpoints, podés agregar:
- JWT con FastAPI
- OAuth2 (Google, Facebook)
- Por ahora los endpoints son públicos

### Despliegue en Produccion
```bash
# Backend + PostgreSQL local con Docker
docker compose up -d
```

Para despliegue en Railway:
- Servicio PostgreSQL administrado
- Servicio backend usando `backend/Dockerfile`
- `DATABASE_URL` apuntando a PostgreSQL
- `ALLOWED_ORIGINS` apuntando al dominio del frontend

---

## Instalación

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env
```

## Uso

```bash
# Iniciar PostgreSQL y backend con Docker
docker compose up -d

# O iniciar solo backend usando una DATABASE_URL existente
uvicorn app.main:app --reload

# Cargar datos de un scraper específico (requiere X-Admin-Key)
curl -X POST "http://localhost:8000/opportunities/refresh?source=khan" \
  -H "X-Admin-Key: TU_ADMIN_API_KEY"

# Ver estadisticas
curl http://localhost:8000/opportunities/stats

# Documentación
open http://localhost:8000/docs
```

Migrar datos desde la base local SQLite:

```bash
SQLITE_DATABASE_URL=sqlite:///educatycs.db \
DATABASE_URL=postgresql+psycopg://educatycs:educatycs@localhost:5432/educatycs \
python scripts/migrate_sqlite_to_postgres.py
```

CRUD manual (admin):

```bash
# Crear
curl -X POST "http://localhost:8000/opportunities/" \
  -H "X-Admin-Key: TU_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Curso manual","opportunity_type":"course","provider":"Admin","source_url":"https://example.com/manual-1"}'

# Actualizar
curl -X PATCH "http://localhost:8000/opportunities/1" \
  -H "X-Admin-Key: TU_ADMIN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Curso manual actualizado"}'

# Eliminar
curl -X DELETE "http://localhost:8000/opportunities/1" \
  -H "X-Admin-Key: TU_ADMIN_API_KEY"
```

## Tests

Suite smoke de API (sin scraper real):

```bash
pytest -q tests
```

Cobertura básica:
- `GET /health`
- `GET /docs`
- `GET /opportunities/` con filtros
- `GET /opportunities/{id}`
- `POST /opportunities/`
- `PATCH /opportunities/{id}`
- `DELETE /opportunities/{id}`
- `GET /opportunities/stats`
- `GET /opportunities/sources`
- `GET /opportunities/scheduler`
- Validación de error para `POST /opportunities/refresh` con source inválido
- Comportamiento de rate limiting (429 + reset de ventana)

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point + lifecycle
│   ├── database.py          # SQLite + SQLAlchemy
│   ├── scheduler.py         # APScheduler
│   ├── models/
│   │   └── opportunity.py   # Modelo SQLAlchemy
│   ├── schemas/
│   │   └── opportunity.py   # Modelos Pydantic
│   ├── scrapers/
│   │   ├── base.py          # Clase base
│   │   ├── capacitate.py    # ✅ Fundación Slim
│   │   ├── google_activate.py # ✅ Google
│   │   ├── conecta_empleo.py  # ✅ Telefónica
│   │   ├── edx_spanish.py     # ✅ edX
│   │   ├── coursera.py        # ✅ Coursera
│   │   ├── khan_academy.py    # ✅ Khan Academy
│   │   └── santander.py       # ⚠️ Necesita arreglo
│   └── routers/
│       └── opportunities.py
├── educatycs.db
├── requirements.txt
└── README.md
```

## Agregar un Nuevo Scraper

1. Crear `app/scrapers/mi_scraper.py`:

```python
import logging
from app.schemas import Opportunity, OpportunityType
from .base import BaseScraper

logger = logging.getLogger(__name__)

class MiScraper(BaseScraper):
    BASE_URL = "https://ejemplo.com"
    source_name = "Mi Fuente"

    def scrape(self) -> list[Opportunity]:
        opportunities = []
        page = self.new_page()
        try:
            page.goto(self.BASE_URL, wait_until="networkidle")
            # ... lógica de extracción ...
        finally:
            page.close()
        return opportunities
```

2. Registrar en `app/scrapers/__init__.py`
3. Agregar a `SCRAPERS` en `app/routers/opportunities.py`
4. Agregar a `SCRAPERS` en `app/scheduler.py`

---

## Configuración

### Variables de Entorno

Copia `.env.example` a `.env` y configura:

```bash
# Database
DATABASE_URL=sqlite:///educatycs.db

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=true

# CORS (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_WINDOW_SECONDS=60

# Scheduler
SCHEDULER_INTERVAL_HOURS=6

# Admin
ADMIN_API_KEY=change-this-admin-key
```

---

## Docker

### Construir y ejecutar

```bash
# Con docker-compose (recomendado)
docker-compose up -d

# O solo Docker
docker build -t educatycs .
docker run -p 8000:8000 -v ./educatycs.db:/app/educatycs.db educatycs
```

### Variables de entorno en Docker

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - DATABASE_URL=sqlite:///educatycs.db
      - SCHEDULER_ENABLED=true
      - SCHEDULER_INTERVAL_HOURS=6
```

---

## Tech Stack

- Python 3.11+
- FastAPI 0.129+
- SQLAlchemy 2.0+
- SQLite
- APScheduler 3.11+
- Playwright 1.58+
- Pydantic 2.12+

---

## Notas para Continuar el Desarrollo

## Cambios Recientes

| Fecha | Cambio | Detalle |
|-------|--------|---------|
| 2026-02-20 | Configuración DB por `.env` | `app/database.py` ahora usa `DATABASE_URL` desde settings. |
| 2026-02-20 | Rate limiting mejorado | Se agregó `RATE_LIMIT_WINDOW_SECONDS` y limpieza de contadores expirados. |
| 2026-02-20 | Seguridad CRUD admin | CRUD manual ahora requiere `X-Admin-Key` con `ADMIN_API_KEY`. |
| 2026-02-20 | Logging | Logs estructurados en startup/shutdown y eventos de `429`. |
| 2026-02-20 | Manejo global de errores | Excepciones no controladas ahora responden `500` estable con logging. |
| 2026-02-20 | CRUD manual | Nuevos endpoints `POST /opportunities/`, `PATCH /opportunities/{id}` y `DELETE /opportunities/{id}`. |
| 2026-02-20 | Respuestas con `id` | `GET /opportunities/` y `GET /opportunities/{id}` ahora incluyen `id` en el schema de salida. |
| 2026-02-20 | Tests smoke API | Se agregaron `tests/conftest.py` y `tests/test_api_smoke.py`. |
| 2026-02-20 | Limpieza de scrapers | Se retiró `aprende_mx` para mantener estabilidad. |

**Contexto:**
1. Proyecto de servicio social - priorizar simplicidad
2. Sin microservicios - todo en un backend
3. Sin auth compleja
4. Playwright sync (no async)
5. Scrapers heredan de `BaseScraper` con context manager

**Estado actual:**
- 8 scrapers funcionando (Khan, UNAM, Santander, Capacitate, Google, Conecta Empleo, Coursera, edX)
- 1,679 cursos en la base de datos
- 20 providers únicos
- Filtros completos (source, search, is_free, opportunity_type, tags)
- CRUD manual disponible para oportunidades (`POST/PATCH/DELETE`)
- Respuestas de oportunidades con `id` incluido
- API lista para frontend
- Docker configurado

**Siguiente paso sugerido:**
1. ~~Arreglar `app/scrapers/santander.py` explorando el HTML~~ ✅
2. ~~Cargar Khan Academy~~ ✅
3. ~~Cargar UNAM~~ ✅
4. ~~Agregar filtros adicionales~~ ✅
5. ~~Docker + Variables de entorno~~ ✅
6. Conectar Frontend (Flutter/Vue/Nuxt)
7. Desplegar en producción
