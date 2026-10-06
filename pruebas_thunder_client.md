# Guía de pruebas con Thunder Client

Base URL: `http://127.0.0.1:8000`
Orden obligatorio: primero PERSONAS, luego EMERGENCIAS, luego UBICACIONES (por las claves foráneas).

## Flujo feliz
| # | Método | URL | Body | Esperado |
|---|--------|-----|------|----------|
| 1 | POST | /personas | `{"nombre":"Ana Pérez","telefono":"3001234567","tipo_persona":"CIUDADANO"}` | 201 + registro con id |
| 2 | POST | /emergencias | `{"tipo":"ACCIDENTE","descripcion":"Accidente cerca de la universidad","estado":"REPORTADA","id_persona":1}` | 201 |
| 3 | POST | /ubicaciones | `{"latitud":8.2501234,"longitud":-73.3556789,"direccion":"Calle 10 # 5-20","id_emergencia":1}` | 201 |
| 4 | GET | /emergencias | — | 200 lista |
| 5 | GET | /emergencias/1 | — | 200 |
| 6 | PUT | /emergencias/1 | `{"tipo":"ACCIDENTE","descripcion":"Accidente atendido","estado":"ATENDIDA","id_persona":1}` | 200 con estado ATENDIDA |
| 7 | GET | /ubicaciones | — | 200 lista |
| 8 | GET | /ubicaciones/1 | — | 200 |
| 9 | PUT | /ubicaciones/1 | `{"latitud":8.25,"longitud":-73.35,"direccion":"Calle 11 # 5-20","id_emergencia":1}` | 200 |
| 10 | GET | /emergencias/1/ubicacion | — | 200 ubicación |
| 11 | GET | /emergencias/1/detalle | — | 200 emergencia + persona + ubicación |

## Casos de error (id inexistente y claves foráneas)
| Método | URL | Esperado |
|--------|-----|----------|
| GET | /emergencias/999 | 404 Emergencia no encontrada |
| PUT | /emergencias/999 | 404 |
| DELETE | /emergencias/999 | 404 |
| GET | /ubicaciones/999 | 404 |
| GET | /emergencias/999/ubicacion | 404 |
| GET | /emergencias/999/detalle | 404 |
| POST /emergencias con `"id_persona": 999` | | 400 La persona indicada no existe |
| POST /ubicaciones con `"id_emergencia": 999` | | 400 La emergencia indicada no existe |
| POST /ubicaciones con `"latitud": 200` | | 422 validación |
| DELETE /personas/1 (tiene emergencias) | | 409 |
| DELETE /emergencias/1 (tiene ubicaciones) | | 409 |

## Cierre del flujo (DELETE)
Eliminar en orden inverso: `DELETE /ubicaciones/1` → `DELETE /emergencias/1` → `DELETE /personas/1`, todos 200.
Toma capturas de pantalla de cada respuesta como evidencia.
