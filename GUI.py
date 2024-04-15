import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import conexion as con

#Diccionario de valores admitidos en la contraseña
diccionario = {' ':0}
diccionario.update({chr(i + ord('A')): i + 1 for i in range(26)})
diccionario.update({str(i): i + 27 for i in range(10)})
diccionario.update({'_':37})
diccionario.update({'-':38})

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
tree = ttk.Treeview(cocina, columns=("Nombre Alimento"))
tree.heading("#0", text="Ordenes")
tree.column("#0", width=200)  
tree.pack(padx=10, pady=10)

def marcar_listo():
    row = tree.focus()
    tree.delete(row)

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
    window.withdraw()
    signin.deiconify()

def Signin(): #Aqui hay que hacer que guarde en la base de datos los usuarios y sus contraseñas
    name = entry_name_sn.get()
    jobPos = entry_jobPos_sn.get()
    username = entry_usuario_sn.get()
    password = entry_password_sn.get()
    confPassword = entry_Confpassword_sn.get()

    #Verifica que los valores no sean vacios
    if name=="" or jobPos=="" or username=="" or password=="" or confPassword=="":
        messagebox.showerror("Error al registrar usuario", "Todas las casillas deben tener información.")
    #Verifica que la contraseña tenga los valores aceptados
    elif verificar_caracteres(password) or ' ' in password:
        messagebox.showerror("Error al registrar usuario", "La contraseña solo puede contener letras del abecedario anglosajón, números, guión(-) y guión bajo(_).")
    #Verifica que la contraseña y la confirmación sean iguales
    elif password!=confPassword:
        messagebox.showerror("Error al registrar usuario", "La contraseña no coincide.")
    else:
        #Añade un usuario nuevo
        if len(password)%2 != 0:
            password += ' '
        if con.agregar_Usuario(name, jobPos, username, password):
            messagebox.showinfo("Registro exitoso", "Usuario agregado correctamente")
            open_main_menu()
        else:
            messagebox.showerror("Error al registrar usuario", "Hubo un problema al agregar el usuario.")
    
def login(): #Aqui tiene que jalar los datos de la base de datos
    username = entry_username_w.get()
    password = entry_password_w.get()
    
    if len(password)%2 != 0:
            password += ' '
    if con.verificar_Usuario(username, password):
        open_main_menu()        
    else:
        messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos")
        
def open_main_menu(): #Me falta meterle para ponerle todas las opciones a otras pantallas
    cocina.withdraw()
    window.withdraw()
    signin.withdraw()
    main_menu_window.deiconify()
    
def return_to_login():
    main_menu_window.withdraw()
    window.deiconify()

def verificar_caracteres(cadena):
    cadena = cadena.upper()
    caracteres_permitidos = set(diccionario.keys())
    caracteres_invalidos = [char for char in cadena if char not in caracteres_permitidos]
    
    if caracteres_invalidos:
        return True
    else:
        return False

#----------------------------- Log In -----------------------------------
label_username_w = tk.Label(window, text="Usuario:")
label_username_w.pack(pady=5)
entry_username_w = tk.Entry(window)
entry_username_w.pack(pady=5)

label_password_w = tk.Label(window, text="Contraseña:")
label_password_w.pack(pady=5)
entry_password_w = tk.Entry(window, show= "*")
entry_password_w.pack(pady=5)


btn_login = tk.Button(window, text="Iniciar Sesión", command=login)
btn_login.place(x= 420, y = 200)


btn_irSignin = tk.Button(window, text = "Registrarse", command=signinWindow)
btn_irSignin.place(x = 520, y = 200)

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
btn_irSignin.pack(pady=5)

#----------------------------- Menu -----------------------------------
lbl_menu = tk.Label(main_menu_window, text="¡Bienvenido al Menú Principal!")
lbl_menu.pack(pady=10)

btn_exit = tk.Button(main_menu_window, text="Regresar", command=return_to_login)
btn_exit.pack(pady=5)

btn_cocina = tk.Button(main_menu_window, text="Cocina", command=PantCocina)
btn_cocina.pack(pady=5)


#----------------------------- Cocina -----------------------------------

btn_reg = tk.Button(cocina, text="Regresar", command=open_main_menu)
btn_reg.place(x= 420, y = 250)

btn_listo = tk.Button(cocina, text = "Marcar como Listo", command=marcar_listo)
btn_listo.place(x= 520, y = 250)

window.mainloop()
