import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import sys
import smtplib
from email.mime.text import MIMEText
import webbrowser
import webview

# ----------------------------- FUNCIONES DE ARCHIVO -----------------------------

ARCHIVO_USUARIOS = "usuarios.json"

def cargar_usuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as f:
            return json.load(f)
    else:
        return {
            "admin": {
                "password": "1234",
                "email": "admin@gmail.com"
            },
            "juan": {
                "password": "passjuan",
                "email": "juan@gmail.com"
            }
        }

def guardar_usuarios():
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

# ----------------------------- FUNCIONES PRINCIPALES -----------------------------

def abrir_interfaz_web():
    import ctypes

    # Obtener resolución de pantalla (Windows)
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    webview.create_window(
        "Castro Feijoo SRL",
        "https://castro-feijoo-srl.netlify.app/",
        width=screen_width,
        height=screen_height,
        resizable=True
    )
    webview.start(gui='qt')

def mostrar_alerta(titulo, mensaje, tipo="info"):
    ventana_alerta = tk.Toplevel()
    ventana_alerta.title(titulo)
    ventana_alerta.geometry("360x260")
    ventana_alerta.configure(bg="#f8f5eb")
    ventana_alerta.resizable(False, False)
    ventana_alerta.grab_set()

    frame = tk.Frame(ventana_alerta, bg="#f8f5eb")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    color = {"info": "#204C78", "error": "#a94442", "warning": "#b7950b"}.get(tipo, "#204C78")

    tk.Label(frame, text=titulo, font=("Segoe UI", 14, "bold"), fg=color, bg="#f8f5eb").pack(pady=(0, 10))
    tk.Label(frame, text=mensaje, font=("Segoe UI", 11), bg="#f8f5eb",
         wraplength=300, justify="center").pack(pady=(20, 20))
    ttk.Button(frame, text="Aceptar", command=ventana_alerta.destroy, style="Rounded.TButton").pack(ipadx=8, ipady=5)


def verificar_login():
    usuario = entry_usuario.get().strip()
    contraseña = entry_contraseña.get().strip()

    # Limpiar estilos anteriores
    entry_usuario.configure(style="TEntry")
    entry_contraseña.configure(style="TEntry")
    mensaje_error.config(text="")

    campos_invalidos = []

    if not usuario:
        campos_invalidos.append(entry_usuario)
    if not contraseña:
        campos_invalidos.append(entry_contraseña)

    if campos_invalidos:
        for campo in campos_invalidos:
            campo.configure(style="Error.TEntry")
        mensaje_error.config(text="Todos los campos son obligatorios.")
        return

    # Verificar credenciales
    if usuario in usuarios and usuarios[usuario]["password"] == contraseña:
        ventana.destroy()
        abrir_interfaz_web()
    else:
        entry_usuario.configure(style="Error.TEntry")
        entry_contraseña.configure(style="Error.TEntry")
        mensaje_error.config(text="Usuario o contraseña incorrectos.")


def enviar_email(destinatario, asunto, mensaje):
    print(f"[Simulado] Enviando email a {destinatario}")
    print(f"Asunto: {asunto}")
    print(f"Mensaje: {mensaje}")
    return True

def recuperar_contraseña():
    def buscar_contraseña():
        usuario = entry_usuario_rec.get().strip()

        # Limpiar estilos anteriores
        entry_usuario_rec.configure(style="TEntry")
        mensaje_error_rec.config(text="")

        if not usuario:
            entry_usuario_rec.configure(style="Error.TEntry")
            mensaje_error_rec.config(text="El campo es obligatorio.")
            return

        if usuario in usuarios:
            email = usuarios[usuario]["email"]
            contraseña = usuarios[usuario]["password"]
            asunto = "Recuperación de contraseña"
            cuerpo = f"Hola {usuario}, los pasos para restablecer tu contraseña han sido enviados al correo"
            exito = enviar_email(email, asunto, cuerpo)
            if exito:
                mostrar_alerta("Recuperación enviada", f"Enviamos la contraseña a {email}", tipo="info")
                ventana_rec.destroy()
            else:
                entry_usuario_rec.configure(style="Error.TEntry")
                mensaje_error_rec.config(text="No se pudo enviar el correo.")
        else:
            entry_usuario_rec.configure(style="Error.TEntry")
            mensaje_error_rec.config(text="El usuario ingresado no existe.")

    ventana_rec = tk.Toplevel()
    ventana_rec.title("Recuperar contraseña")
    ventana_rec.geometry("400x300")
    ventana_rec.configure(bg="#f8f5eb")
    ventana_rec.resizable(False, False)
    ventana_rec.grab_set()

    # Frame de contenido
    frame = tk.Frame(ventana_rec, bg="#f8f5eb")
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Título
    tk.Label(frame, text="🔑 Recuperar contraseña", font=("Segoe UI", 16, "bold"),
             bg="#f8f5eb", fg="#204C78").pack(pady=(0, 15))

    # Campo usuario
    tk.Label(frame, text="Ingresá tu nombre de usuario:", font=("Segoe UI", 11),
             bg="#f8f5eb").pack(anchor="w", padx=25)
    entry_usuario_rec = ttk.Entry(frame, font=("Segoe UI", 11), width=30)
    entry_usuario_rec.pack(padx=10, pady=(5, 5))

    mensaje_error_rec = tk.Label(frame, text="", font=("Segoe UI", 10),
                                 fg="red", bg="#f8f5eb")
    mensaje_error_rec.pack(pady=(0, 0))


    # Botón recuperar con estilo coherente
    btn_recuperar = ttk.Button(frame, text="Enviar", command=buscar_contraseña, style="Rounded.TButton")
    btn_recuperar.pack(pady=10)


def crear_usuario():
    def guardar_nuevo_usuario():
        nuevo_usuario = entry_nuevo_usuario.get()
        nueva_contraseña = entry_nueva_contraseña.get()
        confirmar_contraseña = entry_confirmar_contraseña.get()
        nuevo_email = entry_email.get()

        # Validaciones
        if nuevo_usuario in usuarios:
            messagebox.showerror("Error", "El usuario ya existe.")
            entry_nuevo_usuario.focus_force()
        elif not nuevo_usuario or not nueva_contraseña or not confirmar_contraseña or not nuevo_email:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            entry_nuevo_usuario.focus_force()
        elif "@" not in nuevo_email or "." not in nuevo_email:
            messagebox.showwarning("Email inválido", "El email no tiene un formato válido.")
            entry_email.focus_force()
        elif len(nuevo_usuario) < 3:
            messagebox.showwarning("Usuario inválido", "El nombre de usuario debe tener al menos 3 caracteres.")
            entry_nuevo_usuario.focus_force()
        elif len(nueva_contraseña) < 6:
            messagebox.showwarning("Contraseña débil", "La contraseña debe tener al menos 6 caracteres.")
            entry_nueva_contraseña.focus_force()
        elif nueva_contraseña != confirmar_contraseña:
            messagebox.showerror("Contraseñas no coinciden", "Las contraseñas ingresadas no son iguales.")
            entry_nueva_contraseña.delete(0, 'end')
            entry_confirmar_contraseña.delete(0, 'end')
            entry_nueva_contraseña.focus_force()
        else:
            usuarios[nuevo_usuario] = {
                "password": nueva_contraseña,
                "email": nuevo_email
            }
            guardar_usuarios()
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            nueva_ventana.destroy()

    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Crear nuevo usuario")
    nueva_ventana.geometry("400x330")
    nueva_ventana.resizable(False, False)
    nueva_ventana.grab_set()
    nueva_ventana.focus_force()

    # Campos del formulario
    tk.Label(nueva_ventana, text="Nuevo Usuario:").pack(pady=5)
    entry_nuevo_usuario = ttk.Entry(nueva_ventana)
    entry_nuevo_usuario.pack(pady=5)

    tk.Label(nueva_ventana, text="Contraseña:").pack(pady=5)
    entry_nueva_contraseña = ttk.Entry(nueva_ventana, show="*")
    entry_nueva_contraseña.pack(pady=5)

    tk.Label(nueva_ventana, text="Confirmar contraseña:").pack(pady=5)
    entry_confirmar_contraseña = ttk.Entry(nueva_ventana, show="*")
    entry_confirmar_contraseña.pack(pady=5)

    tk.Label(nueva_ventana, text="Email:").pack(pady=5)
    entry_email = ttk.Entry(nueva_ventana)
    entry_email.pack(pady=5)
    
    btn_enviar = ttk.Button(nueva_ventana, text="Enviar", command=guardar_nuevo_usuario)
    btn_enviar.pack(pady=15)

def mostrar_login():
    os.execl(sys.executable, sys.executable, *sys.argv)

# ----------------------------- INICIO DEL PROGRAMA -----------------------------

usuarios = cargar_usuarios()

ventana = tk.Tk()
ventana.title("Inicio de Sesión")
ventana.state("zoomed")
ventana.configure(bg="#f8f5eb")
ventana.resizable(True, True)

style = ttk.Style(ventana)
try:
    ruta_azure = os.path.join(os.path.dirname(__file__), "azure.tcl")
    ventana.tk.call("source", ruta_azure)
    style.theme_use("azure")
except Exception as e:
    print(f"No se pudo cargar el tema Azure: {e}")
    style.theme_use("clam")

style.configure("Rounded.TButton",
                font=("Segoe UI", 12, "bold"),
                foreground="white",
                background="#204C78",
                padding=7,
                relief="flat")

style.configure("Error.TEntry",
                foreground="black",
                bordercolor="red",
                lightcolor="red",
                darkcolor="red",
                borderwidth=2)

style.map("Rounded.TButton",
          background=[("active", "#15314d")],
          relief=[("pressed", "sunken"), ("!pressed", "flat")])

contenedor = tk.Frame(ventana, bg="#f8f5eb")
contenedor.pack(expand=True, fill="both")

# ----------------------- LOGO ARRIBA -----------------------
try:
    from PIL import Image, ImageTk
    from PIL.Image import Resampling

    logo_path = os.path.abspath("logo.png")
    logo_img = Image.open(logo_path)
    logo_img = logo_img.resize((250, 250), Resampling.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(contenedor, image=logo, bg="#f8f5eb")
    logo_label.image = logo
    logo_label.pack(pady=(100, 50))  # logo centrado arriba
except Exception as e:
    print("No se pudo cargar el logo:", e)

# ----------------------- FORMULARIO ABAJO -----------------------
form_frame = tk.Frame(contenedor, bg="#f8f5eb")
form_frame.pack()

# Título
tk.Label(form_frame, text="🔐 Iniciar Sesión", font=("Segoe UI", 22, "bold"),
         bg="#f8f5eb", fg="#204C78").pack(pady=(0, 20))

# Usuario
user_label = tk.Label(form_frame, text="Usuario", font=("Segoe UI", 12),
                      bg="#f8f5eb", fg="#333", anchor="w", width=30)
user_label.pack(pady=(0, 2))
entry_usuario = ttk.Entry(form_frame, font=("Segoe UI", 12), width=30)
entry_usuario.pack(pady=(0, 12))

# Contraseña
pass_label = tk.Label(form_frame, text="Contraseña", font=("Segoe UI", 12),
                      bg="#f8f5eb", fg="#333", anchor="w", width=30)
pass_label.pack(pady=(0, 2))
entry_contraseña = ttk.Entry(form_frame, show="*", font=("Segoe UI", 12), width=30)
entry_contraseña.pack(pady=(0, 20))

# Botón Entrar
btn_login = ttk.Button(form_frame, text="Iniciar sesión", command=verificar_login, style="Rounded.TButton")
btn_login.pack(pady=(20, 20), ipadx=5, ipady=5)

mensaje_error = tk.Label(form_frame, text="", font=("Segoe UI", 10),
                         fg="red", bg="#f8f5eb")
mensaje_error.pack(pady=(0, 10))

# Separador
ttk.Separator(form_frame, orient='horizontal').pack(fill='x', padx=20, pady=(0, 10))

# Enlaces
frame_botones_sec = tk.Frame(form_frame, bg="#f8f5eb")
frame_botones_sec.pack()

color_link = "#b7950b"
dorado_oscuro = "#8c6d07"
fuente_link = ("Segoe UI", 12)

label_olvido = tk.Label(frame_botones_sec, text="¿Olvidaste tu contraseña?", fg=color_link,
                        bg="#f8f5eb", cursor="hand2", font=fuente_link)
label_olvido.pack(side="left", padx=10)
label_olvido.bind("<Button-1>", lambda e: recuperar_contraseña())
label_olvido.bind("<Enter>", lambda e: label_olvido.config(fg=dorado_oscuro))
label_olvido.bind("<Leave>", lambda e: label_olvido.config(fg=color_link))

label_crear = tk.Label(frame_botones_sec, text="Registrarse", fg=color_link,
                       bg="#f8f5eb", cursor="hand2", font=fuente_link)
label_crear.pack(side="left", padx=10)
label_crear.bind("<Button-1>", lambda e: crear_usuario())
label_crear.bind("<Enter>", lambda e: label_crear.config(fg=dorado_oscuro))
label_crear.bind("<Leave>", lambda e: label_crear.config(fg=color_link))

ventana.mainloop()