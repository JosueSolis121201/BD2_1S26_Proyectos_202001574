-- 1. Crear el Keyspace con Replication Factor de 3
CREATE KEYSPACE reservadb WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};
USE reservadb;

-- 2. Tabla para consultar disponibilidad por espacio y fecha (Query 1)
CREATE TABLE disponibilidad_espacio_fecha (
    espacio_nombre text,
    fecha date,
    hora_inicio time,
    hora_fin time,
    estado text,
    PRIMARY KEY ((espacio_nombre, fecha), hora_inicio)
);

-- 3. Tabla para el historial de reservas de un usuario (Query 2)
CREATE TABLE historial_usuario (
    email_usuario text,
    fecha date,
    hora_inicio time,
    espacio_nombre text,
    estado text,
    PRIMARY KEY ((email_usuario), fecha, hora_inicio)
) WITH CLUSTERING ORDER BY (fecha DESC, hora_inicio DESC);

-- 4. Tabla para ocupación de espacios en un rango de fechas (Query 3)
CREATE TABLE ocupacion_espacio_mes (
    espacio_nombre text,
    mes_anio text, 
    fecha date,
    hora_inicio time,
    usuario_email text,
    estado text,
    PRIMARY KEY ((espacio_nombre, mes_anio), fecha, hora_inicio)
);