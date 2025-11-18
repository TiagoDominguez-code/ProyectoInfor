import tkinter as tk

ventana = tk.Tk()
ventana.title('Feedback del juego')
ventana.geometry('800x450')
# Título

titulo = tk.Label(ventana, text="Dejanos tu opinión sobre el juego", font=('Arial', 12))
titulo.pack(pady=10)

# Ingreso del nombre del jugador
tk.Label(ventana, text="Tu nombre:").pack()
entrada_nombre = tk.Entry(ventana)
entrada_nombre.pack()

# Ingreso del comentario
tk.Label(ventana, text="Tu opinión:").pack()
entrada_opinion = tk.Entry(ventana, width=50)
entrada_opinion.pack(pady=5)

# Selección de valoración
tk.Label(ventana, text="Valoración (1 a 5):").pack()
valoracion = tk.Spinbox(ventana, from_=1, to=5, width=5)
valoracion.pack(pady=5)

# Listbox para mostrar feedbacks
lista_feedback = tk.Listbox(ventana, width=60)
lista_feedback.pack(pady=10)

# Función para agregar el feedback
def enviar_feedback():
    nombre = entrada_nombre.get()
    opinion = entrada_opinion.get()
    puntuacion = valoracion.get()

    if nombre and opinion:
        texto = f"{nombre} (⭐{puntuacion}): {opinion}"
        lista_feedback.insert(tk.END, texto)
        entrada_nombre.delete(0, tk.END)
        entrada_opinion.delete(0, tk.END)
        valoracion.delete(0, tk.END)
        valoracion.insert(0, "1")

boton_enviar = tk.Button(ventana, text="Enviar opinión", command=enviar_feedback)
boton_enviar.pack()

ventana.mainloop()