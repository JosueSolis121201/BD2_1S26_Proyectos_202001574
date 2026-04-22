Documentación Técnica: Sistema de Recomendación de Películas con Neo4j
Este documento detalla el diseño e implementación del sistema de recomendación desarrollado para el curso de Sistemas de Bases de Datos 2 de la Universidad de San Carlos de Guatemala.

# 1. Modelo Conceptual de Grafos
El modelo representa las relaciones complejas entre usuarios, contenido cinematográfico y conexiones sociales de forma natural 

![alt text](<Segundo Proyecto/img/Diagrama.png>)


# 2. Descripción de Propiedades de Nodos y Relaciones
A continuación se detallan los atributos utilizados para enriquecer el modelo de datos.

2.1 Nodos (Entidades)
- Usuario: Nombre, Email (Único), Edad, País
- Película: Título, Año de Lanzamiento, Duración (minutos), Sinopsis
- Género: Nombre del Género, Descripción
- Actor: Nombre, Fecha de Nacimiento, Nacionalidad
- Director: Nombre, Fecha de Nacimiento, Nacionalidad

2.2 Relaciones
- CALIFICÓ: Puntuación [1-5], fecha, comentario
- VIO: Fecha de visualización, completó [true/false]
- ES_AMIGO_DE: Fecha de amistad
- ACTUÓ_EN: Nombre del personaje
- LE_GUSTA: Nivel de interés [1-5]


3. Script Cypher de Creación del Esquema
Se implementaron restricciones de unicidad para garantizar la integridad de los datos antes de la carga masiva 
// Restricciones de Unicidad
CREATE CONSTRAINT FOR (u:Usuario) REQUIRE u.email IS UNIQUE;
CREATE CONSTRAINT FOR (p:Pelicula) REQUIRE p.titulo IS UNIQUE;
CREATE CONSTRAINT FOR (g:Genero) REQUIRE g.nombreGenero IS UNIQUE;
CREATE CONSTRAINT FOR (a:Actor) REQUIRE a.nombre IS UNIQUE;
CREATE CONSTRAINT FOR (d:Director) REQUIRE d.nombre IS UNIQUE;

![alt text](<Segundo Proyecto/img/Indice.png>)

4. Documentación de Consultas Implementadas
Se desarrollaron consultas eficientes para responder a los requerimientos de negocio.
Consulta de Películas Recomendadas (Amigos): Encuentra películas vistas por amigos que el usuario aún no ha visto.

## 1. Obtener todas las películas calificadas por un usuario específico con puntuación mayor a 4

**Descripción:** Esta consulta recupera todas las películas que un usuario ha calificado altamente (puntuación mayor a 4). Es útil para identificar las películas que más han gustado a un usuario específico e incluye sus comentarios sobre cada película.

```Bash

MATCH (u:Usuario {email: "user10@ejemplo.com"})-[c:CALIFICÓ]->(p:Pelicula)
WHERE c.puntuacion > 4
RETURN p.titulo, c.puntuacion, c.comentario
```

![alt text](<Segundo Proyecto/img/1img.png>)

## 2. Encontrar las películas que vieron los amigos de un usuario pero que el usuario aún no ha visto

**Descripción:** Esta consulta implementa un sistema de recomendación social. Encuentra películas que los amigos de un usuario han visto pero que el usuario aún no ha visualizado. Es el corazón del sistema de recomendaciones basado en el criterio de amigos.

```Bash

MATCH (u:Usuario {email: "user15@ejemplo.com"})-[:ES_AMIGO_DE]-(amigo:Usuario)
MATCH (amigo)-[:VIO]->(p:Pelicula)
WHERE NOT (u)-[:VIO]->(p)
RETURN DISTINCT p.titulo AS PeliculasRecomendadas
```
![alt text](<Segundo Proyecto/img/2img.png>)

## 3. Obtener el promedio de calificaciones de una película

**Descripción:** Esta consulta calcula el promedio de todas las calificaciones que ha recibido una película específica. Permite evaluar la calidad percibida de una película según la opinión agregada de todos los usuarios.

```Bash
MATCH (u:Usuario)-[c:CALIFICÓ]->(p:Pelicula {titulo: "Pelicula 45"})
RETURN p.titulo, avg(c.puntuacion) AS PromedioCalificacion
```
![alt text](<Segundo Proyecto/img/3img.png>)

## 4. Encontrar los géneros favoritos de un usuario basándose en sus calificaciones

**Descripción:** Esta consulta identifica los 3 géneros que más le gustan a un usuario según el promedio de calificaciones que ha dado a películas de cada género. Incluye información sobre cuántas películas de cada género ha calificado, proporcionando un perfil de preferencias de contenido del usuario.

```Bash
MATCH (u:Usuario {email: "user25@ejemplo.com"})-[c:CALIFICÓ]->(p:Pelicula)-[:PERTENECE_A]->(g:Genero)
RETURN g.nombreGenero AS Genero, avg(c.puntuacion) AS PuntuacionPromedio, count(p) AS PeliculasCalificadas
ORDER BY PuntuacionPromedio DESC, PeliculasCalificadas DESC
LIMIT 3
```
![alt text](<Segundo Proyecto/img/4img.png>)

## 5. Encontrar la ruta más corta de amistad entre dos usuarios

**Descripción:** Esta consulta utiliza el algoritmo de ruta más corta para encontrar el camino mínimo de amistad entre dos usuarios cualquiera en la red social. Demuestra la capacidad de Neo4j para análisis de redes sociales y conexiones entre entidades distantes.

```Bash
MATCH ruta = shortestPath((u1:Usuario {email: "user10@ejemplo.com"})-[:ES_AMIGO_DE*]-(u2:Usuario {email: "user400@ejemplo.com"}))
RETURN ruta
```
![alt text](<Segundo Proyecto/img/5img.png>)

## 6. Listar las películas más populares (con más visualizaciones) de un género específico

**Descripción:** Esta consulta identifica las 5 películas más vistas de un género específico. Es útil para descubrir las películas de mayor popularidad dentro de un género particular, permitiendo identificar tendencias de consumo y éxitos dentro de cada categoría.

```Bash
MATCH (u:Usuario)-[:VIO]->(p:Pelicula)-[:PERTENECE_A]->(g:Genero {nombreGenero: "Ciencia Ficción"})
RETURN p.titulo AS Pelicula, count(u) AS TotalVisualizaciones
ORDER BY TotalVisualizaciones DESC
LIMIT 5
```

![alt text](<Segundo Proyecto/img/6img.png>)

## 7. Calcular rutas más cortas entre usuarios

**Descripción:** Esta consulta calcula los grados de separación ("degrees of separation") entre dos usuarios limitando la búsqueda a un máximo de 6 saltos de amistad. Devuelve la longitud del camino más corto, útil para análisis de conectividad en redes sociales y recomendaciones basadas en proximidad.

```Bash
MATCH ruta = shortestPath(
    (u1:Usuario {email: "user1@ejemplo.com"})-[:ES_AMIGO_DE*1..6]-(u2:Usuario {email: "user300@ejemplo.com"})
)
RETURN u1.nombre AS UsuarioOrigen, u2.nombre AS UsuarioDestino, length(ruta) AS GradosDeSeparacion
```

![alt text](<Segundo Proyecto/img/7img.png>)

## 8. Identificar películas altamente conectadas (con más actores y directores reconocidos)

**Descripción:** Esta consulta identifica las 10 películas con mayor número de conexiones (actores y directores) en el sistema. Películas altamente conectadas representan producciones con elencos grandes y son indicadoras de películas de gran presupuesto o producciones importantes en la base de datos.

```Bash
MATCH (p:Pelicula)
OPTIONAL MATCH (a:Actor)-[:ACTUÓ_EN]->(p)
OPTIONAL MATCH (d:Director)-[:DIRIGIÓ]->(p)
RETURN p.titulo AS Pelicula, 
       count(DISTINCT a) AS TotalActores, 
       count(DISTINCT d) AS TotalDirectores, 
       (count(DISTINCT a) + count(DISTINCT d)) AS ConexionesTotales
ORDER BY ConexionesTotales DESC
LIMIT 10
```

![alt text](<Segundo Proyecto/img/8img.png>)

5. Análisis de Ventajas de Neo4j
El uso de una base de datos de grafos para este sistema ofrece ventajas críticas:
Rendimiento en Traversal: Las consultas que atraviesan múltiples niveles de relaciones (como "amigos de amigos") son órdenes de magnitud más rápidas que en SQL.
Modelado Natural: El esquema coincide directamente con el dominio del problema (redes sociales y conexiones de contenido).
Flexibilidad: Permite añadir nuevas relaciones (como "LE_GUSTA") o propiedades sin necesidad de migraciones de esquema costosas.
