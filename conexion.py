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
        contraseña = encriptacion(contraseña)

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

        #Encripta la contraseña
        contraseña = encriptacion(contraseña)

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

def encriptacion(contraseña):
    diccionario = {' ':0}
    diccionario.update({chr(i + ord('A')): i + 1 for i in range(26)})
    diccionario.update({str(i): i + 27 for i in range(10)})
    diccionario.update({'_':37})
    diccionario.update({'-':38})
    p=97
    q=89
    n=p*q
    e=13

    def buscarValor(letra):
        for llave, value in diccionario.items():
            if llave == letra:
                return str(value).zfill(2)
        return "Esta letra no está en el diccionario"
    
    contraseña=contraseña.upper()
    palabraNumero = []
    for i in range(0, len(contraseña), 2):
        num1 = buscarValor(contraseña[i])
        num2 = buscarValor(contraseña[i + 1]) if i + 1 < len(contraseña) else 00
        palabraNumero.append(num1+num2)

    palabraEncriptada = []
    for i in palabraNumero:
        i = int(i)
        x = (i**e)%n
        x = str(x).zfill(4)
        palabraEncriptada.append(x)

    contraseña_encriptada = ''.join(palabraEncriptada)
    return contraseña_encriptada


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