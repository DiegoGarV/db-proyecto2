import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import conexion as con


# Pantalla Log In
#Crea la interfaz gráfica
window = tk.Tk()
window.title("Inicio de Sesión")
window.geometry("1000x500")
window.resizable(0,0)
window.protocol("WM_DELETE_WINDOW", quit)

# Pantalla Sign In
signin = tk.Toplevel(window)
signin.title("Registro")
signin.geometry("1000x500")
signin.withdraw()
signin.resizable(0,0)
signin.protocol("WM_DELETE_WINDOW", quit)


# Pantalla Menu
main_menu_window = tk.Toplevel(window)
main_menu_window.title("Menú Principal")
main_menu_window.geometry("1000x500")
main_menu_window.withdraw()
main_menu_window.resizable(0,0)
main_menu_window.protocol("WM_DELETE_WINDOW", quit)

# Pantalla Cocina
cocina = tk.Toplevel()
cocina.title("Cocina")
cocina.geometry("1000x500")
cocina.resizable (0,0)
cocina.withdraw()
cocina.protocol("WM_DELETE_WINDOW", quit)
tree = ttk.Treeview(cocina, columns=("Nombre Plato"))
tree.heading("#0", text="Ordenes")
tree.column("#0", width=200)  
tree.pack(padx=10, pady=10)

# Pantalla Bar
bar = tk.Toplevel()
bar.title("Bar")
bar.geometry("1000x500")
bar.resizable(0,0)
bar.withdraw()
bar.protocol("WM_DELETE_WINDOW", quit)
Bartree = ttk.Treeview(bar, columns=("Nombre Bebida"))
Bartree.heading("#0", text="Ordenes")
Bartree.column("#0", width=200)  
Bartree.pack(padx=10, pady=10)

# Pantalla Menu Reportes
reportes = tk.Toplevel()
reportes.title("Reportes")
reportes.geometry("1000x500")
reportes.resizable(0,0)
reportes.withdraw()
reportes.protocol("WM_DELETE_WINDOW", quit)

# Pantallas Reportes
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
        row = tree.focus()
        tree.delete(row)
    except: 
        messagebox.showerror("Error al marcar como listo", "Porfavor seleccione un registro")
        return False 
    
def PantCocina():
    main_menu_window.withdraw()
    cocina.deiconify()

    con.tabla_cocina()
    resultados = con.tabla_cocina()


    for item in tree.get_children():
        tree.delete(item)

    contador = 0
    for resultado in resultados:
        contador = contador + 1
        tree.insert("", "end", values=(contador, resultado[0],))
        
def signinWindow():
    signin.deiconify()
    window.withdraw()

def Signin(): #Aqui hay que hacer que guarde en la base de datos los usuarios y sus contraseñas
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

    #btn_Signin = tk.Button(signin, text = "Registrarse", command=Signin) #al precionar este boton hacer lo de arriba
    #btn_Signin.pack(pady = 5,padx=5)
    
def login(): #Aqui tiene que jalar los datos de la base de datos
    username = entry_username_w.get()
    password = entry_password_w.get()
    
    if con.verificar_Usuario(username, password):
        open_main_menu()        
    else:
        messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos")
        
def Reportes():
    main_menu_window.withdraw()
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

#----------------------------- Cocina -----------------------------------
btn_R1 = tk.Button(reportes, text="Reporte 1", command= r1.deiconify)
btn_R1.place(x = 400, y = 100)
btn_R1.config(font=("Arial", 10, "bold"))

btn_R2 = tk.Button(reportes, text="Reporte 2", command= r2.deiconify)
btn_R2.place(x = 510, y = 100)
btn_R2.config(font=("Arial", 10, "bold"))

btn_R3 = tk.Button(reportes, text="Reporte 3", command= r3.deiconify)
btn_R3.place(x = 400, y = 150)
btn_R3.config(font=("Arial", 10, "bold"))

btn_R4 = tk.Button(reportes, text="Reporte 4", command= r4.deiconify)
btn_R4.place(x = 510, y = 150)
btn_R4.config(font=("Arial", 10, "bold"))

btn_R5 = tk.Button(reportes, text="Reporte 5", command= r5.deiconify)
btn_R5.place(x = 400, y = 200)
btn_R5.config(font=("Arial", 10, "bold"))

btn_R6 = tk.Button(reportes, text="Reporte 6", command= r6.deiconify)
btn_R6.place(x=510, y=200)
btn_R6.config(font=("Arial", 10, "bold"))

btn_Creg = tk.Button(reportes, text="Regresar", command=open_main_menu)
btn_Creg.place(x= 460, y = 250)
btn_Creg.config(font=("Arial", 10, "bold"))

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

#----------------------------- Bar -----------------------------------


window.mainloop()
