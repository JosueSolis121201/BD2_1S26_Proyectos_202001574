**Curso:** Bases 2

**Universidad:** Universidad de San Carlos de Guatemala (USAC) - FIUSAC 

**Estudiante:** Josue Daniel Solis Osorio

**Carnet:** 202001574

---


# Manual de Usuario

## 2.1 Guia de Instalacion del Cluster

Para levantar el sistema en cualquier entorno local, siga estos pasos:

1. Instale Docker y Docker Compose en su maquina.
2. Descargue el archivo `docker-compose.yml` provisto en el codigo fuente.
3. Abra una terminal en el directorio del archivo y ejecute:

```bash
docker compose up -d
```

4. Espere un par de minutos a que los 3 nodos se sincronicen e inicien.
5. Acceda a la consola CQL ejecutando:

```bash
docker exec -it cassandra-node1 cqlsh
```

## 2.2 Guia de Consultas Implementadas 

A continuacion, se presentan los comandos para utilizar las consultas del negocio.

### A. Consultar la disponibilidad de un espacio en una fecha concreta

**Descripción:** Muestra todas las reservas de un espacio específico en una fecha exacta, ordenadas por hora de inicio. Permite identificar rápidamente cuáles horarios están ocupados (Completada, Confirmada, Cancelada) y cuáles están disponibles para nuevas reservas.

Parametros: `espacio_nombre` y `fecha`.

```sql
SELECT *
FROM reservadb.disponibilidad_espacio_fecha
WHERE espacio_nombre = 'Sala 5'
    AND fecha = '2026-08-15';
```

Ejemplo de salida:

```text
espacio_nombre | fecha      | hora_inicio        | estado     | hora_fin
---------------+------------+--------------------+------------+--------------------
Sala 5         | 2026-08-15 | 08:00:00.000000000 | Completada | 11:00:00.000000000
Sala 5         | 2026-08-15 | 10:00:00.000000000 | Confirmada | 14:00:00.000000000
Sala 5         | 2026-08-15 | 14:00:00.000000000 | Completada | 16:00:00.000000000
Sala 5         | 2026-08-15 | 15:00:00.000000000 | Cancelada  | 18:00:00.000000000
Sala 5         | 2026-08-15 | 17:00:00.000000000 | Completada | 21:00:00.000000000
Sala 5         | 2026-08-15 | 18:00:00.000000000 | Confirmada | 21:00:00.000000000
```

### B. Ver el historial de reservas de un usuario

**Descripción:** Retorna todas las reservas realizadas por un usuario específico, ordenadas automáticamente de las más recientes a las antiguas. Permite al usuario revisar su actividad y al administrador hacer seguimiento de patrones de uso.

Parametro requerido: `email_usuario`.

El sistema devolvera los datos ordenados del mas reciente al mas antiguo.

```sql
SELECT email_usuario, fecha, hora_inicio, espacio_nombre, estado
FROM reservadb.historial_usuario
WHERE email_usuario = 'ariasbianca@example.net'; 


SELECT * FROM reservadb.historial_usuario;
```

Ejemplo de salida:

```text
email_usuario         | fecha      | hora_inicio        | espacio_nombre | estado
----------------------+------------+--------------------+----------------+-----------
eugenio23@example.com | 2026-12-29 | 11:00:00.000000000 | Escritorio 37  | Confirmada
eugenio23@example.com | 2026-12-24 | 14:00:00.000000000 | Sala 5         | Confirmada
eugenio23@example.com | 2026-12-24 | 13:00:00.000000000 | Escritorio 21  | Cancelada
... (188 rows)
```

### C. Obtener ocupacion de espacios en un rango de fechas

**Descripción:** Consulta la ocupación de un espacio durante un rango de fechas dentro de un mes específico. Devuelve todas las reservas en el rango, permitiendo analizar la demanda y disponibilidad de un espacio durante períodos determinados.

Parametros requeridos: `espacio_nombre`, `mes_anio` y el rango de fechas (`>=` y `<=`).

```sql
SELECT *
FROM reservadb.ocupacion_espacio_mes
WHERE espacio_nombre = 'Escritorio 10'
    AND mes_anio = '2026-05'
    AND fecha >= '2026-05-01'
    AND fecha <= '2026-05-15';
```

## 2.3 Resolucion de problemas comunes

### 1) Error de conexion en cqlsh

Sintoma:

```text
Connection error: ('Unable to connect to any servers', ... Connection refused ...)
```

Causa probable: Cassandra aun no termina de iniciar.

Solucion:

```bash
docker ps -a
docker logs -f cassandra-node1
```

Espere hasta ver `Startup complete` y luego intente de nuevo:

```bash
docker exec -it cassandra-node1 cqlsh
```

### 2) El comando pip falla con "Unknown or unsupported command 'install'"

Sintoma:

```text
Unknown or unsupported command 'install'
```

Causa probable: `pip` apunta a otra herramienta del sistema y no al de Python.

Solucion:

```bash
python -m pip install cassandra-driver faker
```

Si tiene mas de una version de Python, use el ejecutable especifico de su entorno.

### 3) Los nodos Cassandra no se mantienen estables

Sintoma: reinicios, errores de bootstrap o datos inconsistentes al iniciar varias veces.

Causa probable: volumenes previos con estado de cluster anterior.

Solucion (reinicio limpio):

```bash
docker compose down -v
docker compose up -d
```

Luego valide el estado:

```bash
docker exec cassandra-node1 nodetool status
docker exec cassandra-node1 cqlsh -e "DESCRIBE CLUSTER;"
```

### 4) Un contenedor no aparece en estado Up

Sintoma: alguno de los nodos sale como `Exited` en `docker ps -a`.

Solucion:

```bash
docker logs cassandra-node2
docker logs cassandra-node3
docker compose up -d


docker exec cassandra-node2 nodetool status

docker stop cassandra-node3
docker logs cassandra-node3

docker start cassandra-node3
```

Vaciar bd mantener tablas:
docker exec -i cassandra-node1 cqlsh -e "TRUNCATE reservadb.disponibilidad_espacio_fecha; TRUNCATE reservadb.historial_usuario; TRUNCATE reservadb.ocupacion_espacio_mes;"

cargarbd:
Get-Content .\scrips\create.cql | docker exec -i cassandra-node1 cqlsh

activar venv:
& .\.venv\Scripts\Activate.ps1
python -m pip install cassandra-driver faker

cargar datos:
python .\generar_datos.py

validacion
docker exec -it cassandra-node1 cqlsh -e "SELECT * FROM reservadb.historial_usuario LIMIT 5;"
docker exec -it cassandra-node1 cqlsh -e "SELECT COUNT(*) FROM reservadb.historial_usuario;"


## Test Limpieza
# Reset completo + carga de esquema + carga masiva de datos (todo en una sola corrida)
docker compose down -v
docker compose up -d

Write-Host "Esperando que cassandra-node1 acepte CQL..."
do {
    Start-Sleep -Seconds 5
    $ok = docker exec cassandra-node1 cqlsh -e "DESCRIBE KEYSPACES;" 2>$null
} until ($LASTEXITCODE -eq 0)

Write-Host "Aplicando esquema..."
Get-Content .\scrips\create.cql | docker exec -i cassandra-node1 cqlsh

Write-Host "Activando entorno virtual..."
& .\.venv\Scripts\Activate.ps1

Write-Host "Instalando dependencias Python..."
python -m pip install cassandra-driver faker

Write-Host "Cargando 100,000 reservas..."
python .\generar_datos.py

Write-Host "Verificando cluster y datos..."
docker exec cassandra-node1 nodetool status
docker exec cassandra-node1 cqlsh -e "SELECT * FROM reservadb.disponibilidad_espacio_fecha LIMIT 5;"
docker exec cassandra-node1 cqlsh -e "SELECT * FROM reservadb.historial_usuario LIMIT 5;"
docker exec cassandra-node1 cqlsh -e "SELECT * FROM reservadb.ocupacion_espacio_mes LIMIT 5;"


## Test Caida y recarga nodo

$NodoCaido = "cassandra-node2"

Write-Host "1) Estado inicial del cluster"
docker exec cassandra-node1 nodetool status

Write-Host "2) Simulando caída de $NodoCaido"
docker stop $NodoCaido

Write-Host "3) Validando estado tras la caída"
docker ps -a
docker exec cassandra-node1 nodetool status

Write-Host "4) Pruebas de consistencia con 1 nodo caído"
docker exec cassandra-node1 cqlsh -e "CONSISTENCY ONE; SELECT * FROM reservadb.historial_usuario LIMIT 1;"
docker exec cassandra-node1 cqlsh -e "CONSISTENCY QUORUM; SELECT * FROM reservadb.historial_usuario LIMIT 1;"
docker exec cassandra-node1 cqlsh -e "CONSISTENCY ALL; SELECT * FROM reservadb.historial_usuario LIMIT 1;"

Write-Host "5) Restaurando nodo"
docker start $NodoCaido

Write-Host "6) Estado final del cluster"
docker exec cassandra-node1 nodetool status