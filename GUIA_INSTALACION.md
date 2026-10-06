# Guía de instalación y puesta en marcha

Pasos para dejar la API SENTIR funcionando desde cero, por terminal, en **Windows** y **Linux** (Ubuntu/Debian, Arch, Fedora).

**Orden general:** proyecto → entorno virtual → PostgreSQL → usuario, base y tablas → `.env` → probar conexión → arrancar → probar endpoints.

Datos que usa esta guía (puedes cambiarlos, pero deben coincidir en todos los pasos y en el `.env`):

| Dato | Valor |
|------|-------|
| Usuario de la base | `sentir_user` |
| Contraseña | `sentir123` |
| Base de datos | `sentir` |
| Puerto | `5432` |

---

## 0. Requisitos
- Python 3.10 o superior (`python --version`)
- Git (opcional, para clonar)
- PostgreSQL 14 o superior (se instala en el paso 3)

## 1. Obtener el proyecto
```bash
git clone <URL-de-tu-repositorio> api-sentir
cd api-sentir
```
Si lo descargaste como `.zip`, descomprímelo y entra a la carpeta. **Comprueba que `routers/` sea una subcarpeta** junto a `main.py`; si quedó todo suelto, la API falla con `No module named 'routers'`.

## 2. Entorno virtual y dependencias

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Si al activar dice que la ejecución de scripts está deshabilitada:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
y vuelve a activar.

**Linux**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
En Debian/Ubuntu, si falla la creación del entorno: `sudo apt install -y python3-venv python3-pip`.

Sabrás que está activo porque la terminal muestra `(venv)` al inicio.

## 3. Instalar PostgreSQL

### Windows
Opción recomendada: descargar el instalador de https://www.postgresql.org/download/windows/ y ejecutarlo. **Cuando pida contraseña para el superusuario `postgres`, anótala.** Deja el puerto `5432`.

Por terminal también se puede:
```powershell
winget install -e --id PostgreSQL.PostgreSQL.16
```
Esta vía puede instalar sin pedir clave. Si te pasó, ve a la sección 11.

Agrega `psql` a la terminal. **Cambia `16` por tu versión instalada** (mira la carpeta `C:\Program Files\PostgreSQL`):
```powershell
$env:Path += ";C:\Program Files\PostgreSQL\16\bin"
psql --version
```
Esto vale solo para la terminal actual; repítelo en cada terminal nueva o agrégalo al PATH del sistema.

### Ubuntu / Debian / Mint
```bash
sudo apt update && sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable --now postgresql
```

### Arch / Manjaro / EndeavourOS
En Arch hay que inicializar el clúster antes de arrancar el servicio:
```bash
sudo pacman -S --needed postgresql
sudo -iu postgres initdb --locale=C.UTF-8 --encoding=UTF8 -D /var/lib/postgres/data
sudo systemctl enable --now postgresql
```

### Fedora
```bash
sudo dnf install -y postgresql-server postgresql-contrib
sudo postgresql-setup --initdb
sudo systemctl enable --now postgresql
```
Fedora trae autenticación `ident` para conexiones locales, que rechaza contraseñas. Corrígelo:
```bash
sudo sed -i 's/ident$/scram-sha-256/' /var/lib/pgsql/data/pg_hba.conf
sudo systemctl restart postgresql
```

Comprueba que el servicio corre: `systemctl status postgresql` (Linux) o `Get-Service postgresql*` (Windows).

## 4. Crear usuario, base y tablas

Ejecuta esto **dentro de la carpeta del proyecto** (donde está `schema.sql`).

### Windows
Usa la contraseña de `postgres` que definiste al instalar (aquí `TU_CLAVE_POSTGRES`):
```powershell
$env:PGPASSWORD="TU_CLAVE_POSTGRES"
psql -U postgres -h 127.0.0.1 -c "CREATE USER sentir_user WITH PASSWORD 'sentir123';"
psql -U postgres -h 127.0.0.1 -c "CREATE DATABASE sentir OWNER sentir_user;"

$env:PGPASSWORD="sentir123"
psql -U sentir_user -h 127.0.0.1 -d sentir -f schema.sql
psql -U sentir_user -h 127.0.0.1 -d sentir -c "\dt"
```

### Linux
```bash
sudo -u postgres psql -c "CREATE USER sentir_user WITH PASSWORD 'sentir123';"
sudo -u postgres psql -c "CREATE DATABASE sentir OWNER sentir_user;"

PGPASSWORD=sentir123 psql -h 127.0.0.1 -U sentir_user -d sentir -f schema.sql
PGPASSWORD=sentir123 psql -h 127.0.0.1 -U sentir_user -d sentir -c "\dt"
```

El último comando debe listar tres tablas: `personas`, `emergencias` y `ubicaciones`.

> Si ya tienes tablas propias con otros nombres de columna, no ejecutes `schema.sql`; ajusta el código a tus columnas.

## 5. Configurar el `.env`

El archivo debe llamarse exactamente `.env` (sin `.txt`), en la misma carpeta que `main.py`, con las **cinco** variables y sin comillas ni espacios alrededor del `=`.

**Windows (PowerShell)** — se escribe con codificación correcta:
```powershell
@"
DB_HOST=127.0.0.1
DB_NAME=sentir
DB_USER=sentir_user
DB_PASSWORD=sentir123
DB_PORT=5432
"@ | Set-Content -Path .env -Encoding ascii
Get-Content .env
```

**Linux**
```bash
cat > .env << 'ENVEOF'
DB_HOST=127.0.0.1
DB_NAME=sentir
DB_USER=sentir_user
DB_PASSWORD=sentir123
DB_PORT=5432
ENVEOF
cat .env
```

Por qué `127.0.0.1` y no `localhost`: `localhost` a veces resuelve a IPv6 (`::1`) y la conexión falla de forma confusa. La IP fuerza IPv4.

## 6. Probar la conexión
```bash
python con_db.py
```
(En Linux, `python3` si `python` no existe.) Debe imprimir:
```
Conexión exitosa a la base de datos
```
Si falla, ve a la sección 10.

## 7. Arrancar la API
Desde la carpeta del proyecto, con `(venv)` activo:
```bash
uvicorn main:app --reload
```
- `main:app` = archivo `main.py`, variable `app`.
- Abre http://127.0.0.1:8000/docs.

> **Importante:** `--reload` solo reinicia cuando cambia un archivo `.py`. Si editas el `.env`, detén uvicorn (`Ctrl + C`) y vuelve a lanzarlo.

## 8. Probar los endpoints
En `/docs` (o con Thunder Client), en este orden por las claves foráneas:

1. `POST /personas` → `{"nombre":"Ana Pérez","telefono":"3001234567","tipo_persona":"CIUDADANO"}` → 201
2. `POST /emergencias` → `{"tipo":"ACCIDENTE","descripcion":"Accidente cerca de la universidad","estado":"REPORTADA","id_persona":1}` → 201
3. `POST /ubicaciones` → `{"latitud":8.2501234,"longitud":-73.3556789,"direccion":"Calle 10 # 5-20","id_emergencia":1}` → 201
4. `GET /emergencias/1/detalle` → emergencia, persona y ubicación juntas
5. Prueba un id inexistente, por ejemplo `GET /emergencias/999` → 404

Más casos en `pruebas_thunder_client.md`.

## 9. Alternativa: PostgreSQL con Docker
Si prefieres no instalar PostgreSQL, crea `docker-compose.yml` en la carpeta del proyecto:
```yaml
services:
  db:
    image: postgres:16
    container_name: sentir-db
    environment:
      POSTGRES_DB: sentir
      POSTGRES_USER: sentir_user
      POSTGRES_PASSWORD: sentir123
    ports:
      - "5432:5432"
    volumes:
      - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql
      - sentir_data:/var/lib/postgresql/data
volumes:
  sentir_data:
```
```bash
docker compose up -d
```
Crea la base y las tablas solo la primera vez. El `.env` es el mismo de la sección 5. Para empezar de cero: `docker compose down -v`.

## 10. Problemas frecuentes

| Síntoma | Causa y solución |
|---------|------------------|
| `ModuleNotFoundError: No module named 'routers'` | Falta la subcarpeta `routers/` (con `__init__.py`) junto a `main.py`, o ejecutas uvicorn desde otra carpeta. |
| `Error loading ASGI app. Attribute "api" not found` | Comando mal escrito. Es `uvicorn main:app --reload`. |
| `fe_sendauth: no password supplied` | El `.env` no tiene `DB_PASSWORD`, tiene otro nombre (`.env.txt`) o no está en la carpeta correcta. Recréalo con la sección 5. |
| `password authentication failed for user` | La contraseña del `.env` no coincide con la de la base. Cámbiala: `ALTER USER sentir_user PASSWORD 'sentir123';` |
| `database "sentir" does not exist` | Falta crear la base (sección 4). |
| `connection refused` | PostgreSQL no está corriendo. Arráncalo con `systemctl start postgresql` (Linux) o `Start-Service` (Windows). |
| `connection to server at "localhost" (::1)` | Pon `DB_HOST=127.0.0.1` en el `.env`. |
| `/docs` da error 500 al ejecutar, pero `python con_db.py` conecta | uvicorn arrancó con un `.env` anterior. Reinícialo (`Ctrl + C` y de nuevo). |
| `permission denied for schema public` | La base se creó sin dueño correcto: `ALTER DATABASE sentir OWNER TO sentir_user;` |
| `relation "personas" does not exist` | No se ejecutó `schema.sql` en la base `sentir`. |
| `psql` no se reconoce (Windows) | Agrega la carpeta `bin` de tu versión al PATH (sección 3). |
| El puerto 5432 está ocupado | Hay otro PostgreSQL. Cambia el puerto y `DB_PORT` en el `.env`. |
| `la ejecución de scripts está deshabilitada` al activar el venv | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |

## 11. Windows: PostgreSQL instalado sin clave (o clave olvidada)

Se resetea saltándose la autenticación unos segundos. Abre PowerShell **como administrador** y pega el bloque completo. Detecta solo la versión, el servicio y las rutas:

```powershell
$svc = Get-CimInstance Win32_Service | Where-Object { $_.Name -like "postgresql*" } | Select-Object -First 1
$name   = $svc.Name
$pgdata = $svc.PathName -replace '.*-D\s+"([^"]+)".*','$1'
$bin    = Split-Path ($svc.PathName -replace '^"([^"]+)".*','$1')
$env:Path += ";$bin"
"Servicio: $name | Datos: $pgdata"

# Respaldo ANTES de modificar, y autenticación temporal sin clave
Copy-Item "$pgdata\pg_hba.conf" "$pgdata\pg_hba.original" -Force
(Get-Content "$pgdata\pg_hba.conf") -replace 'scram-sha-256','trust' | Set-Content "$pgdata\pg_hba.conf"
Restart-Service $name -Force
Start-Sleep 3

# Nueva clave para postgres
psql -U postgres -h 127.0.0.1 -w -c "ALTER USER postgres PASSWORD 'postgres123';"

# Restaurar la seguridad original
Copy-Item "$pgdata\pg_hba.original" "$pgdata\pg_hba.conf" -Force
Restart-Service $name -Force
Start-Sleep 3
```

- Debe aparecer `ALTER ROLE`. La clave de `postgres` queda en `postgres123`.
- Mientras el archivo está en modo sin clave, cualquiera en el equipo entraría sin contraseña: ejecuta el bloque completo, sin pausas.
- Verifica que la seguridad volvió: `Select-String -Path "$pgdata\pg_hba.conf" -Pattern "^host"` debe mostrar `scram-sha-256`.
- Luego continúa en la sección 4, usando `postgres123` como clave de `postgres`.

## 12. Comandos útiles

```bash
# Ver datos
psql -h 127.0.0.1 -U sentir_user -d sentir -c "SELECT * FROM emergencias;"

# Borrar y recrear las tablas (empezar de cero)
psql -h 127.0.0.1 -U sentir_user -d sentir -c "DROP TABLE IF EXISTS ubicaciones, emergencias, personas CASCADE;"
psql -h 127.0.0.1 -U sentir_user -d sentir -f schema.sql

# Linux: estado / parar / arrancar PostgreSQL
sudo systemctl status postgresql
sudo systemctl stop postgresql
sudo systemctl start postgresql
```
En Windows: `Get-Service postgresql*`, `Stop-Service <nombre>`, `Start-Service <nombre>`. En PowerShell, `PGPASSWORD` se define con `$env:PGPASSWORD="clave"` antes de `psql`.

## 13. Antes de subir a GitHub
- `.env` y `venv/` **no** se suben (ya están en `.gitignore`).
- Verifica con `git status` que `.env` no aparezca en la lista.
- Comparte solo `.env.example`, con valores de ejemplo.
