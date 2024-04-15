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
    
def tabla_cocina():
    try: 
        cur = conn.cursor()

        cur.execute("""
        SELECT alimentos.nombre_alimento
        FROM ordenes
        JOIN pedidos ON ordenes.id_orden = pedidos.id_orden
        JOIN alimentos ON pedidos.id_alimento = alimentos.id_alimento
        WHERE alimentos.tipo_alimento = 'plato'
        ORDER BY ordenes.fecha_apertura ASC;
        """)

        resultados = cur.fetchall()
        
        
        alimentos_con_cantidad = []

      
        for nombre_alimento in resultados:
            nombre = nombre_alimento 
            cantidad = CantAlimento(nombre)
            alimentos_con_cantidad.extend([nombre] * CantAlimento(nombre))  

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
        ORDER BY ordenes.fecha_apertura ASC;
        """)

        resultados = cur.fetchall()
        
       
        alimentos_con_cantidad = []

        
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
    if len(contraseña) % 2 != 0:
        contraseña += ' '
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

        cantidad = cur.fetchone()[0]  

        return cantidad if cantidad else 0

    except psycopg2.Error as e:
        print("Error al obtener la cantidad del alimento:", e)
        return 0
    
def plato_mas_pedidos(fecha_inicio, fecha_final):
    try:
        cur = conn.cursor()

        cur.execute(""" SELECT a.nombre_alimento AS plato,
        COUNT(*) AS cantidad_pedidos
        FROM pedidos p
        JOIN alimentos a ON p.id_alimento = a.id_alimento
        JOIN ordenes o ON p.id_orden = o.id_orden
        WHERE a.tipo_alimento ILIKE 'plato'
        AND o.fecha_orden BETWEEN %s AND %s
        GROUP BY a.nombre_alimento
        ORDER BY COUNT(*) DESC; """, (fecha_inicio, fecha_final))
        platos_pedidos = cur.fetchall()
        return platos_pedidos
    
    except psycopg2.Error:
        return None
    
    
def horarios_altos(fecha_inicio, fecha_final):
    try:
        cur = conn.cursor()

        cur.execute(""" SELECT DATE_TRUNC('hour', o.fecha_orden) AS hora,
        COUNT(*) AS cantidad_ordenes
        FROM ordenes o
        WHERE o.fecha_orden BETWEEN '2024-01-01' AND '2024-03-31' -- Rango de fechas
        GROUP BY DATE_TRUNC('hour', o.fecha_orden)
        ORDER BY COUNT(*) DESC; """, (fecha_inicio, fecha_final))
        horas_altas = cur.fetchall()
        return horas_altas
    
    except psycopg2.Error as e:
        return None


    
def QuejasXCliente(fecha_inicio, fecha_fin):

    
    try: 
    
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                p.nombre_personal AS persona,
                COUNT(q.id_queja) AS total_quejas
            FROM 
                quejas q
            JOIN 
                personal p ON q.id_personal = p.id_personal
            WHERE 
                q.fecha_queja BETWEEN %s AND %s
            GROUP BY 
                p.nombre_personal;
    """, (fecha_inicio, fecha_fin))
        
        resultados = cur.fetchall()
        return resultados
        

    except psycopg2.Error as e: 
        print("Error al ejecutar el query", e)
        return 0