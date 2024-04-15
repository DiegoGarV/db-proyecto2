import psycopg2
from psycopg2 import OperationalError
import random

dbname = 'restaurante'
user = 'postgres'
password = 'Basedatos1'    #Este cambienlo a la contraseña que tengan en la bd
host = 'localhost'
port = '5432'

try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Conexión exitosa a la base de datos")

    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print("Versión de PostgreSQL:", version)

except OperationalError as e:
    print("Error al conectar a la base de datos:", e)

def verificar_Usuario(usuario, contraseña):
    try:
        cur = conn.cursor()

        usuario = usuario.lower()
        # Consulta SQL para buscar el usuario en la tabla 'personal'
        cur.execute("SELECT COUNT(*) FROM personal WHERE LOWER(usuario) = %s AND contraseña = %s", (usuario, contraseña))
        result = cur.fetchone()

        # Si el resultado es 1 (existe una coincidencia), las credenciales son válidas
        if result[0] == 1:
            return True
        else:
            return False

    except psycopg2.Error as e:
        print("Error al verificar las credenciales:", e)
        return False
    

def agregar_Usuario(nombre, pos, usuario, contraseña):
    try:
        cur = conn.cursor()

        # Verificar si el usuario ya existe en la base de datos
        cur.execute("SELECT COUNT(*) FROM personal WHERE LOWER(usuario) = %s", (usuario.lower(),))
        count = cur.fetchone()[0]
        if count > 0:
            return False

        # Generar un id_personal único
        id_personal = random.randint(1, 200)
        while True:
            cur.execute("SELECT COUNT(*) FROM personal WHERE id_personal = %s", (id_personal,))
            count = cur.fetchone()[0]
            if count == 0:
                break
            id_personal = random.randint(1, 200)  # Intentar con otro id_personal único

        # Insertar el nuevo usuario en la tabla Personal
        cur.execute("INSERT INTO personal (id_personal, nombre_personal, posicion_laboral, usuario, contraseña) VALUES (%s, %s, %s, %s, %s)",
                    (id_personal, nombre, pos, usuario, contraseña))

        conn.commit()
        print("Usuario agregado correctamente con id_personal:", id_personal)
        return True

    except psycopg2.Error as e:
        print("Error al agregar usuario:", e)
        return False
    
def tabla():
    
    try: 
        cur = conn.cursor()

        cur.execute("""
        SELECT alimentos.nombre_alimento
        FROM ordenes
        JOIN pedidos ON ordenes.id_orden = pedidos.id_orden
        JOIN alimentos ON pedidos.id_alimento = alimentos.id_alimento
        ORDER BY ordenes.fecha_orden ASC;
        """)

        resultados = cur.fetchall()
        return resultados


    except psycopg2.Error as e:    
        print("Error al agregar usuario:", e)
        return False 
