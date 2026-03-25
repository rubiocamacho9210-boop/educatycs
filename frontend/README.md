# EducaTYCs Frontend

Plataforma web para descubrir oportunidades educativas gratuitas en línea para hispanohablantes de todo el mundo.
Enfoque actual: **app pública de consulta** para que cualquier persona explore cursos, becas y talleres formativos.

## Actualizaciones recientes

- [x] `layouts/default.vue` actualizado con navegación completa:
  - `Digital` (`/`)
  - `Acerca de` (`/acerca-de`)
  - `Beneficiarios` (`/beneficiarios`)
  - `Panel administrativo` (`/panel-admin`)
- [x] Nuevo componente `components/HeroCarousel.vue` basado en `base.pen`
- [x] Nuevas páginas:
  - `pages/acerca-de.vue`
  - `pages/beneficiarios.vue`
  - `pages/panel-admin.vue`
- [x] `pages/index.vue` actualizado para incluir `HeroCarousel` manteniendo filtros, grid y paginación del MVP
- [x] Validación de build: `npm run build` exitoso

## Tech Stack

### Web (Primera iteración)
- **Nuxt 3** (SSR + TypeScript)
- TypeScript

### Mobile (Próxima iteración)
- **Flutter**

---

## Tareas por Prioridad

## Plan de Entrega (7 días)

### Día 1 - Setup y base técnica
- [x] Inicializar Nuxt 3 + TypeScript
- [x] Configurar `.env` con `NUXT_PUBLIC_API_BASE`
- [x] Configurar `runtimeConfig` en `nuxt.config.ts`
- [x] Crear tipos TypeScript (`types/opportunity.ts`)
- [x] Crear composable base de API (`composables/useOpportunities.ts`)
- [x] Crear `tailwind.config.js` con tokens de color semánticos
- [x] Diseñar y refinar cards HTML de oportunidades (`card-1.html` … `card-6.html`)

Nota: en este entorno se dejó scaffold manual equivalente de Nuxt por restricción de red; al ejecutar `npm install` en local quedará listo para correr.

### Día 2 - Home/Listado MVP
- [x] Construir `pages/index.vue` con listado (`GET /opportunities/`)
- [x] Mostrar cards con: título, proveedor, tags y botón de detalle
- [x] Implementar estados: loading, error y empty
- [x] Implementar paginación inicial (`limit`, `offset`)

### Día 3 - Filtros y búsqueda
- [x] Filtro por `source`
- [x] Filtro por `opportunity_type`
- [x] Filtro por `tag`
- [x] Búsqueda por texto (`search`)
- [x] Sincronizar filtros con query params de URL

### Día 4 - Detalle de curso
- [x] Crear ruta dinámica `pages/curso/[id].vue`
- [x] Consumir `GET /opportunities/{id}`
- [x] Mostrar información completa del curso
- [x] Agregar CTA a `source_url` (abrir en nueva pestaña)
- [x] Manejar `404` de forma amigable

### Día 5 - UI/UX y responsive
- [x] Optimizar layout para móvil y desktop
- [x] Mejorar tipografía, espaciados y jerarquía visual
- [x] Pulir componentes de filtro y card
- [x] Validar accesibilidad básica (contraste, foco, labels)

### Día 6 - Deploy
- [ ] Deploy en Vercel/Netlify
- [ ] Configurar variable de entorno de API en producción
- [ ] Verificar CORS backend con dominio final
- [ ] Ejecutar smoke test manual post-deploy

### Día 7 - Cierre de entrega
- [ ] Corregir bugs encontrados
- [ ] Limpiar README y dejar instrucciones finales de ejecución
- [ ] Preparar demo (capturas o video corto)
- [ ] Validar flujo completo antes de entregar

### 🎯 PRIORIDAD ALTA - MVP Web

#### 1. Configuración del Proyecto
- [x] Inicializar proyecto Nuxt 3
- [x] Configurar TypeScript
- [x] Integrar TailwindCSS con `tailwind.config.js` y tokens de color personalizados
- [x] Configurar variables de entorno para API

#### 2. Conexión con Backend
- [x] Crear cliente API base (useFetch de Nuxt en composable)
- [ ] Configurar CORS en backend (si es necesario)
- [ ] Probar endpoints:
  - `GET /opportunities/` - Listar cursos
  - `GET /opportunities/{id}` - Ver detalle
  - `GET /opportunities/sources` - Fuentes disponibles
  - `GET /opportunities/stats` - Estadísticas
  - (Opcional admin) `POST/PATCH/DELETE /opportunities` con `X-Admin-Key`

#### 3. Pantallas Principales
- [x] **Home/Listado**: Grid de cursos con paginación
- [x] **Detalle del curso**: Información completa + link externo
- [x] **Filtros**: Barra de filtros (search, type) con sync de URL
- [x] **Barra de búsqueda**: Search input

#### 4. UI/UX Básico
- [x] Diseño responsive (móvil + desktop)
- [x] Loading states (`components/AppLoading.vue`)
- [x] Error handling (`components/AppError.vue`)
- [x] Cards de cursos con: título, provider, descripción, badge gratuito, tags, botón

---

### 🔷 PRIORIDAD MEDIA - Mejoras Web

#### 5. Funcionalidades Extras
- [ ] **Infinite scroll** o paginación infinita
- [ ] **Favoritos guardados** (localStorage)
- [ ] **Compartir** cursos (copy link, social)
- [ ] **Filtrado en tiempo real** (computed properties)

#### 6. SEO y Performance
- [ ] Meta tags dinámicos
- [ ] Open Graph images
- [ ] Optimizar imágenes
- [ ] PWA support (Service Worker)

#### 7. UI/UX Avanzado
- [ ] Dark mode
- [ ] Skeleton loaders
- [ ] Animaciones suaves
- [ ] Notificaciones toast

---

### 🎯 PRIORIDAD BAJA - Optimizaciones

#### 8. Autenticación (Opcional)
- [ ] Login/Registro de usuarios
- [ ] Guardar favoritos en servidor (si más adelante se agrega auth en backend)
- [ ] Historial de cursos vistos

#### 9. Analytics
- [ ] Google Analytics o Plausible
- [ ] Trackear: filtros usados, cursos clicks, tiempo en página

---

## 📱 MOBILE - Próxima Iteración (Flutter)

### Fase 1: Setup
- [ ] Crear proyecto Flutter
- [ ] Conectar con API REST

### Fase 2: Features Mobile
- [ ] Lista de cursos con pull-to-refresh
- [ ] Filtros (bottom sheet)
- [ ] Detalle del curso
- [ ] Abrir link externo en navegador

### Fase 3: Native Features
- [ ] Notificaciones push (cuando haya nuevos cursos)
- [ ] Compartir cursos
- [ ] Guardar favoritos offline

---

## API Reference

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/opportunities/` | Lista de cursos |
| GET | `/opportunities/{id}` | Detalle de curso |
| GET | `/opportunities/sources` | Fuentes disponibles |
| GET | `/opportunities/total` | Total de oportunidades (con filtros) |
| GET | `/opportunities/stats` | Estadísticas |
| POST | `/opportunities/refresh` | Actualizar datos (requiere `X-Admin-Key`) |
| POST | `/opportunities/refresh-async` | Actualizar datos en background (requiere `X-Admin-Key`) |
| POST | `/opportunities/` | Crear oportunidad manual (requiere `X-Admin-Key`) |
| PATCH | `/opportunities/{id}` | Actualizar oportunidad (admin con `X-Admin-Key`) |
| DELETE | `/opportunities/{id}` | Eliminar oportunidad (admin con `X-Admin-Key`) |

### Query Params

```bash
# Listar con filtros
GET /opportunities/?source=khan
GET /opportunities/?search=python
GET /opportunities/?opportunity_type=course
GET /opportunities/?tag=programacion
GET /opportunities/?limit=20&offset=0
```

### Respuesta de Ejemplo

```json
{
  "id": 123,
  "title": "Introducción a Python",
  "description": "Curso básico de programación",
  "opportunity_type": "course",
  "provider": "Coursera",
  "source": "coursera",
  "source_url": "https://coursera.org/learn/python",
  "location": "Online",
  "is_free": true,
  "tags": ["programación", "python"]
}
```

## Panel Administrativo

El panel administrativo **no aparece en la navegación pública** por seguridad, pero sigue disponible para uso interno.

### Acceso

Navega directamente a:

```
http://localhost:3000/panel-admin        ← desarrollo
https://tu-dominio.com/panel-admin       ← producción
```

No se requiere login en el frontend — el panel es una interfaz gráfica que llama a los endpoints protegidos del backend usando la `X-Admin-Key` configurada en el servidor.

### ¿Qué permite hacer?

- Disparar la actualización del catálogo (`POST /opportunities/refresh`)
- Ver el estado del scheduler automático
- Crear, editar o desactivar oportunidades manualmente

### Seguridad

- El enlace no está indexado ni aparece en el menú público
- Las operaciones de escritura requieren la `X-Admin-Key` en el backend
- Se recomienda restringir el acceso por IP en producción si el servidor lo permite

---

## Política de Acceso (Frontend Público)

- La app web es pública para consulta.
- Usuarios finales consumen endpoints `GET` (listado, detalle, fuentes, total).
- Endpoints de mantenimiento/admin (`POST/PATCH/DELETE /opportunities` y `POST /opportunities/refresh`) solo se usan desde el panel administrativo con `X-Admin-Key`.

---

## Tokens de Color (Tailwind)

Definidos en `tailwind.config.js` para evitar valores hex hardcodeados:

| Token | Hex | Uso |
|-------|-----|-----|
| `brand` | `#1A73E8` | Botón primario, foco |
| `brand-dark` | `#1558B0` | Hover del botón |
| `border` | `#D7DCE3` | Bordes de cards y tags |
| `surface` | `#EEF2F7` | Fondo de badges de tipo |
| `ink` | `#1F2937` | Texto principal |
| `ink-muted` | `#6B7280` | Texto secundario / metadatos |

---

## Arquitectura Sugerida (Nuxt 3)

```
frontend/
├── app.vue              # Entrada de la app (NuxtLayout + NuxtPage)
├── tailwind.config.js   # Tokens de color y configuración de Tailwind
├── layouts/
│   └── default.vue      # Shell: nav principal + footer
├── pages/
│   ├── index.vue        # Home / Listado
│   ├── acerca-de.vue    # Página institucional del proyecto
│   ├── beneficiarios.vue # Instituciones beneficiarias
│   ├── panel-admin.vue  # Acceso administrativo (UI)
│   ├── curso/
│   │   └── [id].vue    # Detalle del curso
├── components/
│   ├── OpportunityCard.vue  # Card de oportunidad
│   ├── FilterBar.vue        # Barra de filtros (search, tipo, fuente, limpiar)
│   ├── HeroCarousel.vue     # Carrusel principal (home y páginas informativas)
│   ├── AppLoading.vue       # Spinner de carga
│   └── AppError.vue         # Mensaje de error
├── composables/
│   ├── useOpportunities.ts       # Fetch de listado con filtros
│   ├── useOpportunitiesTotal.ts  # Fetch del total de oportunidades (paginación)
│   ├── useSources.ts             # Fetch de fuentes disponibles
│   └── useAnalytics.ts           # Inicialización de Google Analytics 4
├── utils/
│   └── filters.ts           # Funciones puras de filtrado (testeable)
├── tests/
│   └── filters.test.ts      # Unit tests con Vitest
├── types/
│   └── opportunity.ts       # Tipos TypeScript
├── stubs/
│   └── app-manifest-stub.mjs  # Stub para deshabilitar app manifest de Nuxt
├── vitest.config.ts         # Configuración de Vitest
└── .env                     # Variables de entorno
```

---

## Estado Actual del Backend

- **URL**: `http://localhost:8000` (desarrollo)
- **Cursos**: 1,679+
- **Fuentes**: 8 scrapers
- **Documentación**: `/docs` (Swagger)
- **Lectura pública**: `GET /opportunities*`, `GET /sources`, `GET /stats`
- **Admin protegido**: CRUD manual con `X-Admin-Key`

---

## Próximos Pasos

1. ✅ Backend listo
2. ✅ Frontend Nuxt 3 inicializado
3. ✅ Conexión API (listado, detalle, fuentes)
4. ✅ UI de listado + filtros + detalle
5. ✅ Navegación y páginas institucionales base
6. ⏳ Deploy web
7. ⏳ App Flutter (próxima iteración)

---

## Recursos

- [Nuxt 3 Docs](https://nuxt.com/docs)
- [Vue 3 Docs](https://vuejs.org/guide/)
- [Flutter Docs](https://docs.flutter.dev/)
- [TailwindCSS](https://tailwindcss.com/) (opcional)

## Comandos rápidos

```bash
npm install
npm run dev
npm run test        # corre los tests una vez
npm run test:watch  # modo watch para desarrollo
```
