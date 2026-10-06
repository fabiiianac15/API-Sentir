-- Esquema de la base de datos SENTIR (PostgreSQL)
-- Ejecutar solo si las tablas aún no existen: psql -U <usuario> -d <base> -f schema.sql

CREATE TABLE IF NOT EXISTS personas (
    id_persona   SERIAL PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    telefono     VARCHAR(20),
    tipo_persona VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS emergencias (
    id_emergencia SERIAL PRIMARY KEY,
    tipo          VARCHAR(50)  NOT NULL,
    descripcion   TEXT,
    fecha         TIMESTAMP    NOT NULL DEFAULT NOW(),
    estado        VARCHAR(30)  NOT NULL DEFAULT 'REPORTADA',
    id_persona    INTEGER      NOT NULL REFERENCES personas(id_persona)
);

CREATE TABLE IF NOT EXISTS ubicaciones (
    id_ubicacion  SERIAL PRIMARY KEY,
    latitud       DOUBLE PRECISION NOT NULL,
    longitud      DOUBLE PRECISION NOT NULL,
    direccion     VARCHAR(200),
    id_emergencia INTEGER NOT NULL REFERENCES emergencias(id_emergencia)
);
