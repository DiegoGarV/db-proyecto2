import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import conexion as con
from datetime import datetime


#---------------------- Pantalla Log In ----------------------
window = tk.Tk()
window.title("Inicio de Sesión")
window.geometry("1000x500")
window.resizable(0,0)
window.protocol("WM_DELETE_WINDOW", quit)

#---------------------- Pantalla Sign In ----------------------
signin = tk.Toplevel(window)
signin.title("Registro")
signin.geometry("1000x500")
signin.withdraw()
signin.resizable(0,0)
signin.protocol("WM_DELETE_WINDOW", quit)


#---------------------- Pantalla Menu ----------------------
main_menu_window = tk.Toplevel(window)
main_menu_window.title("Menú Principal")
main_menu_window.geometry("1000x500")
main_menu_window.withdraw()
main_menu_window.resizable(0,0)
main_menu_window.protocol("WM_DELETE_WINDOW", quit)

#---------------------- Pantalla Cocina ----------------------
cocina = tk.Toplevel()
cocina.title("Cocina")
cocina.geometry("1000x500")
cocina.resizable (0,0)
cocina.withdraw()
cocina.protocol("WM_DELETE_WINDOW", quit)
Kitchentree = ttk.Treeview(cocina, columns=("Nombre", "Num"))
Kitchentree.heading("Nombre", text="Nombre plato")
Kitchentree.heading("Num", text="Número cola")
Kitchentree.column("#0", width=200)  
Kitchentree.pack(padx=10, pady=10)

#---------------------- Pantalla Bar ----------------------
bar = tk.Toplevel()
bar.title("Bar")
bar.geometry("1000x500")
bar.resizable(0,0)
bar.withdraw()
bar.protocol("WM_DELETE_WINDOW", quit)
Bartree = ttk.Treeview(bar, columns=("Nombre", "Num"))
Bartree.heading("Nombre", text="Nombre bebida")
Bartree.heading("Num", text="Número cola")
Bartree.column("#0", width=0)
Bartree.pack(padx=10, pady=10)

#---------------------- Pantalla Menu Reportes ----------------------
reportes = tk.Toplevel()
reportes.title("Reportes")
reportes.geometry("1000x500")
reportes.resizable(0,0)
reportes.withdraw()
reportes.protocol("WM_DELETE_WINDOW", quit)

#---------------------- Pantallas Reportes ----------------------
r1 = tk.Toplevel()
r2 = tk.Toplevel()
r3 = tk.Toplevel()
r4 = tk.Toplevel()
r5 = tk.Toplevel()
r6 = tk.Toplevel()

r1.title("Platos mas pedidos")
r2.title("Horario con mas pedidos")
r3.title("Tiempo promedio")
r4.title("Reporte de quejas")
r5.title("Quejas por plato")
r6.title("Reporte de eficiencia")

r1.geometry("1000x500")
r2.geometry("1000x500")
r3.geometry("1000x500")
r4.geometry("1000x500")
r5.geometry("1000x500")
r6.geometry("1000x500")

r1.resizable(0,0)
r2.resizable(0,0)
r3.resizable(0,0)
r4.resizable(0,0)
r5.resizable(0,0)
r6.resizable(0,0)

r1.withdraw()
r2.withdraw()
r3.withdraw()
r4.withdraw()
r5.withdraw()
r6.withdraw()

r1.protocol("WM_DELETE_WINDOW", quit)
r2.protocol("WM_DELETE_WINDOW", quit)
r3.protocol("WM_DELETE_WINDOW", quit)
r4.protocol("WM_DELETE_WINDOW", quit)
r5.protocol("WM_DELETE_WINDOW", quit)
r6.protocol("WM_DELETE_WINDOW", quit)

R1tree = ttk.Treeview(r1, columns=("Plato", "Cantidad de Pedidos"))
R1tree.heading("Plato", text="Nombre del plato")
R1tree.heading("Cantidad de Pedidos", text="Cantidad de Pedidos")
R1tree.column("#0", width=0)
R1tree.pack(padx=10, pady=10)

R2tree = ttk.Treeview(r2, columns=("Hora", "Cantidad de Pedidos"))
R2tree.heading("Hora", text="Hora")
R2tree.heading("Cantidad de Pedidos", text="Cantidad de Pedidos")
R2tree.column("#0", width=0)
R2tree.pack(padx=10, pady=10)

R3tree = ttk.Treeview(r3, columns=("Cantidad Personas"))
R3tree.heading("#0", text="Promedio de Tiempo")
R3tree.column("#0", width=200)
R3tree.pack(padx=10, pady=10)

R4tree = ttk.Treeview(r4, columns=("Nombre Cliente"))
R4tree.heading("#0", text="Quejas")
R4tree.column("#0", width=200)
R4tree.pack(padx=10, pady=10)

#---------------------- Funciones --------------------------
def R1(): 
    fecha_inicio = entry_fecha_inicioR1.get()
    fecha_final=entry_fecha_finR1.get()

    fecha1 = datetime.strptime(fecha_inicio, "%Y/%m/%d %H:%M")
    fecha2 = datetime.strptime(fecha_final, "%Y/%m/%d %H:%M")

    if fecha1 <= fecha2:
        resultados = con.plato_mas_pedidos(fecha_inicio, fecha_final)
        
        if resultados is not None and resultados:
            for item in R1tree.get_children():
                R1tree.delete(item)

            contador = 0
            for resultado in resultados:
                contador = contador + 1
                R1tree.insert("", "end", values=( resultado))
        else:
            messagebox.showerror("Sin datos", "Parece que no hay datos entre esas fechas.")
    else:
        messagebox.showerror("Error al ingresar las fechas", "La fecha inicial no puede ser posterior a la fecha final.")

def R2(): 
    fecha_inicio = entry_fecha_inicioR2.get()
    fecha_final=entry_fecha_finR2.get()

    fecha1 = datetime.strptime(fecha_inicio, "%Y/%m/%d %H:%M")
    fecha2 = datetime.strptime(fecha_final, "%Y/%m/%d %H:%M")

    if fecha1 <= fecha2:
        resultados = con.horarios_altos(fecha_inicio, fecha_final)
        
        if resultados is not None and resultados:
            for item in R1tree.get_children():
                R1tree.delete(item)

            contador = 0
            for resultado in resultados:
                contador = contador + 1
                R2tree.insert("", "end", values=( resultado))
        else:
            messagebox.showerror("Sin datos", "Parece que no hay datos entre esas fechas.")
    else:
        messagebox.showerror("Error al ingresar las fechas", "La fecha inicial no puede ser posterior a la fecha final.")

def R3():
    con.PromedioComida(fecha_inicio=entry_fecha_inicioR3.get(), fecha_fin=entry_fecha_finR3.get())
    
    resultados = con.PromedioComida(fecha_inicio=entry_fecha_inicioR3.get(), fecha_fin=entry_fecha_finR3.get())

    for item in R3tree.get_children():
        R3tree.delete(item)
    
    contador = 0
    for resultado in resultados: 
        contador = contador +1
        R3tree.insert("", "end", values=(resultado))

def R4(): 
    con.QuejasXCliente(fecha_inicio=entry_fecha_inicioR4.get(), fecha_fin=entry_fecha_finR4.get())

    resultados = con.QuejasXCliente(fecha_inicio=entry_fecha_inicioR4.get(), fecha_fin=entry_fecha_finR4.get())

    for item in R4tree.get_children():
        R4tree.delete(item)

    contador = 0
    for resultado in resultados:
        contador = contador + 1
        R4tree.insert("", "end", values=( resultado))

def Bar_marcar_listo():
    try:
        row = Bartree.focus()
        Bartree.delete(row)
    except: 
        messagebox.showerror("Error al marcar como listo", "Porfavor seleccione un registro")
        return False 

def PantBar():
    main_menu_window.withdraw()
    bar.deiconify()

    con.tabla_bar()
    
    resultados = con.tabla_bar()


    for item in Bartree.get_children():
        Bartree.delete(item)

    contador = 0
    for resultado in resultados:
        contador = contador + 1
        Bartree.insert("", "end", values=(contador, resultado[0],))

def Cocina_marcar_listo():
    try:
        row = Kitchentree.focus()
        Kitchentree.delete(row)
    except: 
        messagebox.showerror("Error al marcar como listo", "Porfavor seleccione un registro")
        return False 
    
def PantCocina():
    main_menu_window.withdraw()
    cocina.deiconify()

    con.tabla_cocina()
    resultados = con.tabla_cocina()


    for item in Kitchentree.get_children():
        Kitchentree.delete(item)

    contador = 0
    for resultado in resultados:
        contador = contador + 1
        Kitchentree.insert("", "end", values=(contador, resultado[0],))
        
def signinWindow():
    signin.deiconify()
    window.withdraw()

def Signin(): 
    name = entry_name_sn.get()
    jobPos = entry_jobPos_sn.get()
    username = entry_usuario_sn.get()
    password = entry_password_sn.get()
    
    #Añade un usuario nuevo
    if con.agregar_Usuario(name, jobPos, username, password):
        messagebox.showinfo("Registro exitoso", "Usuario agregado correctamente")
        open_main_menu()  
    else:
        messagebox.showerror("Error al registrar usuario", "Hubo un problema al agregar el usuario")
    
def login(): 
    username = entry_username_w.get()
    password = entry_password_w.get()
    
    if con.verificar_Usuario(username, password):
        open_main_menu()        
    else:
        messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos")
        
def Reportes():
    main_menu_window.withdraw()
    r1.withdraw()
    r2.withdraw()
    r3.withdraw()
    r4.withdraw()
    r5.withdraw()
    r6.withdraw()
    reportes.deiconify()

def open_main_menu(): 
    reportes.withdraw()
    bar.withdraw()
    cocina.withdraw()
    window.withdraw()
    main_menu_window.deiconify()
    
def return_to_login():
    signin.withdraw()
    main_menu_window.withdraw()
    window.deiconify()

def r1_load():
    reportes.withdraw()
    r1.deiconify()

def r2_load():
    reportes.withdraw()
    r2.deiconify()

def r3_load():
    reportes.withdraw()
    r3.deiconify()

def r4_load():
    reportes.withdraw()
    r4.deiconify()

def r5_load():
    reportes.withdraw()
    r5.deiconify()

def r6_load():
    reportes.withdraw()
    r6.deiconify()

#----------------------------- Log In -----------------------------------
label_username_w = tk.Label(window, text="Usuario:")
label_username_w.place(x = 440, y = 150)
entry_username_w = tk.Entry(window)
entry_username_w.place(x = 440, y = 170)

label_password_w = tk.Label(window, text="Contraseña:")
label_password_w.place(x=440, y = 190)
entry_password_w = tk.Entry(window, show= "*")
entry_password_w.place(x=440, y = 210)


btn_login = tk.Button(window, text="Iniciar Sesión", command=login)
btn_login.place(x= 420, y = 250)


btn_irSignin = tk.Button(window, text = "Registrarse", command=signinWindow)
btn_irSignin.place(x = 510, y = 250)

#----------------------------- Sign In -----------------------------------
label_name_sn = tk.Label(signin, text="Nombre completo:")
label_name_sn.pack(pady=5)
entry_name_sn = tk.Entry(signin)
entry_name_sn.pack(pady=5)

label_jobPos_sn = tk.Label(signin, text="Puesto de trabajo:")
label_jobPos_sn.pack(pady=5)
entry_jobPos_sn = tk.Entry(signin)
entry_jobPos_sn.pack(pady=5)

label_usuario_sn = tk.Label(signin, text="Nombre de usuario:")
label_usuario_sn.pack(pady=5)
entry_usuario_sn = tk.Entry(signin)
entry_usuario_sn.pack(pady=5)

label_password_sn = tk.Label(signin, text="Crear Contraseña:")
label_password_sn.pack(pady=5)
entry_password_sn = tk.Entry(signin, show= "*")
entry_password_sn.pack(pady=5)

label_Confpassword_sn = tk.Label(signin, text="Confirmar Contraseña:")
label_Confpassword_sn.pack(pady=5)
entry_Confpassword_sn = tk.Entry(signin, show= "*")
entry_Confpassword_sn.pack(pady=5)

btn_irSignin = tk.Button(signin, text = "Registrarse", command=Signin)
btn_irSignin.place(x = 420, y = 305)


btn_exit = tk.Button(signin, text="Regresar", command=return_to_login)
btn_exit.place(x = 520, y = 305)

#----------------------------- Menu -----------------------------------
lbl_menu = tk.Label(main_menu_window, text="¡Bienvenido al Menú Principal!")
lbl_menu.pack(pady=10)
lbl_menu.config(font=("arial", 20, "bold"))

btn_exit = tk.Button(main_menu_window, text="Regresar", command=return_to_login)
btn_exit.place(x = 460, y = 250)
btn_exit.config(font=("Arial", 10, "bold"))


btn_cocina = tk.Button(main_menu_window, text="  Cocina ", command=PantCocina)
btn_cocina.place(x = 510, y = 150)
btn_cocina.config(font=("Arial", 10, "bold"))


btn_bar = tk.Button(main_menu_window, text="    Bar    ", command=PantBar)
btn_bar.place(x = 410, y = 200)
btn_bar.config(font=("Arial", 10, "bold"))

btn_pedido = tk.Button(main_menu_window, text=" Pedido ")
btn_pedido.place(x = 410, y = 150)
btn_pedido.config(font=("Arial", 10, "bold"))

btn_registros = tk.Button(main_menu_window, text="Reportes", command=Reportes)
btn_registros.place(x = 510, y = 200)
btn_registros.config(font=("Arial", 10, "bold"))

#----------------------------- Reportes -----------------------------------
btn_R1 = tk.Button(reportes, text="Platos más pedidos", command=r1_load, width=20, height=2, font=("Arial", 10, "bold"))
btn_R1.place(x=350, y=100)

btn_R2 = tk.Button(reportes, text="Horas pico", command=r2_load, width=20, height=2, font=("Arial", 10, "bold"))
btn_R2.place(x=530, y=100)

btn_R3 = tk.Button(reportes, text="Tardanza en comer", command=r3_load, width=20, height=2, font=("Arial", 10, "bold"))
btn_R3.place(x=350, y=150)

btn_R4 = tk.Button(reportes, text="Quejas a personal", command=r4_load, width=20, height=2, font=("Arial", 10, "bold"))
btn_R4.place(x=530, y=150)

btn_R5 = tk.Button(reportes, text="Quejas a platos", command=r5_load, width=20, height=2, font=("Arial", 10, "bold"))
btn_R5.place(x=350, y=200)

btn_R6 = tk.Button(reportes, text="Eficiencia de meseros", command=r6_load, width=20, height=2, font=("Arial", 10, "bold"))
btn_R6.place(x=530, y=200)

btn_Creg = tk.Button(reportes, text="Regresar", command=open_main_menu, width=20, height=2, font=("Arial", 10, "bold"))
btn_Creg.place(x=430, y=250)

#----------------------------- Cocina -----------------------------------

btn_Creg = tk.Button(cocina, text="Regresar", command=open_main_menu)
btn_Creg.place(x= 420, y = 250)

btn_Clisto = tk.Button(cocina, text = "Marcar como Listo", command=Cocina_marcar_listo)
btn_Clisto.place(x= 520, y = 250)

#----------------------------- Bar -----------------------------------

btn_Breg = tk.Button(bar, text="Regresar", command=open_main_menu)
btn_Breg.place(x= 420, y = 250)

btn_Blisto = tk.Button(bar, text = "Marcar como Listo", command=Bar_marcar_listo)
btn_Blisto.place(x= 520, y = 250)

#----------------------------- R1 -----------------------------------4
label_fecha_inicioR1 = tk.Label(r1, text="Fecha Inicio (YYYY/MM/DD 00:00):")
label_fecha_inicioR1.pack(pady=5)
entry_fecha_inicioR1 = tk.Entry(r1)
entry_fecha_inicioR1.pack(pady=10)

label_fecha_finR1 = tk.Label(r1, text="Fecha Fin (YYYY/MM/DD 00:00):")
label_fecha_finR1.pack(pady=5)
entry_fecha_finR1 = tk.Entry(r1)
entry_fecha_finR1.pack(pady=5)

btn_registroR1 = tk.Button(r1, text="Realizar Reporte", command=R1)
btn_registroR1.pack(pady=5)

btn_regresarR1 = tk.Button(r1, text="Regresar", command=Reportes)
btn_regresarR1.pack(pady=5)

#----------------------------- R2 -----------------------------------4
label_fecha_inicioR2 = tk.Label(r2, text="Fecha Inicio (YYYY/MM/DD 00:00):")
label_fecha_inicioR2.pack(pady=5)
entry_fecha_inicioR2 = tk.Entry(r2)
entry_fecha_inicioR2.pack(pady=10)

label_fecha_finR2 = tk.Label(r2, text="Fecha Fin (YYYY/MM/DD 00:00):")
label_fecha_finR2.pack(pady=5)
entry_fecha_finR2 = tk.Entry(r2)
entry_fecha_finR2.pack(pady=5)

btn_registroR2 = tk.Button(r2, text="Realizar Reporte", command=R2)
btn_registroR2.pack(pady=5)

btn_regresarR2 = tk.Button(r2, text="Regresar", command=Reportes)
btn_regresarR2.pack(pady=5)

#----------------------------- R3 -----------------------------------

label_fecha_inicioR3 = tk.Label(r3, text="Fecha Inicio (YYYY/MM/DD 00:00):")
label_fecha_inicioR3.pack(pady=5)
entry_fecha_inicioR3 = tk.Entry(r3)
entry_fecha_inicioR3.pack(pady=10)

label_fecha_finR3 = tk.Label(r3, text="Fecha Fin (YYYY/MM/DD 00:00):")
label_fecha_finR3.pack(pady=5)
entry_fecha_finR3 = tk.Entry(r3)
entry_fecha_finR3.pack(pady=5)

btn_registroR3 = tk.Button(r3, text="Realizar Reporte", command=R3)
btn_registroR3.pack(pady=5)

btn_regresarR3 = tk.Button(r3, text="Regresar", command=Reportes)
btn_regresarR3.pack(pady=5)
#----------------------------- R4 -----------------------------------
label_fecha_inicioR4 = tk.Label(r4, text="Fecha Inicio (YYYY/MM/DD 00:00):")
label_fecha_inicioR4.pack(pady=5)
entry_fecha_inicioR4 = tk.Entry(r4)
entry_fecha_inicioR4.pack(pady=10)

label_fecha_finR4 = tk.Label(r4, text="Fecha Fin (YYYY/MM/DD 00:00):")
label_fecha_finR4.pack(pady=5)
entry_fecha_finR4 = tk.Entry(r4)
entry_fecha_finR4.pack(pady=5)

btn_registroR4 = tk.Button(r4, text="Realizar Reporte", command=R4)
btn_registroR4.pack(pady=5)

btn_regresarR4 = tk.Button(r4, text="Regresar", command=Reportes)
btn_regresarR4.pack(pady=5)

window.mainloop()
