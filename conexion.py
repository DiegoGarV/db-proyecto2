import psycopg2

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

    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Versión de PostgreSQL:", version)

    cur.close()
    conn.close()

except psycopg2.Error as e:
    print("Error al conectar a la base de datos:", e)
