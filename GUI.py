import tkinter as tk
from tkinter import messagebox
import conexion as con

window = tk.Tk()
window.title("Inicio de Sesión")
window.geometry("1000x500")

signin = tk.Tk()
signin.title("Registro")
signin.geometry("1000x500")
signin.withdraw()

main_menu_window = tk.Tk()
main_menu_window.title("Menú Principal")
main_menu_window.geometry("1000x500")
main_menu_window.withdraw()

def Signin():
    signin.deiconify()
    window.withdraw()
    username = entry_usuario_sn.get()
    password = entry_password_sn.get()
    
    btn_Signin = tk.Button(signin, text = "Registrarse", command=Signin)
    btn_Signin.pack(pady = 5,padx=5)
    
def login():
    username = entry_username_w.get()
    password = entry_password_w.get()
    
    if username == "usuario" and password == "contraseña":
        open_main_menu()        
    else:
        messagebox.showerror("Error de inicio de sesión", "Usuario o contraseña incorrectos")
        
def open_main_menu():
    window.withdraw()
    main_menu_window.deiconify()
    
    
    
    lbl_menu = tk.Label(main_menu_window, text="¡Bienvenido al Menú Principal!")
    lbl_menu.pack(pady=10)
    
    btn_exit = tk.Button(main_menu_window, text="Salir", command=return_to_login)
    btn_exit.pack(pady=5)
    

def return_to_login():
    main_menu_window.withdraw()
    window.deiconify()


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


btn_irSignin = tk.Button(window, text = "Registrarse", command=Signin)
btn_irSignin.place(x = 520, y = 200)

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


window.mainloop()
main_menu_window.mainloop()
signin.mainloop()

