from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import errors

from con_db import get_db
from schemas import UbicacionIn

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones"])

COLUMNAS = "id_ubicacion, latitud, longitud, direccion, id_emergencia"


# GET -> SELECT (todas)
@router.get("")
def consultar_ubicaciones(conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute(f"SELECT {COLUMNAS} FROM ubicaciones ORDER BY id_ubicacion")
        return cursor.fetchall()


# GET -> SELECT + WHERE (una)
@router.get("/{id_ubicacion}")
def consultar_ubicacion(id_ubicacion: int, conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute(
            f"SELECT {COLUMNAS} FROM ubicaciones WHERE id_ubicacion = %s",
            (id_ubicacion,),
        )
        ubicacion = cursor.fetchone()

    if ubicacion is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return ubicacion


# POST -> INSERT
@router.post("", status_code=201)
def registrar_ubicacion(ubicacion: UbicacionIn, conexion=Depends(get_db)):
    try:
        with conexion.cursor() as cursor:
            cursor.execute(f"""
                INSERT INTO ubicaciones (latitud, longitud, direccion, id_emergencia)
                VALUES (%s, %s, %s, %s)
                RETURNING {COLUMNAS}
            """, (ubicacion.latitud, ubicacion.longitud,
                  ubicacion.direccion, ubicacion.id_emergencia))
            creada = cursor.fetchone()
        conexion.commit()
    except errors.ForeignKeyViolation:
        conexion.rollback()
        raise HTTPException(status_code=400, detail="La emergencia indicada no existe")
    return creada


# PUT -> UPDATE + WHERE
@router.put("/{id_ubicacion}")
def actualizar_ubicacion(id_ubicacion: int, ubicacion: UbicacionIn,
                         conexion=Depends(get_db)):
    try:
        with conexion.cursor() as cursor:
            cursor.execute(f"""
                UPDATE ubicaciones
                SET latitud = %s, longitud = %s, direccion = %s, id_emergencia = %s
                WHERE id_ubicacion = %s
                RETURNING {COLUMNAS}
            """, (ubicacion.latitud, ubicacion.longitud, ubicacion.direccion,
                  ubicacion.id_emergencia, id_ubicacion))
            actualizada = cursor.fetchone()
        conexion.commit()
    except errors.ForeignKeyViolation:
        conexion.rollback()
        raise HTTPException(status_code=400, detail="La emergencia indicada no existe")

    if actualizada is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return actualizada


# DELETE -> DELETE + WHERE
@router.delete("/{id_ubicacion}")
def eliminar_ubicacion(id_ubicacion: int, conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute("""
            DELETE FROM ubicaciones
            WHERE id_ubicacion = %s
            RETURNING id_ubicacion
        """, (id_ubicacion,))
        eliminada = cursor.fetchone()
    conexion.commit()

    if eliminada is None:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return {"message": "Ubicación eliminada correctamente"}
