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

## La aplicación web (frontend)

La app web es una **página única** escrita en **HTML, CSS y JavaScript puro** (sin frameworks ni librerías) que consume la API REST con `fetch`. Sus archivos son:

- `principal/templates/index.html` — estructura de la pantalla.
- `principal/static/css/styles.css` — estilos.
- `principal/static/js/app.js` — lógica del CRUD (los cuatro recursos se describen en el objeto `RECURSOS` y comparten el mismo código).

### Estructura de la pantalla

| Zona de la pantalla | Elemento | Para qué sirve |
|---|---|---|
| Cabecera | Pestañas **Categorías · Platos · Zonas · Mesas** | Cambiar de CRUD sin recargar la página |
| Mensajes | Caja de avisos (verde = éxito, roja = error) | Confirmar operaciones o mostrar errores de la API |
| Formulario | Campos del recurso seleccionado | Crear y editar registros |
| Barra de la tabla | Caja de **búsqueda** | Filtrar por texto (envía `?search=`) |
| Tabla | Filas + columna **Acciones** | Ver los registros y botones **Editar** / **Eliminar** |
| Pie de la tabla | Botones **« Anterior** / **Siguiente »** | Navegar entre páginas (10 registros por página) |

### Flujo general de uso

1. Levanta el servidor (`python manage.py runserver`) y abre <http://127.0.0.1:8000/>.
2. Al cargar, la app abre por defecto la pestaña **Categorías**.
3. Rellena el formulario y pulsa **Crear** para añadir un registro (POST). El nuevo registro aparece en la tabla y se muestra un mensaje verde.
4. Usa la **búsqueda** para filtrar y los botones **« Anterior / Siguiente »** para paginar.
5. Pulsa **Editar** en una fila para cargar ese registro en el formulario: el botón cambia a **Actualizar** (PUT) y aparece **Cancelar edición**.
6. Pulsa **Eliminar** en una fila para borrar el registro (DELETE). El navegador pide confirmación antes de continuar.
7. Cambiar de pestaña reinicia el formulario y limpia la búsqueda.

> **Nota técnica:** cada acción hace `fetch` a la API y recarga la tabla. Los errores de validación del backend se traducen a texto y se muestran en la caja de mensajes.

### Flujo de uso por CRUD

#### 1. Categorías

**Pestaña:** `Categorías` · **Endpoint:** `/api/categorias/`

**Columnas de la tabla:** ID, Nombre, Descripción, Activa.

**Formulario (crear/editar):**

| Campo | Tipo | Notas |
|---|---|---|
| Nombre | texto | Obligatorio y único |
| Descripción | área de texto | Opcional |
| Activa | casilla | Marcada por defecto |

**Flujo:** rellena el nombre → **Crear**. Para cambiar el nombre o activarla/desactivarla, pulsa **Editar**, ajusta y **Actualizar**. Para borrarla, pulsa **Eliminar**.

**Al eliminar:** si la categoría tiene **Platos** asociados, el borrado se bloquea y se muestra el aviso *"El registro está relacionado con N platos; elimínalos o reasígnalos primero."*

#### 2. Platos

**Pestaña:** `Platos` · **Endpoint:** `/api/platos/`

**Columnas de la tabla:** ID, Nombre, Categoría, Precio, Estado, Destacado.

**Formulario (crear/editar):**

| Campo | Tipo | Notas |
|---|---|---|
| Nombre | texto | Obligatorio y único |
| Descripción | área de texto | Opcional |
| Categoría | lista desplegable | Obligatoria; se carga desde `/api/categorias/` |
| Precio | número | Obligatorio y mayor que 0 |
| Precio costo | número | Opcional; no puede superar el precio de venta |
| Tiempo preparación (min) | número | Por defecto 15 |
| Calorías | número | Opcional |
| Vegetariano | casilla | Opcional |
| Picante | casilla | Opcional |
| Estado | lista desplegable | Disponible / Agotado / Descontinuado |
| Destacado | casilla | Opcional |

**Flujo:** elige la categoría, completa nombre y precio → **Crear**. **Editar** permite cambiar cualquier campo; **Eliminar** borra el plato.

**Al eliminar:** se borra directamente, sin bloqueos (el plato no tiene dependencias).

#### 3. Zonas

**Pestaña:** `Zonas` · **Endpoint:** `/api/zonas/`

**Columnas de la tabla:** ID, Nombre, Descripción, Activa.

**Formulario (crear/editar):**

| Campo | Tipo | Notas |
|---|---|---|
| Nombre | texto | Obligatorio y único |
| Descripción | área de texto | Opcional |
| Activa | casilla | Marcada por defecto |

**Flujo:** igual que Categorías. Se crea, edita y elimina desde la misma pestaña.

**Al eliminar:** si la zona tiene **Mesas** asociadas, el borrado se bloquea y se muestra el aviso *"El registro está relacionado con N mesas; elimínalos o reasígnalos primero."*

#### 4. Mesas

**Pestaña:** `Mesas` · **Endpoint:** `/api/mesas/`

**Columnas de la tabla:** ID, Número, Zona, Capacidad, Estado, Activa.

**Formulario (crear/editar):**

| Campo | Tipo | Notas |
|---|---|---|
| Número | número | Obligatorio y único |
| Zona | lista desplegable | Obligatoria; se carga desde `/api/zonas/` |
| Capacidad (personas) | número | Obligatoria; por defecto 2 |
| Estado | lista desplegable | Disponible / Ocupada / Reservada / En mantenimiento |
| Activa | casilla | Marcada por defecto |
| Descripción | área de texto | Opcional |

**Flujo:** elige la zona, indica número y capacidad → **Crear**. **Editar** recarga la mesa en el formulario (incluida su zona) para actualizarla. **Eliminar** borra la mesa.

**Al eliminar:** la mesa no tiene dependencias actualmente, así que se elimina directamente.

### Reglas y mensajes de la API que verás en la app

- **Errores de validación:** aparecen en rojo, por ejemplo `precio: El precio debe ser mayor a cero.`
- **Campos obligatorios:** el navegador los exige antes de enviar el formulario.
- **Borrado protegido:** cuando un registro está en uso por otro (Categoría con Platos, Zona con Mesas), la API responde `400` con un mensaje claro en lugar de un error 500, y la app lo muestra en la caja de mensajes.
- **Imagen del plato:** el modelo `Plato` admite una imagen, pero el formulario de la app no la incluye; se puede subir desde `/admin/` o Swagger.

---

## Relación entre modelos

- `Plato` tiene una **ForeignKey** hacia `Categoria`.
- `Mesa` tiene una **ForeignKey** hacia `Zona`.
- `Pedido` (recurso del compañero) se relaciona con `Mesa` y `Plato`.

Las dos ForeignKeys usan `on_delete=PROTECT`, por lo que **no se puede borrar** una
Categoría que tenga Platos ni una Zona que tenga Mesas: la API responde `400`
con un mensaje claro y la app lo muestra. Primero hay que borrar o reasignar
esos Platos/Mesas.

---

## Pruebas

```bash
cd principal
python manage.py test
```

Incluye pruebas del CRUD de Mesas y Categorías: listar, crear y las reglas de
eliminación (una Zona con Mesas o una Categoría con Platos no se borran y
responden `400` con un mensaje claro).
