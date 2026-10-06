from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import errors

from con_db import get_db
from schemas import EmergenciaIn

router = APIRouter(prefix="/emergencias", tags=["Emergencias"])

COLUMNAS = "id_emergencia, tipo, descripcion, fecha, estado, id_persona"


# GET -> SELECT (todas)
@router.get("")
def consultar_emergencias(conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT {COLUMNAS} FROM emergencias ORDER BY id_emergencia")
        return cursor.fetchall()


# GET -> SELECT + WHERE (una)
@router.get("/{id_emergencia}")
def consultar_emergencia(id_emergencia: int, conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute(
            f"SELECT {COLUMNAS} FROM emergencias WHERE id_emergencia = %s",
            (id_emergencia,),
        )
        emergencia = cursor.fetchone()

    if emergencia is None:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")
    return emergencia


# POST -> INSERT
@router.post("", status_code=201)
def registrar_emergencia(emergencia: EmergenciaIn, conexion=Depends(get_db)):
    try:
        with conexion.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO emergencias (tipo, descripcion, fecha, estado, id_persona)
                VALUES (%s, %s, NOW(), %s, %s)
                RETURNING {COLUMNAS}
            """, (emergencia.tipo, emergencia.descripcion,
                  emergencia.estado, emergencia.id_persona))
            creada = cursor.fetchone()
        conexion.commit()
    except errors.ForeignKeyViolation:
        conexion.rollback()
        raise HTTPException(status_code=400, detail="La persona indicada no existe")
    return creada


# PUT -> UPDATE + WHERE
@router.put("/{id_emergencia}")
def actualizar_emergencia(id_emergencia: int, emergencia: EmergenciaIn,
                          conexion=Depends(get_db)):
    try:
        with conexion.cursor() as cursor:
            cursor.execute(f"""
                UPDATE emergencias
                SET tipo = %s, descripcion = %s, estado = %s, id_persona = %s
                WHERE id_emergencia = %s
                RETURNING {COLUMNAS}
            """, (emergencia.tipo, emergencia.descripcion, emergencia.estado,
                  emergencia.id_persona, id_emergencia))
            actualizada = cursor.fetchone()
        conexion.commit()
    except errors.ForeignKeyViolation:
        conexion.rollback()
        raise HTTPException(status_code=400, detail="La persona indicada no existe")

    if actualizada is None:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")
    return actualizada


# DELETE -> DELETE + WHERE
@router.delete("/{id_emergencia}")
def eliminar_emergencia(id_emergencia: int, conexion=Depends(get_db)):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                DELETE FROM emergencias
                WHERE id_emergencia = %s
                RETURNING id_emergencia
            """, (id_emergencia,))
            eliminada = cursor.fetchone()
        conexion.commit()
    except errors.ForeignKeyViolation:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar: la emergencia tiene ubicaciones asociadas",
        )

    if eliminada is None:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")
    return {"message": "Emergencia eliminada correctamente"}


# ---------------------- INTEGRACIÓN ----------------------

# GET -> ubicación asociada a una emergencia
@router.get("/{id_emergencia}/ubicacion")
def consultar_ubicacion_de_emergencia(id_emergencia: int, conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM emergencias WHERE id_emergencia = %s", (id_emergencia,)
        )
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Emergencia no encontrada")

        cursor.execute("""
            SELECT id_ubicacion, latitud, longitud, direccion, id_emergencia
            FROM ubicaciones
            WHERE id_emergencia = %s
            ORDER BY id_ubicacion
            LIMIT 1
        """, (id_emergencia,))
        ubicacion = cursor.fetchone()

    if ubicacion is None:
        raise HTTPException(
            status_code=404, detail="La emergencia no tiene ubicación registrada"
        )
    return ubicacion


# GET -> emergencia + persona que la reportó + ubicación
@router.get("/{id_emergencia}/detalle")
def consultar_detalle_de_emergencia(id_emergencia: int, conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT e.id_emergencia, e.tipo, e.descripcion, e.fecha, e.estado,
                   p.id_persona, p.nombre, p.telefono, p.tipo_persona,
                   u.id_ubicacion, u.latitud, u.longitud, u.direccion
            FROM emergencias e
            JOIN personas p ON p.id_persona = e.id_persona
            LEFT JOIN ubicaciones u ON u.id_emergencia = e.id_emergencia
            WHERE e.id_emergencia = %s
            ORDER BY u.id_ubicacion
            LIMIT 1
        """, (id_emergencia,))
        fila = cursor.fetchone()

    if fila is None:
        raise HTTPException(status_code=404, detail="Emergencia no encontrada")

    ubicacion = None
    if fila["id_ubicacion"] is not None:
        ubicacion = {
            "id_ubicacion": fila["id_ubicacion"],
            "latitud": fila["latitud"],
            "longitud": fila["longitud"],
            "direccion": fila["direccion"],
        }

    return {
        "emergencia": {
            "id_emergencia": fila["id_emergencia"],
            "tipo": fila["tipo"],
            "descripcion": fila["descripcion"],
            "fecha": fila["fecha"],
            "estado": fila["estado"],
        },
        "persona": {
            "id_persona": fila["id_persona"],
            "nombre": fila["nombre"],
            "telefono": fila["telefono"],
            "tipo_persona": fila["tipo_persona"],
        },
        "ubicacion": ubicacion,
    }
