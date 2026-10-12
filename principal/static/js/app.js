/*
 * app.js — Frontend en JavaScript puro (sin frameworks) que consume la API
 * de Django REST Framework del proyecto Restaurante.
 *
 * Implementa el CRUD completo (GET, POST, PUT y DELETE) de cuatro recursos:
 * Categorías, Platos, Zonas y Mesas. La estructura de cada recurso se describe
 * en el objeto RECURSOS y el resto del archivo es código genérico que se
 * reutiliza para todos.
 */

/* -------------------------------------------------------------------------
 * 1. Configuración de los recursos
 *    - columnas: cómo se muestra cada registro en la tabla (GET)
 *    - campos:   qué inputs tiene el formulario (POST / PUT)
 * ---------------------------------------------------------------------- */
const RECURSOS = {
  categorias: {
    titulo: 'Categorías',
    endpoint: '/api/categorias/',
    columnas: [
      { campo: 'id', etiqueta: 'ID' },
      { campo: 'nombre', etiqueta: 'Nombre' },
      { campo: 'descripcion', etiqueta: 'Descripción' },
      { campo: 'activa', etiqueta: 'Activa', tipo: 'bool' },
    ],
    campos: [
      { campo: 'nombre', etiqueta: 'Nombre', tipo: 'text', requerido: true },
      { campo: 'descripcion', etiqueta: 'Descripción', tipo: 'textarea' },
      { campo: 'activa', etiqueta: 'Activa', tipo: 'checkbox', defecto: true },
    ],
  },

  platos: {
    titulo: 'Platos',
    endpoint: '/api/platos/',
    columnas: [
      { campo: 'id', etiqueta: 'ID' },
      { campo: 'nombre', etiqueta: 'Nombre' },
      { campo: 'categoria_nombre', etiqueta: 'Categoría' },
      { campo: 'precio', etiqueta: 'Precio' },
      { campo: 'estado', etiqueta: 'Estado' },
      { campo: 'destacado', etiqueta: 'Destacado', tipo: 'bool' },
    ],
    campos: [
      { campo: 'nombre', etiqueta: 'Nombre', tipo: 'text', requerido: true },
      { campo: 'descripcion', etiqueta: 'Descripción', tipo: 'textarea' },
      { campo: 'categoria', etiqueta: 'Categoría', tipo: 'fk', fuente: '/api/categorias/', textoCampo: 'nombre', requerido: true },
      { campo: 'precio', etiqueta: 'Precio', tipo: 'number', paso: '0.01', requerido: true },
      { campo: 'precio_costo', etiqueta: 'Precio costo', tipo: 'number', paso: '0.01' },
      { campo: 'tiempo_preparacion', etiqueta: 'Tiempo preparación (min)', tipo: 'number', defecto: 15 },
      { campo: 'calorias', etiqueta: 'Calorías', tipo: 'number' },
      { campo: 'es_vegetariano', etiqueta: 'Vegetariano', tipo: 'checkbox' },
      { campo: 'es_picante', etiqueta: 'Picante', tipo: 'checkbox' },
      {
        campo: 'estado', etiqueta: 'Estado', tipo: 'select', defecto: 'DISPONIBLE',
        opciones: [
          { valor: 'DISPONIBLE', texto: 'Disponible' },
          { valor: 'AGOTADO', texto: 'Agotado' },
          { valor: 'DESCONTINUADO', texto: 'Descontinuado' },
        ],
      },
      { campo: 'destacado', etiqueta: 'Destacado', tipo: 'checkbox' },
    ],
  },

  zonas: {
    titulo: 'Zonas',
    endpoint: '/api/zonas/',
    columnas: [
      { campo: 'id', etiqueta: 'ID' },
      { campo: 'nombre', etiqueta: 'Nombre' },
      { campo: 'descripcion', etiqueta: 'Descripción' },
      { campo: 'activa', etiqueta: 'Activa', tipo: 'bool' },
    ],
    campos: [
      { campo: 'nombre', etiqueta: 'Nombre', tipo: 'text', requerido: true },
      { campo: 'descripcion', etiqueta: 'Descripción', tipo: 'textarea' },
      { campo: 'activa', etiqueta: 'Activa', tipo: 'checkbox', defecto: true },
    ],
  },

  mesas: {
    titulo: 'Mesas',
    endpoint: '/api/mesas/',
    columnas: [
      { campo: 'id', etiqueta: 'ID' },
      { campo: 'numero', etiqueta: 'Número' },
      { campo: 'zona_nombre', etiqueta: 'Zona' },
      { campo: 'capacidad', etiqueta: 'Capacidad' },
      { campo: 'estado', etiqueta: 'Estado' },
      { campo: 'activa', etiqueta: 'Activa', tipo: 'bool' },
    ],
    campos: [
      { campo: 'numero', etiqueta: 'Número', tipo: 'number', requerido: true },
      { campo: 'zona', etiqueta: 'Zona', tipo: 'fk', fuente: '/api/zonas/', textoCampo: 'nombre', requerido: true },
      { campo: 'capacidad', etiqueta: 'Capacidad (personas)', tipo: 'number', defecto: 2, requerido: true },
      {
        campo: 'estado', etiqueta: 'Estado', tipo: 'select', defecto: 'DISPONIBLE',
        opciones: [
          { valor: 'DISPONIBLE', texto: 'Disponible' },
          { valor: 'OCUPADA', texto: 'Ocupada' },
          { valor: 'RESERVADA', texto: 'Reservada' },
          { valor: 'MANTENIMIENTO', texto: 'En mantenimiento' },
        ],
      },
      { campo: 'activa', etiqueta: 'Activa', tipo: 'checkbox', defecto: true },
      { campo: 'descripcion', etiqueta: 'Descripción', tipo: 'textarea' },
    ],
  },

  pedidos: {
    titulo: 'Pedidos',
    endpoint: '/api/pedidos/',
    columnas: [
      { campo: 'id', etiqueta: 'ID' },
      { campo: 'zona_nombre', etiqueta: 'Zona' },
      { campo: 'mesa_numero', etiqueta: 'Mesa' },
      { campo: 'categoria_nombre', etiqueta: 'Categoría' },
      { campo: 'plato_nombre', etiqueta: 'Plato' },
      { campo: 'precio_unitario', etiqueta: 'Precio' },
      { campo: 'cantidad', etiqueta: 'Cantidad' },
      { campo: 'total', etiqueta: 'Total' },
      { campo: 'estado', etiqueta: 'Estado' },
    ],
    // Todo se selecciona (nada se escribe) para que el mesero sea rápido.
    // Zona y Categoría solo filtran las listas de Mesa y Plato: no se envían a la API.
    campos: [
      { campo: 'zona', etiqueta: 'Zona', tipo: 'fk', fuente: '/api/zonas/', textoCampo: 'nombre', requerido: true, soloFiltro: true },
      {
        campo: 'mesa', etiqueta: 'Mesa', tipo: 'fk', fuente: '/api/mesas/', dependeDe: 'zona', requerido: true,
        texto: (mesa) => `Mesa ${mesa.numero} (${mesa.capacidad} personas)`,
      },
      { campo: 'categoria', etiqueta: 'Categoría', tipo: 'fk', fuente: '/api/categorias/', textoCampo: 'nombre', requerido: true, soloFiltro: true },
      {
        campo: 'plato', etiqueta: 'Plato', tipo: 'fk', fuente: '/api/platos/?estado=DISPONIBLE', dependeDe: 'categoria', requerido: true,
        texto: (plato) => `${plato.nombre} - $${plato.precio}`,
      },
      {
        campo: 'cantidad', etiqueta: 'Cantidad', tipo: 'select', defecto: '1',
        opciones: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((n) => ({ valor: String(n), texto: String(n) })),
      },
      {
        campo: 'estado', etiqueta: 'Estado', tipo: 'select', defecto: 'PENDIENTE',
        opciones: [
          { valor: 'PENDIENTE', texto: 'Pendiente' },
          { valor: 'EN_PREPARACION', texto: 'En preparación' },
          { valor: 'ENTREGADO', texto: 'Entregado' },
          { valor: 'CANCELADO', texto: 'Cancelado' },
        ],
      },
    ],
  },
};

/* -------------------------------------------------------------------------
 * 2. Estado de la aplicación
 * ---------------------------------------------------------------------- */
let recursoActual = 'categorias';
let editandoId = null;        // null = creando, número = editando ese id
let urlPaginaSiguiente = null;
let urlPaginaAnterior = null;
const cacheFk = {};           // caché de opciones para selects de ForeignKey

/* -------------------------------------------------------------------------
 * 3. Utilidades
 * ---------------------------------------------------------------------- */

// Envuelve fetch: convierte a JSON y lanza un error legible si falla.
async function pedir(url, opciones = {}) {
  const respuesta = await fetch(url, opciones);
  if (respuesta.status === 204) return null; // DELETE no devuelve cuerpo
  const datos = await respuesta.json().catch(() => ({}));
  if (!respuesta.ok) throw new Error(textoDeError(datos, respuesta.status));
  return datos;
}

// Convierte los errores de validación de DRF en un texto entendible.
function textoDeError(datos, status) {
  if (datos && typeof datos === 'object') {
    // Errores generales (por ejemplo, al no poder eliminar por relaciones).
    if (datos.detail) return String(datos.detail);

    const partes = Object.entries(datos).map(([campo, valor]) => {
      const texto = Array.isArray(valor) ? valor.join(', ') : String(valor);
      return `${campo}: ${texto}`;
    });
    if (partes.length) return partes.join(' | ');
  }
  return `Error HTTP ${status}`;
}

// La API está paginada: devuelve {count, next, previous, results}.
function listaDe(datos) {
  if (Array.isArray(datos)) return datos;
  return (datos && datos.results) || [];
}

// Pequeño "debounce" para no llamar a la API en cada tecla del buscador.
function debounce(fn, ms) {
  let t;
  return function (...args) {
    clearTimeout(t);
    t = setTimeout(() => fn.apply(this, args), ms);
  };
}

/* -------------------------------------------------------------------------
 * 4. Render del encabezado y de la tabla (GET)
 * ---------------------------------------------------------------------- */
function renderEncabezados() {
  const recurso = RECURSOS[recursoActual];
  const fila = document.getElementById('encabezados');
  fila.innerHTML = '';
  recurso.columnas.forEach((col) => {
    const th = document.createElement('th');
    th.textContent = col.etiqueta;
    fila.appendChild(th);
  });
  const thAcciones = document.createElement('th');
  thAcciones.textContent = 'Acciones';
  fila.appendChild(thAcciones);
}

function renderTabla(items) {
  const recurso = RECURSOS[recursoActual];
  const tbody = document.getElementById('cuerpo');
  tbody.innerHTML = '';

  if (!items.length) {
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan = recurso.columnas.length + 1;
    td.className = 'vacio';
    td.textContent = 'No hay registros todavía.';
    tr.appendChild(td);
    tbody.appendChild(tr);
    return;
  }

  items.forEach((item) => tbody.appendChild(crearFila(item)));
}

function crearFila(item) {
  const recurso = RECURSOS[recursoActual];
  const tr = document.createElement('tr');

  recurso.columnas.forEach((col) => {
    const td = document.createElement('td');
    const valor = item[col.campo];
    if (col.tipo === 'bool') {
      td.textContent = valor ? 'Sí' : 'No';
    } else {
      td.textContent = (valor === null || valor === undefined || valor === '') ? '—' : valor;
    }
    tr.appendChild(td);
  });

  // Botones de editar (PUT) y eliminar (DELETE)
  const tdAcciones = document.createElement('td');
  tdAcciones.className = 'acciones';

  const btnEditar = document.createElement('button');
  btnEditar.type = 'button';
  btnEditar.className = 'editar';
  btnEditar.textContent = 'Editar';
  btnEditar.onclick = () => editar(item.id);
  tdAcciones.appendChild(btnEditar);

  const btnEliminar = document.createElement('button');
  btnEliminar.type = 'button';
  btnEliminar.className = 'peligro';
  btnEliminar.textContent = 'Eliminar';
  btnEliminar.onclick = () => eliminar(item.id);
  tdAcciones.appendChild(btnEliminar);

  tr.appendChild(tdAcciones);
  return tr;
}

function renderPaginacion() {
  const cont = document.getElementById('paginacion');
  cont.innerHTML = '';
  if (!urlPaginaAnterior && !urlPaginaSiguiente) return;

  const btnPrev = document.createElement('button');
  btnPrev.type = 'button';
  btnPrev.textContent = '« Anterior';
  btnPrev.disabled = !urlPaginaAnterior;
  btnPrev.onclick = () => cargar(urlPaginaAnterior);

  const btnNext = document.createElement('button');
  btnNext.type = 'button';
  btnNext.textContent = 'Siguiente »';
  btnNext.disabled = !urlPaginaSiguiente;
  btnNext.onclick = () => cargar(urlPaginaSiguiente);

  cont.appendChild(btnPrev);
  cont.appendChild(btnNext);
}

/* -------------------------------------------------------------------------
 * 5. Construcción del formulario (POST / PUT)
 * ---------------------------------------------------------------------- */
async function renderFormulario(valores = null) {
  const recurso = RECURSOS[recursoActual];
  const form = document.getElementById('formulario');
  form.innerHTML = '';

  const grid = document.createElement('div');
  grid.className = 'grid';

  for (const campo of recurso.campos) {
    grid.appendChild(await crearCampo(campo, valores));
  }
  form.appendChild(grid);

  // Selects que dependen de otro (ej: Mesa depende de Zona): se llenan
  // según lo elegido en el otro select y se recargan cuando este cambia.
  for (const campo of recurso.campos) {
    if (campo.dependeDe) {
      const padre = document.getElementById(`f-${campo.dependeDe}`);
      const hijo = document.getElementById(`f-${campo.campo}`);
      padre.addEventListener('change', () => llenarSelectFk(hijo, campo));
      await llenarSelectFk(hijo, campo, valores ? valores[campo.campo] : undefined);
    }
  }

  const acciones = document.createElement('div');
  acciones.className = 'acciones-form';

  const btnGuardar = document.createElement('button');
  btnGuardar.type = 'submit';
  btnGuardar.textContent = editandoId ? 'Actualizar' : 'Crear';
  acciones.appendChild(btnGuardar);

  if (editandoId) {
    const btnCancelar = document.createElement('button');
    btnCancelar.type = 'button';
    btnCancelar.className = 'secundario';
    btnCancelar.textContent = 'Cancelar edición';
    btnCancelar.onclick = cancelarEdicion;
    acciones.appendChild(btnCancelar);
  }

  form.appendChild(acciones);
}

async function crearCampo(campo, valores) {
  const valor = valores ? valores[campo.campo] : undefined;
  const wrapper = document.createElement('div');
  wrapper.className = 'campo';

  // Casilla de verificación (checkbox)
  if (campo.tipo === 'checkbox') {
    const label = document.createElement('label');
    label.className = 'checkbox';
    const input = document.createElement('input');
    input.type = 'checkbox';
    input.id = `f-${campo.campo}`;
    input.name = campo.campo;
    input.checked = (valor !== undefined && valor !== null) ? !!valor : !!campo.defecto;
    label.appendChild(input);
    label.appendChild(document.createTextNode(' ' + campo.etiqueta));
    wrapper.appendChild(label);
    return wrapper;
  }

  const label = document.createElement('label');
  label.textContent = campo.etiqueta;
  label.setAttribute('for', `f-${campo.campo}`);
  wrapper.appendChild(label);

  let input;
  if (campo.tipo === 'textarea') {
    input = document.createElement('textarea');
    input.rows = 2;
  } else if (campo.tipo === 'select' || campo.tipo === 'fk') {
    input = document.createElement('select');
  } else {
    input = document.createElement('input');
    input.type = campo.tipo; // text | number
    if (campo.tipo === 'number') {
      input.step = campo.paso || '1';
      input.min = '0';
    }
  }
  input.id = `f-${campo.campo}`;
  input.name = campo.campo;
  if (campo.requerido) input.required = true;
  wrapper.appendChild(input);

  // Rellenar selects (fijos o traídos de la API para las ForeignKey)
  if (campo.tipo === 'select') {
    campo.opciones.forEach((op) => input.add(new Option(op.texto, op.valor)));
    input.value = (valor !== undefined && valor !== null) ? String(valor) : (campo.defecto || '');
  } else if (campo.tipo === 'fk') {
    if (!campo.dependeDe) await llenarSelectFk(input, campo, valor); // los dependientes se llenan en renderFormulario
  } else {
    if (valor !== undefined && valor !== null) {
      input.value = valor;
    } else if (campo.defecto !== undefined) {
      input.value = campo.defecto;
    }
  }

  return wrapper;
}

async function llenarSelectFk(select, campo, valor) {
  try {
    let url = campo.fuente;
    if (campo.dependeDe) {
      // Filtra con lo elegido en el otro select, ej: /api/mesas/?zona=2
      const valorPadre = document.getElementById(`f-${campo.dependeDe}`).value;
      url += (url.includes('?') ? '&' : '?') + `${campo.dependeDe}=${valorPadre}`;
    }
    const datos = cacheFk[url] || await pedir(url);
    if (!campo.dependeDe) cacheFk[url] = datos;
    const opciones = listaDe(datos);
    select.innerHTML = '';
    if (!campo.requerido) select.add(new Option('(ninguna)', ''));
    opciones.forEach((item) => {
      const texto = campo.texto ? campo.texto(item) : item[campo.textoCampo];
      select.add(new Option(texto, item.id));
    });
    if (valor !== undefined && valor !== null) select.value = String(valor);
  } catch (error) {
    select.innerHTML = '';
    select.add(new Option('Error al cargar', ''));
  }
}

// Toma los valores del formulario y arma el JSON para la API.
function recolectarDatos() {
  const recurso = RECURSOS[recursoActual];
  const datos = {};

  recurso.campos.forEach((campo) => {
    if (campo.soloFiltro) return; // Zona y Categoría en Pedidos solo filtran
    const input = document.getElementById(`f-${campo.campo}`);

    if (campo.tipo === 'checkbox') {
      datos[campo.campo] = input.checked;
    } else if (campo.tipo === 'number') {
      const v = input.value.trim();
      if (v !== '') datos[campo.campo] = Number(v); // vacío = se omite y aplica el valor por defecto
    } else if (campo.tipo === 'select' || campo.tipo === 'fk') {
      if (input.value !== '') datos[campo.campo] = input.value;
    } else {
      datos[campo.campo] = input.value;
    }
  });

  return datos;
}

/* -------------------------------------------------------------------------
 * 6. Operaciones del CRUD
 * ---------------------------------------------------------------------- */

// GET: pide la lista (con búsqueda y/o paginación) y la pinta.
async function cargar(url = null) {
  const recurso = RECURSOS[recursoActual];
  const texto = document.getElementById('busqueda').value.trim();
  const destino = url || (texto ? `${recurso.endpoint}?search=${encodeURIComponent(texto)}` : recurso.endpoint);

  try {
    const datos = await pedir(destino);
    urlPaginaSiguiente = datos && datos.next ? datos.next : null;
    urlPaginaAnterior = datos && datos.previous ? datos.previous : null;
    renderTabla(listaDe(datos));
    renderPaginacion();
  } catch (error) {
    mostrarMensaje('No se pudo cargar la lista: ' + error.message, 'error');
  }
}

// POST / PUT: crea o actualiza el registro según se esté editando o no.
async function guardar(evento) {
  evento.preventDefault();
  const recurso = RECURSOS[recursoActual];
  const editando = editandoId !== null;
  const url = editando ? `${recurso.endpoint}${editandoId}/` : recurso.endpoint;

  try {
    await pedir(url, {
      method: editando ? 'PUT' : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(recolectarDatos()),
    });
    mostrarMensaje(editando ? 'Registro actualizado correctamente.' : 'Registro creado correctamente.', 'ok');
    await cancelarEdicion();
    await cargar();
  } catch (error) {
    mostrarMensaje('Error: ' + error.message, 'error');
  }
}

// Carga un registro en el formulario para editarlo.
async function editar(id) {
  const recurso = RECURSOS[recursoActual];
  try {
    const item = await pedir(`${recurso.endpoint}${id}/`);
    editandoId = id;
    await renderFormulario(item);
    document.getElementById('formulario').scrollIntoView({ behavior: 'smooth' });
  } catch (error) {
    mostrarMensaje('No se pudo cargar el registro: ' + error.message, 'error');
  }
}

// DELETE: elimina el registro.
async function eliminar(id) {
  const recurso = RECURSOS[recursoActual];
  if (!confirm('¿Seguro que deseas eliminar este registro?')) return;

  try {
    await pedir(`${recurso.endpoint}${id}/`, { method: 'DELETE' });
    mostrarMensaje('Registro eliminado correctamente.', 'ok');
    if (editandoId === id) await cancelarEdicion();
    await cargar();
  } catch (error) {
    mostrarMensaje('No se pudo eliminar: ' + error.message, 'error');
  }
}

async function cancelarEdicion() {
  editandoId = null;
  await renderFormulario();
}

/* -------------------------------------------------------------------------
 * 7. Navegación entre recursos e inicialización
 * ---------------------------------------------------------------------- */
async function seleccionarRecurso(nombre) {
  recursoActual = nombre;
  editandoId = null;

  document.querySelectorAll('#tabs button').forEach((b) => {
    b.classList.toggle('activo', b.dataset.recurso === nombre);
  });

  const recurso = RECURSOS[nombre];
  document.getElementById('titulo').textContent = 'CRUD de ' + recurso.titulo;
  document.getElementById('busqueda').value = '';

  renderEncabezados();
  await renderFormulario();
  await cargar();
}

function mostrarMensaje(texto, tipo) {
  const caja = document.getElementById('mensaje');
  caja.textContent = texto;
  caja.className = 'mensaje ' + tipo;
  clearTimeout(mostrarMensaje._timer);
  mostrarMensaje._timer = setTimeout(() => {
    caja.className = 'mensaje';
  }, 5000);
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('#tabs button').forEach((b) => {
    b.onclick = () => seleccionarRecurso(b.dataset.recurso);
  });
  document.getElementById('busqueda').addEventListener('input', debounce(() => cargar(), 400));
  document.getElementById('formulario').addEventListener('submit', guardar);

  seleccionarRecurso('categorias');
});
