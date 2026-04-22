## Crear Restricciones
```Bash
CREATE CONSTRAINT FOR (u:Usuario) REQUIRE u.email IS UNIQUE;
CREATE CONSTRAINT FOR (p:Pelicula) REQUIRE p.titulo IS UNIQUE;
CREATE CONSTRAINT FOR (g:Genero) REQUIRE g.nombreGenero IS UNIQUE;
CREATE CONSTRAINT FOR (a:Actor) REQUIRE a.nombre IS UNIQUE;
CREATE CONSTRAINT FOR (d:Director) REQUIRE d.nombre IS UNIQUE;
```

## Creación Básica con CREATE

```Bash
// 1. Crear los Nodos
CREATE (u1:Usuario {nombre: "Juan Perez", email: "juan@ejemplo.com", edad: 22, pais: "Guatemala"})
CREATE (p1:Pelicula {titulo: "Inception", añoLanzamiento: 2010, duracion: 148, sinopsis: "Un ladrón roba secretos corporativos."})
CREATE (g1:Genero {nombreGenero: "Ciencia Ficción", descripcion: "Basado en principios científicos."})

// 2. Crear las Relaciones con sus propiedades
CREATE (u1)-[:VIO {fechaVisualizacion: date("2026-04-20"), completo: true}]->(p1)
CREATE (u1)-[:CALIFICÓ {puntuacion: 5, fecha: date("2026-04-21"), comentario: "Excelente trama"}]->(p1)
CREATE (p1)-[:PERTENECE_A]->(g1)

```


## Carga

#### Cargar Usuarios
```Bash
LOAD CSV WITH HEADERS FROM 'file:///usuarios.csv' AS row
MERGE (u:Usuario {email: row.email})
SET u.nombre = row.nombre,
    u.edad = toInteger(row.edad),
    u.pais = row.pais;
```
#### Cargar Películas
```Bash
LOAD CSV WITH HEADERS FROM 'file:///peliculas.csv' AS row
MERGE (p:Pelicula {titulo: row.titulo})
SET p.anoLanzamiento = toInteger(row.anoLanzamiento),
    p.duracion = toInteger(row.duracion),
    p.sinopsis = row.sinopsis;
```
#### Cargar Géneros
```Bash
LOAD CSV WITH HEADERS FROM 'file:///generos.csv' AS row
MERGE (g:Genero {nombreGenero: row.nombreGenero})
SET g.descripcion = row.descripcion;
```
#### Cargar Actores
```Bash
LOAD CSV WITH HEADERS FROM 'file:///actores.csv' AS row
MERGE (a:Actor {nombre: row.nombre})
SET a.fechaNacimiento = date(row.fechaNacimiento),
    a.nacionalidad = row.nacionalidad;
```
#### Cargar Directores
```Bash
LOAD CSV WITH HEADERS FROM 'file:///directores.csv' AS row
MERGE (d:Director {nombre: row.nombre})
SET d.fechaNacimiento = date(row.fechaNacimiento),
    d.nacionalidad = row.nacionalidad;
```

## Relaciones

#### Califico
```Bash
LOAD CSV WITH HEADERS FROM 'file:///califico.csv' AS row
MATCH (u:Usuario {email: row.email})
MATCH (p:Pelicula {titulo: row.titulo})
MERGE (u)-[c:CALIFICÓ]->(p)
SET c.puntuacion = toInteger(row.puntuacion),
    c.fecha = date(row.fecha),
    c.comentario = row.comentario;
```

#### VIO
```Bash
MATCH (u:Usuario), (p:Pelicula)
WITH u, p ORDER BY rand() LIMIT 2500
MERGE (u)-[:VIO {fechaVisualizacion: date('2025-10-15'), completo: true}]->(p);
```
#### ES AMIGO DE
```Bash
MATCH (u1:Usuario), (u2:Usuario)
WHERE u1.email <> u2.email
WITH u1, u2 ORDER BY rand() LIMIT 1500
MERGE (u1)-[:ES_AMIGO_DE {fechaAmistad: date('2024-01-20')}]->(u2);
```
#### PERTENECE_A
```Bash
MATCH (p:Pelicula), (g:Genero)
WITH p, g ORDER BY rand()
WITH p, collect(g)[0..2] AS generos
UNWIND generos AS g
MERGE (p)-[:PERTENECE_A]->(g);
```
#### ACTUO_EN
```Bash
MATCH (a:Actor), (p:Pelicula)
WITH a, p ORDER BY rand() LIMIT 800
MERGE (a)-[:ACTUÓ_EN {personaje: "Personaje " + toString(toInteger(rand()*100))}]->(p);
```

#### Dirigio
```Bash
MATCH (d:Director), (p:Pelicula)
WITH d, p ORDER BY rand()
WITH p, collect(d)[0] AS dir
MERGE (dir)-[:DIRIGIÓ]->(p);
```

#### LE_GUSTA
```Bash
MATCH (u:Usuario), (g:Genero)
WITH u, g ORDER BY rand() LIMIT 1200
MERGE (u)-[:LE_GUSTA {nivelInteres: toInteger(rand()*5)+1}]->(g);
```


# Consultas
```Bash
# 1. Obtener todas las películas calificadas por un usuario específico con puntuación mayor a 4
MATCH (u:Usuario {email: "user10@ejemplo.com"})-[c:CALIFICÓ]->(p:Pelicula)
WHERE c.puntuacion > 4
RETURN p.titulo, c.puntuacion, c.comentario

# 2. Encontrar las películas que vieron los amigos de un usuario pero que el usuario aún no ha visto
MATCH (u:Usuario {email: "user15@ejemplo.com"})-[:ES_AMIGO_DE]-(amigo:Usuario)
MATCH (amigo)-[:VIO]->(p:Pelicula)
WHERE NOT (u)-[:VIO]->(p)
RETURN DISTINCT p.titulo AS PeliculasRecomendadas

# 3. Obtener el promedio de calificaciones de una película
MATCH (u:Usuario)-[c:CALIFICÓ]->(p:Pelicula {titulo: "Pelicula 45"})
RETURN p.titulo, avg(c.puntuacion) AS PromedioCalificacion

# 4. Encontrar los géneros favoritos de un usuario basándose en sus calificaciones
MATCH (u:Usuario {email: "user25@ejemplo.com"})-[c:CALIFICÓ]->(p:Pelicula)-[:PERTENECE_A]->(g:Genero)
RETURN g.nombreGenero AS Genero, avg(c.puntuacion) AS PuntuacionPromedio, count(p) AS PeliculasCalificadas
ORDER BY PuntuacionPromedio DESC, PeliculasCalificadas DESC
LIMIT 3

# 5. Encontrar la ruta más corta de amistad entre dos usuarios
MATCH ruta = shortestPath((u1:Usuario {email: "user10@ejemplo.com"})-[:ES_AMIGO_DE*]-(u2:Usuario {email: "user400@ejemplo.com"}))
RETURN ruta


# 6. Listar las películas más populares (con más visualizaciones) de un género específico
MATCH (u:Usuario)-[:VIO]->(p:Pelicula)-[:PERTENECE_A]->(g:Genero {nombreGenero: "Ciencia Ficción"})
RETURN p.titulo AS Pelicula, count(u) AS TotalVisualizaciones
ORDER BY TotalVisualizaciones DESC
LIMIT 5
```