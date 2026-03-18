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

Parametro requerido: `email_usuario`.

El sistema devolvera los datos ordenados del mas reciente al mas antiguo.

```sql
SELECT email_usuario, fecha, hora_inicio, espacio_nombre, estado
FROM reservadb.historial_usuario
WHERE email_usuario = 'eugenio23@example.com';
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
```

