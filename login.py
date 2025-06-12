import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import sys
import smtplib
from email.mime.text import MIMEText
import webbrowser
import webview
import random
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_password(password_ingresada, password_guardada_hash):
    return bcrypt.checkpw(password_ingresada.encode('utf-8'), password_guardada_hash.encode('utf-8'))

def transicion_glitch(ventana_padre, callback):
    glitch = tk.Toplevel(ventana_padre)
    glitch.overrideredirect(True)
    glitch.attributes("-topmost", True)
    glitch.geometry(f"{ventana_padre.winfo_screenwidth()}x{ventana_padre.winfo_screenheight()}+0+0")

    colores = ["#000", "#0ff", "#f0f", "#fff", "#0f0", "#f00"]
    glitch.configure(bg="black")

    def parpadeo(i=0):
        if i < 8:
            glitch.configure(bg=random.choice(colores))
            glitch.update()
            dx = random.randint(-10, 10)
            dy = random.randint(-10, 10)
            glitch.geometry(f"+{dx}+{dy}")
            glitch.after(50, lambda: parpadeo(i + 1))
        else:
            glitch.destroy()
            callback()

    parpadeo()

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
def fade_in(ventana, alpha=0.0):
    alpha += 0.05
    if alpha <= 1.0:
        ventana.attributes("-alpha", alpha)
        ventana.after(20, lambda: fade_in(ventana, alpha))
def transicion_telon(ventana_padre, callback):
    telon = tk.Toplevel(ventana_padre)
    telon.overrideredirect(True)
    telon.attributes("-topmost", True)
    telon.configure(bg="black")
    telon.geometry(f"{ventana_padre.winfo_screenwidth()}x{ventana_padre.winfo_screenheight()}+0+0")
    telon.lift()

    def oscurecer(alpha=0.0):
        if alpha < 1.0:
            telon.attributes("-alpha", alpha)
            telon.after(10, lambda: oscurecer(alpha + 0.05))
        else:
            telon.after(300, lambda: mostrar_y_destruir_telón())

    def mostrar_y_destruir_telón():
        callback()
        telon.destroy()

    oscurecer()
def transicion_glitch_pixelado(ventana_padre, callback):
    from random import randint, choice

    ancho = ventana_padre.winfo_screenwidth()
    alto = ventana_padre.winfo_screenheight()
    tam_bloque = 40  # tamaño de los "pixeles glitch"

    glitch = tk.Toplevel(ventana_padre)
    glitch.overrideredirect(True)
    glitch.attributes("-topmost", True)
    glitch.geometry(f"{ancho}x{alto}+0+0")

    canvas = tk.Canvas(glitch, width=ancho, height=alto, highlightthickness=0, bg="black")
    canvas.pack()

    def generar_cuadrados(iteracion=0):
        canvas.delete("all")
        for _ in range(200):
            x = randint(0, ancho // tam_bloque) * tam_bloque
            y = randint(0, alto // tam_bloque) * tam_bloque
            color = choice(["white", "black"])
            canvas.create_rectangle(x, y, x + tam_bloque, y + tam_bloque, fill=color, width=0)
        if iteracion < 8:
            glitch.after(60, lambda: generar_cuadrados(iteracion + 1))
        else:
            glitch.destroy()
            callback()

    generar_cuadrados()

def flash_screen(ventana, color="white"):
    flash = tk.Toplevel(ventana)
    flash.overrideredirect(True)
    flash.attributes("-topmost", True)
    flash.configure(bg=color)
    flash.geometry(f"{ventana.winfo_screenwidth()}x{ventana.winfo_screenheight()}+0+0")
    flash.attributes("-alpha", 0.9)
    flash.lift()

    def desaparecer():
        flash.destroy()

    flash.after(150, desaparecer)

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
    if usuario in usuarios and verificar_password(contraseña, usuarios[usuario]["password"]):
        def abrir_y_cerrar():
            ventana.destroy()
            abrir_interfaz_web()

        transicion_telon(ventana, abrir_y_cerrar)



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
        nuevo_usuario = entry_nuevo_usuario.get().strip()
        nueva_contraseña = entry_nueva_contraseña.get().strip()
        confirmar_contraseña = entry_confirmar_contraseña.get().strip()
        nuevo_email = entry_email.get().strip()

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
        elif len(nueva_contraseña) < 8 or \
            not any(c.islower() for c in nueva_contraseña) or \
            not any(c.isupper() for c in nueva_contraseña) or \
            not any(c.isdigit() for c in nueva_contraseña):
            messagebox.showwarning("Contraseña débil",
                "La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas y números.")
            entry_nueva_contraseña.focus_force()
        elif nueva_contraseña != confirmar_contraseña:
            messagebox.showerror("Contraseñas no coinciden", "Las contraseñas ingresadas no son iguales.")
            entry_nueva_contraseña.delete(0, 'end')
            entry_confirmar_contraseña.delete(0, 'end')
            entry_nueva_contraseña.focus_force()
        else:
            usuarios[nuevo_usuario] = {
        "password": hash_password(nueva_contraseña),
        "email": nuevo_email
        }

            guardar_usuarios()
            flash_screen(ventana_reg)
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            ventana_reg.destroy()

    ventana_reg = tk.Toplevel()
    ventana_reg.title("Crear nuevo usuario")
    ventana_reg.geometry("370x500")
    ventana_reg.configure(bg="#f8f5eb")
    ventana_reg.resizable(False, False)
    ventana_reg.grab_set()

    # Tema y estilo
    style_reg = ttk.Style(ventana_reg)
    try:
        ruta_azure = os.path.join(os.path.dirname(__file__), "azure.tcl")
        ventana_reg.tk.call("source", ruta_azure)
        style_reg.theme_use("azure")
    except Exception:
        style_reg.theme_use("clam")

    style_reg.configure("Rounded.TButton",
                        font=("Segoe UI", 12, "bold"),
                        foreground="white",
                        background="#204C78",
                        padding=7,
                        relief="flat")

    style_reg.map("Rounded.TButton",
                  background=[("active", "#15314d")],
                  relief=[("pressed", "sunken"), ("!pressed", "flat")])

    # Transición suave
    ventana_reg.attributes("-alpha", 0.0)
    fade_in(ventana_reg)

    # Contenedor principal
    frame = tk.Frame(ventana_reg, bg="#f8f5eb")
    frame.pack(expand=True, fill="both", padx=30, pady=20)

    # Título
    tk.Label(frame, text="📝 Crear nuevo usuario", font=("Segoe UI", 16, "bold"),
             bg="#f8f5eb", fg="#204C78").pack(pady=(0, 20))

    # Campos en vertical
    def campo(label_text, show=None):
        tk.Label(frame, text=label_text, font=("Segoe UI", 11), bg="#f8f5eb").pack(anchor="w", pady=(0, 2))
        entry = ttk.Entry(frame, font=("Segoe UI", 11), width=30, show=show)
        entry.pack(pady=(0, 12))
        return entry

    entry_nuevo_usuario = campo("Nombre de usuario:")
    # CONTRASEÑA
    tk.Label(frame, text="Contraseña:", font=("Segoe UI", 11), bg="#f8f5eb").pack(anchor="w", pady=(0, 2))

    pass_frame_reg = tk.Frame(frame, bg="#f8f5eb")
    pass_frame_reg.pack(pady=(0, 12))

    entry_nueva_contraseña = ttk.Entry(pass_frame_reg, font=("Segoe UI", 11), width=27, show="*")
    entry_nueva_contraseña.pack(side="left")

    ver_pass_var_reg = tk.BooleanVar(value=False)
    def toggle_pass_reg():
        if ver_pass_var_reg.get():
            entry_nueva_contraseña.configure(show="*")
            btn_ver_pass_reg.config(text="👁")
            ver_pass_var_reg.set(False)
        else:
            entry_nueva_contraseña.configure(show="")
            btn_ver_pass_reg.config(text="🔒")
            ver_pass_var_reg.set(True)

    btn_ver_pass_reg = tk.Button(pass_frame_reg, text="👁", command=toggle_pass_reg,
                                font=("Segoe UI", 10), bd=0, bg="#f8f5eb", activebackground="#f8f5eb",
                                cursor="hand2")
    btn_ver_pass_reg.pack(side="left", padx=(5, 0))


    # CONFIRMAR CONTRASEÑA
    tk.Label(frame, text="Confirmar contraseña:", font=("Segoe UI", 11), bg="#f8f5eb").pack(anchor="w", pady=(0, 2))

    confirm_frame_reg = tk.Frame(frame, bg="#f8f5eb")
    confirm_frame_reg.pack(pady=(0, 12))

    entry_confirmar_contraseña = ttk.Entry(confirm_frame_reg, font=("Segoe UI", 11), width=27, show="*")
    entry_confirmar_contraseña.pack(side="left")

    ver_confirm_var_reg = tk.BooleanVar(value=False)
    def toggle_confirm_reg():
        if ver_confirm_var_reg.get():
            entry_confirmar_contraseña.configure(show="*")
            btn_ver_confirm_reg.config(text="👁")
            ver_confirm_var_reg.set(False)
        else:
            entry_confirmar_contraseña.configure(show="")
            btn_ver_confirm_reg.config(text="🔒")
            ver_confirm_var_reg.set(True)

    btn_ver_confirm_reg = tk.Button(confirm_frame_reg, text="👁", command=toggle_confirm_reg,
                                    font=("Segoe UI", 10), bd=0, bg="#f8f5eb", activebackground="#f8f5eb",
                                    cursor="hand2")
    btn_ver_confirm_reg.pack(side="left", padx=(5, 0))

    entry_email = campo("Correo electrónico:")

    # Botón enviar
    ttk.Button(frame, text="Enviar", command=guardar_nuevo_usuario,
               style="Rounded.TButton").pack(pady=20, ipadx=8, ipady=5)




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
    logo_img = logo_img.resize((230, 230), Resampling.LANCZOS)
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

# Frame para centrar todo
pass_frame = tk.Frame(form_frame, bg="#f8f5eb")
pass_frame.pack()

# Subframe con grid para alinear entry y botón
inner_pass_frame = tk.Frame(pass_frame, bg="#f8f5eb")
inner_pass_frame.pack(padx=(40, 0))  # 40 píxeles de margen a la izquierda

entry_contraseña = ttk.Entry(inner_pass_frame, show="*", font=("Segoe UI", 12), width=30)
entry_contraseña.grid(row=0, column=0, pady=(0, 5))

ver_password_var = tk.BooleanVar(value=False)

def toggle_contraseña():
    if ver_password_var.get():
        entry_contraseña.configure(show="*")
        btn_ver.config(text="👁")
        ver_password_var.set(False)
    else:
        entry_contraseña.configure(show="")
        btn_ver.config(text="🔒")
        ver_password_var.set(True)

btn_ver = tk.Button(inner_pass_frame, text="👁", command=toggle_contraseña,
                    font=("Segoe UI", 10), bd=0, bg="#f8f5eb", activebackground="#f8f5eb",
                    cursor="hand2")
btn_ver.grid(row=0, column=1, padx=(5, 0), pady=(0, 5))


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