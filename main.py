from fastapi import FastAPI

from docs_theme import registrar_docs
from routers import emergencias, personas, ubicaciones

DESCRIPCION = (
    "API REST de **SENTIR** para registrar personas, reportar emergencias y "
    "asociarles una ubicación. Cada recurso ofrece consultar, crear, actualizar "
    "y eliminar, además de consultas de integración."
)

TAGS = [
    {"name": "Personas", "description": "Quién reporta: ciudadanos y otros tipos de persona."},
    {"name": "Emergencias", "description": "Reportes de emergencia, con consultas de ubicación y detalle."},
    {"name": "Ubicaciones", "description": "Coordenadas y dirección de cada emergencia."},
]

app = FastAPI(
    title="API Sentir",
    description=DESCRIPCION,
    version="1.0.0",
    openapi_tags=TAGS,
    docs_url=None,    # /docs lo define registrar_docs con el tema de SENTIR
    redoc_url=None,
)
registrar_docs(app)


@app.get("/")
def root():
    return {"message": "API Sentir - FastAPI"}


app.include_router(personas.router)
app.include_router(emergencias.router)
app.include_router(ubicaciones.router)
