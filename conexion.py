import psycopg2
from psycopg2 import OperationalError
import random


dbname = 'Proyecto2'
user = 'postgres'
password = 'admin'    #Este cambienlo a la contraseña que tengan en la bd
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

        usuario = usuario
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

        contraseña = encriptacion(contraseña)
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
        
        if pos.lower()=='mesero':
            cur.execute("INSERT INTO meseros (id_personal, id_area) VALUES (%s, %s)",
                    (id_personal, random.randint(1, 5),))

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
                        SUM(p.cantidad) AS cantidad_pedidos
                        FROM pedidos p
                        JOIN alimentos a ON p.id_alimento = a.id_alimento
                        JOIN ordenes o ON p.id_orden = o.id_orden
                        WHERE a.tipo_alimento ILIKE 'plato' 
                        AND o.fecha_apertura BETWEEN %s AND %s
                        AND o.fecha_cierre IS NOT NULL
                        GROUP BY a.nombre_alimento
                        ORDER BY SUM(p.cantidad) DESC; """, (fecha_inicio, fecha_final))
        platos_pedidos = cur.fetchall()
        #print(platos_pedidos)
        return platos_pedidos
    
    except psycopg2.Error as e:
        print("Error al obtener el plato más pedido:", e)
        return None
    
def horarios_altos(fecha_inicio, fecha_final):
    try:
        cur = conn.cursor()

        cur.execute(""" SELECT TO_CHAR(DATE_TRUNC('hour', o.fecha_apertura), 'HH24:MI') AS hora_truncada,
                        SUM(p.cantidad) AS cantidad_ordenes
                        FROM ordenes o
                        JOIN pedidos p ON o.id_orden = p.id_orden
                        JOIN alimentos a ON p.id_alimento = a.id_alimento
                        WHERE o.fecha_apertura BETWEEN %s AND %s
                        GROUP BY DATE_TRUNC('hour', o.fecha_apertura)
                        ORDER BY SUM(p.cantidad) DESC; """, (fecha_inicio, fecha_final))
        horas_altas = cur.fetchall()
        #print(horas_altas)
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
    
def PromedioComida(fecha_inicio, fecha_fin):
    try: 
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                mesas.cantidad_personas,
                AVG(EXTRACT(EPOCH FROM (ordenes.fecha_cierre - ordenes.fecha_apertura)) / 60) AS promedio_minutos
            FROM 
                ordenes
            JOIN 
                mesas ON ordenes.id_mesa = mesas.id_mesa
            WHERE 
                ordenes.fecha_apertura BETWEEN %s AND %s 
                AND ordenes.fecha_cierre IS NOT NULL
            GROUP BY 
                mesas.cantidad_personas;
        """, (fecha_inicio, fecha_fin))
        
        resultados = cur.fetchall()
        return resultados
        

    except psycopg2.Error as e: 
        print("Error al ejecutar el query", e)
        return 0
    
def ver_pos(usuario):
    try:
        cur = conn.cursor()

        cur.execute(""" SELECT posicion_laboral
                        FROM personal
                        WHERE LOWER(usuario) = %s;
                    """, (usuario.lower(),))
        posicion = cur.fetchall()
        #print(posicion)
        return posicion

    except psycopg2.Error as e:
        print(f"Error al obtener la posición laboral de {usuario}:", e)
        return None

def crear_pedido(mesa, nit, nombre, direccion, usuario):
    try:
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM clientes WHERE nit_cliente = %s", (nit,))
        existe_cliente = cur.fetchone()[0]

        if existe_cliente > 0:
            pass
        else:
            cur.execute("""INSERT INTO clientes (nit_cliente, nombre_cliente, direccion_cliente) 
                           VALUES (%s, %s, %s)""", (nit, nombre, direccion))

        cur.execute(""" SELECT id_personal
                        FROM personal
                        WHERE LOWER(usuario) = %s;
                    """, (usuario.lower(),))
        id_personal = cur.fetchone()

        id_orden = random.randint(1, 9999)
        id_encuesta = random.randint(1, 9999)
        while True:
            cur.execute("SELECT COUNT(*) FROM ordenes WHERE id_orden = %s", (id_orden,))
            count = cur.fetchone()[0]
            if count == 0:
                break
            id_orden = random.randint(1, 9999)
        
        while True:
            cur.execute("SELECT COUNT(*) FROM encuestas_servicio WHERE id_encuesta = %s", (id_encuesta,))
            count = cur.fetchone()[0]
            if count == 0:
                break
            id_encuesta = random.randint(1, 9999)

        cur.execute("""INSERT INTO encuestas_servicio (id_encuesta, puntuacion_amabilidad, puntuacion_exactitud) 
                       VALUES (%s, %s, %s);""",
                    (id_encuesta, random.randint(1, 5), random.randint(1, 5),))

        cur.execute("""INSERT INTO ordenes (id_orden, estado_orden, total_orden, porcentaje_propina, id_mesa, nit_cliente, id_personal, id_encuesta, fecha_apertura, fecha_cierre) 
                       VALUES (%s, 'abierto', NULL, 15, %s, %s, %s, %s, CURRENT_TIMESTAMP, NULL);""",
                    (id_orden, mesa, nit, id_personal, id_encuesta))

        conn.commit()
        print("Orden agregada correctamente con id_orden:", id_orden)
        return True

    except psycopg2.Error as e:
        print("Error al agregar usuario:", e)
        return False

def obtener_pedidos():
    try:
        cur = conn.cursor()

        cur.execute("""select * from ordenes;""")
        pedidos = cur.fetchall()
        #print(pedidos)
        return pedidos

    except psycopg2.Error as e:
        print("Error al obtener las ordenes:", e)
        return None
    
def obtener_menu():
    try:
        cur = conn.cursor()

        cur.execute("""select * from alimentos;""")
        menu = cur.fetchall()
        #print(menu)
        return menu

    except psycopg2.Error as e:
        print("Error al obtener el menu:", e)
        return None
    
def obtener_datos_pedido():
    try:
        cur = conn.cursor()
        cur.execute("""
        SELECT 
            alimentos.nombre_alimento AS nombre_alimento,
            alimentos.precio_alimento AS precio_unitario,
            pedidos.cantidad AS cantidad,
            ROUND(CAST(alimentos.precio_alimento AS NUMERIC) * CAST(pedidos.cantidad AS NUMERIC), 2) AS subtotal_alimento,
            ordenes.porcentaje_propina AS porcentaje_propina
        FROM 
            pedidos
        JOIN 
            alimentos ON pedidos.id_alimento = alimentos.id_alimento
        JOIN 
            ordenes ON pedidos.id_orden = ordenes.id_orden
        WHERE 
    pedidos.id_orden = 1;

                    """)
        
        pedido = cur.fetchall()
        return pedido
    except psycopg2.Error as e:
        print("Error al obtener el menu:", e)
        return None

def obtener_subtotal_pedido():
    try:
        cur = conn.cursor()
        cur.execute("""
        SELECT 
            SUM(subtotal_alimento) AS subtotal_total
        FROM (
            SELECT 
                ROUND(CAST(alimentos.precio_alimento as numeric) * CAST(pedidos.cantidad AS NUMERIC), 2) AS subtotal_alimento
            FROM 
                pedidos
            JOIN 
                alimentos ON pedidos.id_alimento = alimentos.id_alimento
            WHERE 
                pedidos.id_orden = 1
        ) AS subtotales;
                    
                    """)
        
        subtotal = cur.fetchall()
        return subtotal
    except psycopg2.Error as e:
        print("Error al obtener el menu:", e)
        return None

def obtener_propina_pedido():
    try:
        cur = conn.cursor()
        cur.execute("""
        SELECT porcentaje_propina
        FROM ordenes
        WHERE id_orden = 1;                    
                    """)
        
        propina = cur.fetchall()
        return propina
    except psycopg2.Error as e:
        print("Error al obtener el menu:", e)
        return None
    
def obtener_total_pedido():
    try:
        cur = conn.cursor()
        cur.execute("""
        SELECT 
        ((SELECT ROUND(SUM(alimentos.precio_alimento * pedidos.cantidad)) 
        FROM pedidos 
        JOIN alimentos ON pedidos.id_alimento = alimentos.id_alimento
        WHERE pedidos.id_orden = 1)
        +
        (SELECT porcentaje_propina
        FROM ordenes
        WHERE id_orden = 1)
        ) AS total_con_propina;
                    
                    """)
        
        propina = cur.fetchall()
        return propina
    except psycopg2.Error as e:
        print("Error al obtener el menu:", e)
        return None
    
def QuejasPlato(fecha_inicio, fecha_fin):
    try: 
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                m.nombre_plato AS plato,
                COUNT(q.id_queja) AS total_quejas
            FROM 
                quejas q
            JOIN 
                menu m ON q.id_plato = m.id_plato
            WHERE 
                q.fecha_queja BETWEEN %s AND %s
            GROUP BY 
                m.nombre_plato;
        """, (fecha_inicio, fecha_fin))
        
        resultados = cur.fetchall()
        return resultados

    except psycopg2.Error as e: 
        print("Error al ejecutar el query", e)
        return None

def Eficiencia(fecha_inicio, fecha_fin):
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                p.nombre_personal AS persona,
                COUNT(e.id_encuesta) AS total_encuestas,
                AVG(e.calificacion) AS promedio_calificacion
            FROM 
                encuestas e
            JOIN 
                personal p ON e.id_personal = p.id_personal
            WHERE 
                e.fecha_encuesta BETWEEN %s AND %s
            GROUP BY 
                p.nombre_personal;
        """, (fecha_inicio, fecha_fin))
        
        resultados = cur.fetchall()
        return resultados

    except psycopg2.Error as e:
        print("Error al ejecutar el query", e)
        return None