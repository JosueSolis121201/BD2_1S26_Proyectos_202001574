import csv
import random
from datetime import date, timedelta

# Generadores básicos
nombres_base = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Elena", "Pedro", "Lucia", "Diego", "Sofia"]
apellidos_base = ["Perez", "Gomez", "Lopez", "Garcia", "Rodriguez", "Martinez", "Hernandez", "Gonzalez"]
paises = ["Guatemala", "Mexico", "Colombia", "Argentina", "España", "Chile", "Peru"]
generos_lista = ["Acción", "Comedia", "Drama", "Ciencia Ficción", "Terror", "Romance", "Documental", "Fantasía", "Suspenso", "Animación", "Aventura", "Misterio", "Crimen", "Musical", "Historia"]

def random_date(start_year, end_year):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# 1. Usuarios (500)
usuarios = []
with open('usuarios.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['email', 'nombre', 'edad', 'pais'])
    for i in range(1, 501):
        nombre = f"{random.choice(nombres_base)} {random.choice(apellidos_base)}"
        email = f"user{i}@ejemplo.com"
        edad = random.randint(18, 65)
        pais = random.choice(paises)
        usuarios.append(email)
        writer.writerow([email, nombre, edad, pais])

# 2. Peliculas (200)
peliculas = []
with open('peliculas.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['titulo', 'anoLanzamiento', 'duracion', 'sinopsis'])
    for i in range(1, 201):
        titulo = f"Pelicula {i}"
        ano = random.randint(1990, 2025)
        duracion = random.randint(90, 180)
        sinopsis = f"Una gran aventura número {i}."
        peliculas.append(titulo)
        writer.writerow([titulo, ano, duracion, sinopsis])

# 3. Generos (15)
with open('generos.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['nombreGenero', 'descripcion'])
    for g in generos_lista:
        writer.writerow([g, f"Películas de la categoría {g}"])

# 4. Actores (100)
actores = []
with open('actores.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['nombre', 'fechaNacimiento', 'nacionalidad'])
    for i in range(1, 101):
        nombre = f"Actor {random.choice(nombres_base)} {i}"
        fecha = random_date(1950, 2000).isoformat()
        nac = random.choice(paises)
        actores.append(nombre)
        writer.writerow([nombre, fecha, nac])

# 5. Directores (50)
directores = []
with open('directores.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['nombre', 'fechaNacimiento', 'nacionalidad'])
    for i in range(1, 51):
        nombre = f"Director {random.choice(apellidos_base)} {i}"
        fecha = random_date(1940, 1980).isoformat()
        nac = random.choice(paises)
        directores.append(nombre)
        writer.writerow([nombre, fecha, nac])

# 6. Relaciones: CALIFICÓ (Usuarios -> Peliculas)
with open('califico.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['email', 'titulo', 'puntuacion', 'fecha', 'comentario'])
    for u in usuarios:
        # Cada usuario califica entre 3 y 10 peliculas
        for _ in range(random.randint(3, 10)):
            p = random.choice(peliculas)
            puntuacion = random.randint(1, 5)
            fecha = random_date(2023, 2026).isoformat()
            comentario = f"Comentario sobre {p}"
            writer.writerow([u, p, puntuacion, fecha, comentario])

print("¡Archivos CSV generados con éxito!")