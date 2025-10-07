import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Interfaz con Tkinter")
root.geometry("800x400")

# Frame izquierdo
frame_left = ttk.Frame(root, width=400, padding=20)
frame_left.pack(side="left", fill="y")

ttk.Label(frame_left, text="Información adicional", font=("Arial", 18, "bold")).pack(anchor="w")
ttk.Label(frame_left, text="Aquí puedes mostrar datos, instrucciones, o cualquier otro contenido que desees.", wraplength=350).pack(anchor="w", pady=10)
ttk.Label(frame_left, text="Selecciona una fecha:", font=("Arial", 12, "bold")).pack(anchor="w", pady=10)
fecha = ttk.Entry(frame_left)
fecha.pack(anchor="w")

# Frame derecho
frame_right = ttk.Frame(root, width=400, padding=20)
frame_right.pack(side="right", fill="both", expand=True)

ttk.Label(frame_right, text="Chat con GPT-The office", font=("Arial", 18, "bold")).pack(anchor="w")
ttk.Label(frame_right, text="Escribe tu mensaje:").pack(anchor="w", pady=10)
mensaje = ttk.Entry(frame_right)
mensaje.pack(anchor="w", fill="x")
ttk.Button(frame_right, text="Enviar mensaje").pack(anchor="w", pady=10)
ttk.Label(frame_right, text="Conversación:", font=("Arial", 14, "bold")).pack(anchor="w", pady=10)

root.mainloop()