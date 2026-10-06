from pydantic import BaseModel, Field


class PersonaIn(BaseModel):
    nombre: str
    telefono: str
    tipo_persona: str


class EmergenciaIn(BaseModel):
    tipo: str
    descripcion: str
    estado: str = "REPORTADA"
    id_persona: int


class UbicacionIn(BaseModel):
    latitud: float = Field(ge=-90, le=90)
    longitud: float = Field(ge=-180, le=180)
    direccion: str
    id_emergencia: int
