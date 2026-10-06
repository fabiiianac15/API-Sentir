# API SENTIR

API REST del proyecto **SENTIR** para registrar **personas**, reportar **emergencias** y asociarles una **ubicación**, con consultas de integración que unen los tres recursos.

> Guía completa de instalación (Windows y Linux): [`GUIA_INSTALACION.md`](GUIA_INSTALACION.md)

## Tecnologías
- Python 3.10+ · FastAPI · Uvicorn
- PostgreSQL · psycopg2
- Pydantic (validación de datos) · python-dotenv (variables de entorno)
- Swagger UI con tema propio (`/docs`)

## Estructura del proyecto
```
api-sentir/
├── main.py                  # App FastAPI y registro de routers
├── con_db.py                # Conexión a PostgreSQL
├── schemas.py               # Modelos de entrada (Pydantic)
├── docs_theme.py            # Tema visual de /docs
├── routers/
│   ├── __init__.py
│   ├── personas.py
│   ├── emergencias.py       # incluye endpoints de integración
│   └── ubicaciones.py
├── schema.sql               # Tablas de la base de datos
├── requirements.txt
├── .env.example             # Plantilla de variables de entorno
├── .gitignore
├── GUIA_INSTALACION.md
└── pruebas_thunder_client.md
```

## Inicio rápido
Resumen para quien ya tiene Python y PostgreSQL instalados. Si no, sigue la [guía de instalación](GUIA_INSTALACION.md).

```bash
# 1. Entorno virtual y dependencias
python -m venv venv
# Windows: venv\Scripts\activate      Linux/Mac: source venv/bin/activate
pip install -r requirements.txt

# 2. Base de datos (usuario, base y tablas)
#    Ver la guía: sección 4

# 3. Variables de entorno
#    Windows: copy .env.example .env   Linux/Mac: cp .env.example .env
#    y completar las 5 variables

# 4. Probar la conexión
python con_db.py

# 5. Arrancar la API
uvicorn main:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs

> Si cambias el `.env`, **reinicia uvicorn**. `--reload` solo vigila archivos `.py`.

## Endpoints

| Recurso | Método | Endpoint | Acción |
|---------|--------|----------|--------|
| Personas | GET | `/personas` | Listar todas |
| | GET | `/personas/{id}` | Consultar una |
| | POST | `/personas` | Crear |
| | PUT | `/personas/{id}` | Actualizar |
| | DELETE | `/personas/{id}` | Eliminar |
| Emergencias | GET | `/emergencias` | Listar todas |
| | GET | `/emergencias/{id}` | Consultar una |
| | POST | `/emergencias` | Registrar |
| | PUT | `/emergencias/{id}` | Actualizar |
| | DELETE | `/emergencias/{id}` | Eliminar |
| Ubicaciones | GET | `/ubicaciones` | Listar todas |
| | GET | `/ubicaciones/{id}` | Consultar una |
| | POST | `/ubicaciones` | Registrar |
| | PUT | `/ubicaciones/{id}` | Actualizar |
| | DELETE | `/ubicaciones/{id}` | Eliminar |
| Integración | GET | `/emergencias/{id}/ubicacion` | Ubicación de una emergencia |
| | GET | `/emergencias/{id}/detalle` | Emergencia + persona + ubicación |

## Ejemplos de body

**POST /personas**
```json
{
  "nombre": "Ana Pérez",
  "telefono": "3001234567",
  "tipo_persona": "CIUDADANO"
}
```

**POST /emergencias** (`fecha` la asigna el servidor; `estado` por defecto es `REPORTADA`)
```json
{
  "tipo": "ACCIDENTE",
  "descripcion": "Accidente cerca de la universidad",
  "estado": "REPORTADA",
  "id_persona": 1
}
```

**POST /ubicaciones**
```json
{
  "latitud": 8.2501234,
  "longitud": -73.3556789,
  "direccion": "Calle 10 # 5-20",
  "id_emergencia": 1
}
```

**Respuesta de GET /emergencias/1/detalle**
```json
{
  "emergencia": {
    "id_emergencia": 1,
    "tipo": "ACCIDENTE",
    "descripcion": "Accidente cerca de la universidad",
    "fecha": "2026-10-05T18:30:00",
    "estado": "REPORTADA"
  },
  "persona": {
    "id_persona": 1,
    "nombre": "Ana Pérez",
    "telefono": "3001234567",
    "tipo_persona": "CIUDADANO"
  },
  "ubicacion": {
    "id_ubicacion": 1,
    "latitud": 8.2501234,
    "longitud": -73.3556789,
    "direccion": "Calle 10 # 5-20"
  }
}
```
Si la emergencia aún no tiene ubicación, `ubicacion` viene como `null`.

## Claves foráneas
```
personas (id_persona) ◄── emergencias (id_persona)
                          emergencias (id_emergencia) ◄── ubicaciones (id_emergencia)
```
Por eso el orden para crear datos es: **persona → emergencia → ubicación**, y para borrar, el inverso.

## Códigos de respuesta
| Código | Significado |
|--------|-------------|
| 200 | Operación exitosa |
| 201 | Registro creado |
| 400 | Clave foránea inválida (la persona o emergencia indicada no existe) |
| 404 | El identificador no existe |
| 409 | No se puede eliminar: tiene registros asociados |
| 422 | Datos inválidos (campo faltante, latitud fuera de rango, etc.) |
| 500 | Error del servidor (normalmente conexión a la base de datos) |

## Pruebas
Casos de prueba para Thunder Client, con éxito y errores: [`pruebas_thunder_client.md`](pruebas_thunder_client.md).

## Seguridad
`.env` y `venv/` están en `.gitignore` y **no deben subirse** a GitHub. Comparte solo `.env.example`.