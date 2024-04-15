import psycopg2
from psycopg2 import OperationalError
import random

dbname = 'Proyecto2'
user = 'postgres'
password = 'palocesalope152634'    #Este cambienlo a la contraseña que tengan en la bd
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

        # Consulta SQL para buscar el usuario en la tabla 'personal'
        cur.execute("SELECT COUNT(*) FROM personal WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
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
    
def tabla_cocina():
    
    try: 
        cur = conn.cursor()

        cur.execute("""
        SELECT alimentos.nombre_alimento
        FROM ordenes
        JOIN pedidos ON ordenes.id_orden = pedidos.id_orden
        JOIN alimentos ON pedidos.id_alimento = alimentos.id_alimento
        WHERE alimentos.tipo_alimento = 'plato'
        ORDER BY ordenes.fecha_orden ASC;
        """)

        resultados = cur.fetchall()
        
        # Lista para almacenar los nombres de los alimentos según la cantidad
        alimentos_con_cantidad = []

        # Recorrer los resultados y agregar el nombre del alimento tantas veces como la cantidad indicada
        for nombre_alimento in resultados:
            nombre = nombre_alimento # Obtener el nombre del alimento
            cantidad = CantAlimento(nombre)
            alimentos_con_cantidad.extend([nombre] * CantAlimento(nombre))  # Agregar el nombre según la cantidad

        return alimentos_con_cantidad

    except psycopg2.Error as e:    
        print("Error al mostrar tabla:", e)
        return False 

def tabla_bar():
    
    try: 
        cur = conn.cursor()

        cur.execute("""
        SELECT alimentos.nombre_alimento
        FROM ordenes
        JOIN pedidos ON ordenes.id_orden = pedidos.id_orden
        JOIN alimentos ON pedidos.id_alimento = alimentos.id_alimento
        WHERE alimentos.tipo_alimento = 'bebida'
        ORDER BY ordenes.fecha_orden ASC;
        """)

        resultados = cur.fetchall()
        
        # Lista para almacenar los nombres de los alimentos según la cantidad
        alimentos_con_cantidad = []

        # Recorrer los resultados y agregar el nombre del alimento tantas veces como la cantidad indicada
        for nombre_alimento in resultados:
            nombre = nombre_alimento  
            cantidad = CantAlimento(nombre)
            alimentos_con_cantidad.extend([nombre] * CantAlimento(nombre))  

        return alimentos_con_cantidad

    except psycopg2.Error as e:    
        print("Error al mostrar tabla:", e)
        return False 

def CantAlimento(nombre_alimento):
    try:
        cur = conn.cursor()

        cur.execute("""
        SELECT SUM(cantidad)
        FROM pedidos
        JOIN alimentos ON pedidos.id_alimento = alimentos.id_alimento
        WHERE alimentos.nombre_alimento = %s;
        """, (nombre_alimento,))

        cantidad = cur.fetchone()[0]  # Obtener la cantidad del alimento

        return cantidad if cantidad else 0

    except psycopg2.Error as e:
        print("Error al obtener la cantidad del alimento:", e)
        return 0