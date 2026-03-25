# Deploy en Railway

Esta guia deja el proyecto corriendo con tres servicios en Railway:

- `educatycs-db` (PostgreSQL administrado)
- `educatycs-backend` (FastAPI + Playwright)
- `educatycs-frontend` (Nuxt 3 SSR)

## 1. Preparacion del repo

Sube este repo a GitHub.

Railway va a crear dos servicios desde el mismo repo:

- backend con root directory: `backend`
- frontend con root directory: `frontend`

## 2. Crear el proyecto en Railway

1. Crea un proyecto nuevo en Railway.
2. Agrega una base de datos PostgreSQL.
3. Agrega un servicio desde GitHub para `backend`.
4. Agrega otro servicio desde GitHub para `frontend`.

## 3. Configurar el backend

Servicio: `educatycs-backend`

- Root Directory: `backend`
- Builder: Docker
- Dockerfile: `backend/Dockerfile`

Variables de entorno del backend:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
ALLOWED_ORIGINS=https://TU-FRONTEND.up.railway.app
ADMIN_API_KEY=pon-una-clave-larga-y-segura
DEBUG=false
SCHEDULER_INTERVAL_HOURS=6
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_WINDOW_SECONDS=60
```

Notas:

- Deja una sola replica mientras el scheduler siga corriendo dentro de FastAPI.
- Railway inyecta `PORT` automaticamente; el `Dockerfile` ya lo soporta.

## 4. Configurar el frontend

Servicio: `educatycs-frontend`

- Root Directory: `frontend`
- Builder: Docker
- Dockerfile: `frontend/Dockerfile`

Variables de entorno del frontend:

```env
NUXT_PUBLIC_API_BASE=https://TU-BACKEND.up.railway.app
NUXT_PUBLIC_SITE_URL=https://TU-FRONTEND.up.railway.app
NUXT_PUBLIC_GA_ID=G-MQ6QDH92TV
```

Si todavia no vas a usar Google Analytics, puedes omitir `NUXT_PUBLIC_GA_ID`.

## 5. Conectar frontend y backend

Cuando Railway te asigne dominios:

1. Copia la URL publica del backend.
2. Pegala en `NUXT_PUBLIC_API_BASE` del frontend.
3. Copia la URL publica del frontend.
4. Pegala en `ALLOWED_ORIGINS` del backend.
5. Redepploya ambos servicios si Railway no lo hace automaticamente.

## 6. Migrar datos desde SQLite a PostgreSQL

Si quieres subir el catalogo actual:

1. Arranca PostgreSQL local con Docker:

```bash
cd /Users/gerardorubio/Documents/projects/educatycs/backend
docker compose up -d postgres
```

2. Migra la base SQLite local a PostgreSQL local:

```bash
cd /Users/gerardorubio/Documents/projects/educatycs/backend
SQLITE_DATABASE_URL=sqlite:///educatycs.db \
DATABASE_URL=postgresql+psycopg://educatycs:educatycs@localhost:5432/educatycs \
python scripts/migrate_sqlite_to_postgres.py
```

3. Exporta esos datos al Postgres de Railway o apunta la migracion directo al `DATABASE_URL` de Railway.

Ejemplo directo a Railway:

```bash
cd /Users/gerardorubio/Documents/projects/educatycs/backend
SQLITE_DATABASE_URL=sqlite:///educatycs.db \
DATABASE_URL='postgresql+psycopg://USUARIO:PASSWORD@HOST:PUERTO/DBNAME' \
python scripts/migrate_sqlite_to_postgres.py
```

## 7. Verificaciones

Backend:

```bash
curl https://TU-BACKEND.up.railway.app/health
```

Frontend:

- abre la home
- prueba filtros
- abre un detalle con `Ver mas`
- confirma que carga datos del backend

## 8. Dominio custom

Cuando todo funcione con dominios `up.railway.app`, conecta tu dominio real:

- frontend: `educatycs.mx` o `www.educatycs.mx`
- backend: mejor en subdominio, por ejemplo `api.educatycs.mx`

Luego actualiza:

```env
NUXT_PUBLIC_API_BASE=https://api.educatycs.mx
NUXT_PUBLIC_SITE_URL=https://educatycs.mx
ALLOWED_ORIGINS=https://educatycs.mx,https://www.educatycs.mx
```
