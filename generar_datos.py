from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, SimpleStatement
from faker import Faker
import random
from datetime import datetime, timedelta

# 1. Configuración inicial
print("Conectando al clúster de Cassandra...")
cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect('reservadb')
fake = Faker('es_MX')

# 2. Preparar datos base
espacios = [f"Sala {i}" for i in range(1, 21)] + [f"Escritorio {i}" for i in range(1, 51)]
estados = ['Confirmada', 'Completada', 'Cancelada']
usuarios = [fake.email() for _ in range(500)] # 500 usuarios ficticios

# 3. Preparar las consultas de inserción
insert_disp = session.prepare("""
    INSERT INTO disponibilidad_espacio_fecha (espacio_nombre, fecha, hora_inicio, hora_fin, estado) 
    VALUES (?, ?, ?, ?, ?)
""")

insert_hist = session.prepare("""
    INSERT INTO historial_usuario (email_usuario, fecha, hora_inicio, espacio_nombre, estado) 
    VALUES (?, ?, ?, ?, ?)
""")

insert_ocup = session.prepare("""
    INSERT INTO ocupacion_espacio_mes (espacio_nombre, mes_anio, fecha, hora_inicio, usuario_email, estado) 
    VALUES (?, ?, ?, ?, ?, ?)
""")

# 4. Generación e inserción por lotes (Batch Writes)
total_reservas = 100000
batch_size = 30 # Agrupamos de 30 en 30 reservas para no saturar la memoria
reservas_creadas = 0

print(f"Iniciando la inserción de {total_reservas} reservas usando Batch Writes...")

while reservas_creadas < total_reservas:
    batch = BatchStatement()
    
    for _ in range(batch_size):
        if reservas_creadas >= total_reservas:
            break
            
        # Generar datos aleatorios para la reserva
        espacio = random.choice(espacios)
        usuario = random.choice(usuarios)
        estado = random.choice(estados)
        
        # Fecha aleatoria en el año 2026
        fecha_obj = fake.date_between_dates(date_start=datetime(2026, 1, 1), date_end=datetime(2026, 12, 31))
        mes_anio = fecha_obj.strftime("%Y-%m")
        fecha_str = fecha_obj.strftime("%Y-%m-%d")
        
        # Horarios aleatorios
        hora_inicio_obj = datetime.strptime(f"{random.randint(8, 18)}:00", "%H:%M")
        hora_fin_obj = hora_inicio_obj + timedelta(hours=random.randint(1, 4))
        hora_inicio_str = hora_inicio_obj.strftime("%H:%M:%S")
        hora_fin_str = hora_fin_obj.strftime("%H:%M:%S")
        
        # Agregar al batch las 3 inserciones (denormalización)
        batch.add(insert_disp, (espacio, fecha_str, hora_inicio_str, hora_fin_str, estado))
        batch.add(insert_hist, (usuario, fecha_str, hora_inicio_str, espacio, estado))
        batch.add(insert_ocup, (espacio, mes_anio, fecha_str, hora_inicio_str, usuario, estado))
        
        reservas_creadas += 1

    # Ejecutar el lote
    session.execute(batch)
    
    # Imprimir progreso cada 5,000 registros
    if reservas_creadas % 5000 == 0:
        print(f"Progreso: {reservas_creadas} / {total_reservas} reservas insertadas...")

print("¡Carga masiva completada con éxito!")