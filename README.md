# Restaurante · App Web con Django REST Framework

Proyecto del **Parcial 2.º corte — Desarrollo de Aplicaciones Web**.
Tema elegido: **Restaurante**, con tres CRUDs relacionados (uno por integrante):

| Recurso | App / carpeta | Integrante |
|---|---|---|
| **Platos** (+ Categorías) | `principal/Platos` | Kevin |
| **Mesas** (+ Zonas) | `principal/Mesas` | Kevin |
| Pedidos | — | (compañero del grupo) |

Backend con **Django + Django REST Framework** y un **frontend en HTML, CSS y JavaScript puro (sin frameworks)** que consume la API local.

---

## Tecnologías

- Python 3.14
- Django 6.1.2
- Django REST Framework 3.18.3
- drf-yasg (documentación Swagger / ReDoc)
- SQLite (base de datos por defecto)
- Frontend: HTML, CSS y JavaScript vanilla (sin frameworks)

---

## Estructura del proyecto

```
AppWeb_Restaurante_CRUDs/
├── principal/                 # Proyecto Django
│   ├── manage.py
│   ├── db.sqlite3             # Base de datos (incluye datos de ejemplo)
│   ├── principal/             # Configuración global (settings, urls)
│   ├── Platos/                # CRUD de Platos y Categorías
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── migrations/
│   │   └── api/               # serializers.py + router.py
│   ├── Mesas/                 # CRUD de Mesas y Zonas
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── migrations/
│   │   └── api/               # serializers.py + router.py
│   ├── templates/index.html   # Frontend
│   └── static/
│       ├── css/styles.css
│       └── js/app.js
├── requirements.txt
└── README.md
```

---

## Cómo ejecutar el proyecto

1. **Clonar el repositorio** e ingresar a la carpeta.

2. **Crear el entorno virtual e instalarlo** (Windows):

   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```

   En Linux / macOS:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar las migraciones** (crea/actualiza las tablas):

   ```bash
   cd principal
   python manage.py migrate
   ```

5. **Levantar el servidor de desarrollo:**

   ```bash
   python manage.py runserver
   ```

6. **Abrir en el navegador:**

   - Frontend (tablas + formularios): <http://127.0.0.1:8000/>
   - Documentación Swagger: <http://127.0.0.1:8000/swagger/>
   - Documentación ReDoc: <http://127.0.0.1:8000/redoc/>

> El archivo `db.sqlite3` ya incluye datos de ejemplo (Categorías, Platos, Zonas y Mesas)
> para que las tablas se vean pobladas al abrir el frontend.

---

## Endpoints de la API

| Recurso | URL |
|---|---|
| Categorías | `/api/categorias/` |
| Platos | `/api/platos/` |
| Zonas | `/api/zonas/` |
| Mesas | `/api/mesas/` |

Cada recurso soporta el CRUD completo mediante `DefaultRouter`:

- `GET /api/mesas/` — listar
- `POST /api/mesas/` — crear
- `GET /api/mesas/{id}/` — detalle
- `PUT /api/mesas/{id}/` — actualizar
- `PATCH /api/mesas/{id}/` — actualización parcial
- `DELETE /api/mesas/{id}/` — eliminar

Acciones adicionales:

- `GET /api/mesas/disponibles/` y `GET /api/platos/destacados/`
- `PATCH /api/mesas/{id}/cambiar_estado/` y `PATCH /api/platos/{id}/cambiar_estado/`

Estas rutas se pueden explorar y probar desde **Swagger** (`/swagger/`).

---

## Funcionalidad del frontend

El frontend (`index.html` + `app.js`) consume la API y permite:

- **GET:** mostrar cada recurso en una tabla (Categorías, Platos, Zonas, Mesas).
- **POST:** crear registros desde un formulario; el nuevo registro aparece en la tabla.
- **PUT (bonus):** editar un registro existente con el botón *Editar*.
- **DELETE (bonus):** eliminar un registro con el botón *Eliminar*.
- Buscador y paginación usando los parámetros que ofrece DRF (`?search=`).

No usa librerías ni frameworks externos: solo `fetch` de JavaScript.

---

## Relación entre modelos

- `Plato` tiene una **ForeignKey** hacia `Categoria`.
- `Mesa` tiene una **ForeignKey** hacia `Zona`.
- `Pedido` (recurso del compañero) se relaciona con `Mesa` y `Plato`.

---

## Pruebas

```bash
cd principal
python manage.py test
```

Incluye pruebas básicas del CRUD de Mesas (listar y crear).
