from fastapi import APIRouter, Depends, HTTPException
from psycopg2 import errors

from con_db import get_db
from schemas import PersonaIn

router = APIRouter(prefix="/personas", tags=["Personas"])


# GET -> SELECT (todas)
@router.get("")
def consultar_personas(conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT id_persona, nombre, telefono, tipo_persona
            FROM personas
            ORDER BY id_persona
        """)
        return cursor.fetchall()


# GET -> SELECT + WHERE (una)
@router.get("/{id_persona}")
def consultar_persona(id_persona: int, conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute("""
            SELECT id_persona, nombre, telefono, tipo_persona
            FROM personas
            WHERE id_persona = %s
        """, (id_persona,))
        persona = cursor.fetchone()

    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


# POST -> INSERT
@router.post("", status_code=201)
def guardar_persona(persona: PersonaIn, conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO personas (nombre, telefono, tipo_persona)
            VALUES (%s, %s, %s)
            RETURNING id_persona, nombre, telefono, tipo_persona
        """, (persona.nombre, persona.telefono, persona.tipo_persona))
        creada = cursor.fetchone()
    conexion.commit()
    return creada


# PUT -> UPDATE + WHERE
@router.put("/{id_persona}")
def actualizar_persona(id_persona: int, persona: PersonaIn, conexion=Depends(get_db)):
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE personas
            SET nombre = %s, telefono = %s, tipo_persona = %s
            WHERE id_persona = %s
            RETURNING id_persona, nombre, telefono, tipo_persona
        """, (persona.nombre, persona.telefono, persona.tipo_persona, id_persona))
        actualizada = cursor.fetchone()
    conexion.commit()

    if actualizada is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return actualizada


# DELETE -> DELETE + WHERE
@router.delete("/{id_persona}")
def eliminar_persona(id_persona: int, conexion=Depends(get_db)):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                DELETE FROM personas
                WHERE id_persona = %s
                RETURNING id_persona
            """, (id_persona,))
            eliminada = cursor.fetchone()
        conexion.commit()
    except errors.ForeignKeyViolation:
        conexion.rollback()
        raise HTTPException(
            status_code=409,
            detail="No se puede eliminar: la persona tiene emergencias registradas",
        )

    if eliminada is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"message": "Persona eliminada correctamente"}
