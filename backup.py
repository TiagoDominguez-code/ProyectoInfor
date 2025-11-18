import tkinter as tk
from tkinter import messagebox
import random
import time

# --- 0. PALETA Y FUENTES (Nuevo) ---
COLOR_FONDO_PRINCIPAL = "#f0f0f0"  # Gris muy claro para el fondo
COLOR_FONDO_SECUNDARIO = "#ffffff" # Blanco para el marco de contenido
COLOR_ACENTO_PRIMARIO = "#4CAF50"   # Verde (Éxito, Botón Responder)
COLOR_ACENTO_SECUNDARIO = "#2196F3"  # Azul (Reiniciar)
COLOR_ACENTO_TERCIARIO = "#FF9800" # Naranja (Feedback)
COLOR_TITULO = "#333333"            # Gris oscuro (Títulos)
COLOR_TEXTO = "#444444"             # Gris medio (Texto general)
COLOR_ERROR = "#d9534f"             # Rojo (Error)

FUENTE_TITULO = ('Segoe UI', 16, 'bold')
FUENTE_PREGUNTA = ('Segoe UI', 14, 'bold')
FUENTE_GENERAL = ('Segoe UI', 12)
FUENTE_CRONOMETRO = ('Consolas', 14, 'bold')


# --- 1. DATOS DEL JUEGO ---
QUIZ_DATA = {
    "HTML": [
        {"pregunta": "¿es un lenguaje de programacion?",
         "opciones": ["No", "Si", "Es un lenguaje de Datos", "Depende el punto de vista"],
         "respuesta": "No"},
        {"pregunta": "¿Que significan las siglas HTML?",
         "opciones": ["Hyper Text Markup language", "High Tech Modern Language",
                      "Hyperlink and Text Management Logic", "Home Tool Markup Language"],
         "respuesta": "Hyper Text Markup language"},
        {"pregunta": "¿Que etiqueta se utiliza para definir el cuerpo de un HTML donde va todo el contenido visible?",
         "opciones": ["body", "header", "footer", "main"],
         "respuesta": "body"},
        {"pregunta": "¿Que etiqueta se usa para crear un enlace (hipervinculo) a otra pagina?",
         "opciones": ["<link>", "<a>", "<href>", "<Url>"],
         "respuesta": "<a>"},
        {"pregunta": "Para crear una lista no ordenada, ¿que etiqueta utilizo?",
         "opciones": ["<ol>", "<li>", "<ul>", "<list>"],
         "respuesta": "<ul>"}
    ],
    "CSS": [
        {"pregunta": "¿Qué significa CSS?",
         "opciones": ["Cascading Style Sheets", "Creative Style Syntax",
                      "Computer Style System", "Central Styling Structure"],
         "respuesta": "Cascading Style Sheets"},
        {"pregunta": "¿Cuál propiedad se usa para cambiar el color del texto?",
         "opciones": ["text-color", "font-color", "color", "background-color"],
         "respuesta": "color"},
        {"pregunta": "¿Qué selector se usa para aplicar estilo a todos los elementos de una clase?",
         "opciones": ["#nombreClase", ".nombreClase", "nombreClase", "*nombreClase"],
         "respuesta": ".nombreClase"},
        {"pregunta": "¿Cuál propiedad controla el tamaño de la fuente?",
         "opciones": ["text-size", "font-style", "font-size", "size"],
         "respuesta": "font-size"},
        {"pregunta": "¿Qué propiedad se usa para agregar espacio interno dentro de un elemento?",
         "opciones": ["margin", "spacing", "padding", "border-spacing"],
         "respuesta": "padding"}
    ],
    "Python": [
        {"pregunta": "¿Qué tipo de lenguaje es Python?",
         "opciones": ["Compilado", "Interpretado", "Ensamblador", "Binario"],
         "respuesta": "Interpretado"},
        {"pregunta": "¿Cuál es la extensión típica de un archivo Python?",
         "opciones": [".py", ".pt", ".python", ".txt"],
         "respuesta": ".py"},
        {"pregunta": "¿Qué palabra clave se usa para definir una función?",
         "opciones": ["func", "define", "def", "function"],
         "respuesta": "def"},
        {"pregunta": "¿Cuál estructura se usa para repetir un bloque de código mientras se cumple una condición?",
         "opciones": ["for", "repeat", "while", "loop"],
         "respuesta": "while"},
        {"pregunta": "¿Qué tipo de estructura es una lista en Python?",
         "opciones": ["Inmutable", "Mutable", "Estática", "Constante"],
         "respuesta": "Mutable"}
    ]
}


# --- 2. CLASE ESTADISTICAS ---
class Estadisticas:
    def __init__(self, categoria):
        self.categoria = categoria
        self.aciertos = 0
        self.errores = 0
        self.inicio = time.time()
        self.detalle = []  # (pregunta, respuesta_usuario, respuesta_correcta, estado)

    def registrar_respuesta(self, pregunta_texto, respuesta_usuario, respuesta_correcta):
        correcto = respuesta_usuario == respuesta_correcta
        if correcto:
            self.aciertos += 1
        else:
            self.errores += 1
        self.detalle.append((
            pregunta_texto,
            respuesta_usuario if respuesta_usuario else "(sin respuesta)",
            respuesta_correcta,
            "✔️¡Correcta!" if correcto else "Incorrecta"
        ))

    def tiempo_total(self):
        return round(time.time() - self.inicio, 2)


# --- 3. FUNCION PARA MOSTRAR ESTADISTICAS DETALLADAS ---
def mostrar_estadisticas(ventana, estadisticas):
    ventana_resultados = tk.Toplevel(ventana, bg=COLOR_FONDO_PRINCIPAL) # Aplicar fondo
    ventana_resultados.title("Resultados del intento")
    ventana_resultados.geometry("800x480")

    titulo = tk.Label(
        ventana_resultados,
        text=f"📊 Resultados - Categoría {estadisticas.categoria}",
        font=FUENTE_TITULO,
        fg=COLOR_TITULO,
        bg=COLOR_FONDO_PRINCIPAL # Aplicar fondo
    )
    titulo.pack(pady=10)

    resumen = tk.Label(
        ventana_resultados,
        text=f"Aciertos: {estadisticas.aciertos} | Errores: {estadisticas.errores} | "
             f"Tiempo: {estadisticas.tiempo_total()} segundos",
        font=FUENTE_GENERAL,
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO_PRINCIPAL # Aplicar fondo
    )
    resumen.pack(pady=5)

    # Contenedor con scroll
    frame_tabla = tk.Frame(ventana_resultados, bg=COLOR_FONDO_SECUNDARIO)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

    canvas = tk.Canvas(frame_tabla, bg=COLOR_FONDO_SECUNDARIO)
    scrollbar_y = tk.Scrollbar(frame_tabla, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLOR_FONDO_SECUNDARIO)

    # Actualiza el área de scroll al cambiar tamaño
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set)

    # Estilo de encabezado
    encabezado = tk.Frame(scrollable_frame, bg="#e0e0e0") # Gris claro para encabezado
    encabezado.pack(fill="x", pady=(0, 2))
    encabezado_config = {'bg': "#e0e0e0", 'fg': COLOR_TITULO, 'font': ('Segoe UI', 10, 'bold'), 'padx': 4, 'pady': 6}

    tk.Label(encabezado, text="Pregunta", width=50, anchor="w", **encabezado_config).grid(row=0, column=0, sticky="w")
    tk.Label(encabezado, text="Tu respuesta", width=20, anchor="w", **encabezado_config).grid(row=0, column=1, sticky="w")
    tk.Label(encabezado, text="Correcta", width=20, anchor="w", **encabezado_config).grid(row=0, column=2, sticky="w")
    tk.Label(encabezado, text="Estado", width=20, anchor="w", **encabezado_config).grid(row=0, column=3, sticky="w")

    # Filas con resultados
    for i, (preg, resp_user, resp_ok, estado) in enumerate(estadisticas.detalle, start=1):
        bg_color = COLOR_FONDO_SECUNDARIO if i % 2 == 0 else "#f8f8f8" # Alternar color de fila
        fg_color = COLOR_ACENTO_PRIMARIO if "✔️" in estado else COLOR_ERROR

        fila = tk.Frame(scrollable_frame, bg=bg_color)
        fila.pack(fill="x")

        # Configuración de celda (ajustar anchor/sticky para que se vea bien)
        celda_config = {'font': FUENTE_GENERAL, 'bg': bg_color, 'fg': COLOR_TEXTO, 'pady': 3, 'padx': 4}

        tk.Label(fila, text=preg, width=50, anchor="w", wraplength=520, **celda_config).grid(row=i, column=0, sticky="w")
        tk.Label(fila, text=resp_user, width=20, anchor="w", **celda_config).grid(row=i, column=1, sticky="w")
        tk.Label(fila, text=resp_ok, width=20, anchor="w", **celda_config).grid(row=i, column=2, sticky="w")
        tk.Label(fila, text=estado, width=20, anchor="w", fg=fg_color, bg=bg_color, font=('Segoe UI', 12, 'bold')).grid(row=i, column=3, sticky="w")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar_y.pack(side="right", fill="y")

# --- NUEVA FUNCIÓN DE FEEDBACK ---
def abrir_feedback(ventana_principal):
    ventana = tk.Toplevel(ventana_principal, bg=COLOR_FONDO_PRINCIPAL)
    ventana.title('⭐ Feedback del juego')
    ventana.geometry('400x480') # Reducido para mejor visualización

    titulo = tk.Label(ventana, text="Dejanos tu opinión sobre el juego", font=FUENTE_TITULO, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TITULO)
    titulo.pack(pady=15)

    # Ingreso del nombre del jugador
    tk.Label(ventana, text="Tu nombre:", font=FUENTE_GENERAL, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO).pack()
    entrada_nombre = tk.Entry(ventana, width=40, font=FUENTE_GENERAL)
    entrada_nombre.pack(pady=2)

    # Ingreso del comentario
    tk.Label(ventana, text="Tu opinión:", font=FUENTE_GENERAL, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO).pack(pady=(10, 0))
    entrada_opinion = tk.Entry(ventana, width=40, font=FUENTE_GENERAL)
    entrada_opinion.pack(pady=5)

    # Selección de valoración
    tk.Label(ventana, text="Valoración (1 a 5):", font=FUENTE_GENERAL, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO).pack(pady=(10, 0))
    valoracion = tk.Spinbox(ventana, from_=1, to=5, width=5, font=FUENTE_GENERAL, justify=tk.CENTER)
    valoracion.pack(pady=5)

    # Listbox para mostrar feedbacks
    lista_feedback = tk.Listbox(ventana, width=45, height=8, font=FUENTE_GENERAL, bd=1, relief=tk.FLAT)
    lista_feedback.pack(pady=15, padx=10)

    # Función para agregar el feedback
    def enviar_feedback():
        nombre = entrada_nombre.get()
        opinion = entrada_opinion.get()
        puntuacion = valoracion.get()

        if nombre and opinion:
            # Estilo del texto en el Listbox
            texto = f"{nombre} (⭐{puntuacion}): {opinion}"
            lista_feedback.insert(tk.END, texto)
            
            # Limpiar entradas
            entrada_nombre.delete(0, tk.END)
            entrada_opinion.delete(0, tk.END)
            valoracion.delete(0, tk.END)
            valoracion.insert(0, "1")
            
            messagebox.showinfo("Gracias", "¡Opinión enviada con éxito!")


    boton_enviar = tk.Button(ventana, text="Enviar opinión", command=enviar_feedback,
                             font=FUENTE_GENERAL, bg=COLOR_ACENTO_TERCIARIO, fg='white', bd=0, activebackground=COLOR_ACENTO_TERCIARIO, activeforeground='white')
    boton_enviar.pack(pady=5)


# --- 4. CLASE PRINCIPAL DEL QUIZ ---
class QuizApp:
    def __init__(self, master):
        self.master = master
        master.title("🧠 Quiz App Modular (Tkinter)")
        master.geometry("700x450")
        master.config(bg=COLOR_FONDO_PRINCIPAL) # Fondo de la ventana principal

        # Estado
        self.category_var = tk.StringVar(master)
        self.category_var.set("Seleccionar Categoría")
        self.current_category = None
        self.questions = []
        self.current_q_index = 0
        self.score = 0
        self.mistakes = 0

        # Cronómetro
        self.start_time = None
        self.timer_id = None
        self.elapsed_time_var = tk.StringVar(master, value="Tiempo: 00:00")

        # Selección de opción
        self.selected_option = tk.StringVar()

        # Estadísticas
        self.estadisticas = None

        # UI
        self.create_widgets()
        self.show_start_screen()

    def create_widgets(self):
        # Marco principal
        self.main_frame = tk.Frame(self.master, padx=10, pady=10, bg=COLOR_FONDO_PRINCIPAL)
        self.main_frame.pack(fill='both', expand=True)

        # Menú de categorías
        category_label = tk.Label(self.main_frame, text="Categoría:", font=FUENTE_GENERAL, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TEXTO)
        category_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        categories = list(QUIZ_DATA.keys())
        category_menu = tk.OptionMenu(self.main_frame, self.category_var, *categories, command=self.load_category)
        category_menu.config(font=FUENTE_GENERAL, bg=COLOR_FONDO_SECUNDARIO, bd=1, relief=tk.FLAT, fg=COLOR_TEXTO)
        category_menu.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Cronómetro
        self.timer_label = tk.Label(self.main_frame, textvariable=self.elapsed_time_var, font=FUENTE_CRONOMETRO, bg=COLOR_FONDO_PRINCIPAL, fg=COLOR_TITULO)
        self.timer_label.grid(row=0, column=3, padx=5, pady=10, sticky="e")

        # Contenido (Marco principal de la pregunta)
        self.content_frame = tk.Frame(self.main_frame, bd=1, relief=tk.FLAT, padx=15, pady=15, bg=COLOR_FONDO_SECUNDARIO)
        self.content_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

        # Widgets de contenido
        self.question_label = tk.Label(self.content_frame, text="", wraplength=520, font=FUENTE_PREGUNTA, bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TITULO, justify=tk.LEFT, anchor='w')

        self.option_buttons = []
        for i in range(4):
            # Estilo de Radiobutton
            btn = tk.Radiobutton(self.content_frame, text="", variable=self.selected_option, value="", font=FUENTE_GENERAL, anchor="w",
                                 bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO, selectcolor=COLOR_FONDO_SECUNDARIO, activebackground=COLOR_FONDO_SECUNDARIO, activeforeground=COLOR_TEXTO)
            self.option_buttons.append(btn)

        self.submit_button = tk.Button(self.content_frame, text="Responder", command=self.check_answer, state=tk.DISABLED,
                                         font=FUENTE_GENERAL, bg=COLOR_ACENTO_PRIMARIO, fg='white', bd=0, height=1, activebackground=COLOR_ACENTO_PRIMARIO, activeforeground='white')

        self.feedback_label = tk.Label(self.content_frame, text="¡Selecciona una categoría para empezar!", font=FUENTE_PREGUNTA, bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO)

        self.restart_button = tk.Button(self.content_frame, text="🔁 Reiniciar Quiz", command=self.show_start_screen,
                                         font=FUENTE_GENERAL, bg=COLOR_ACENTO_SECUNDARIO, fg='white', bd=0, activebackground=COLOR_ACENTO_SECUNDARIO, activeforeground='white')

        self.details_button = tk.Button(self.content_frame, text="📝 Ver detalle de estadísticas",
                                         command=lambda: mostrar_estadisticas(self.master, self.estadisticas),
                                         font=FUENTE_GENERAL, bg='#7952B3', fg='white', bd=0, activebackground='#7952B3', activeforeground='white')
        
        self.feedback_button = tk.Button(self.content_frame, text="Dejar Feedback",
                                         command=lambda: abrir_feedback(self.master),
                                         font=FUENTE_GENERAL, bg=COLOR_ACENTO_TERCIARIO, fg='white', bd=0, activebackground=COLOR_ACENTO_TERCIARIO, activeforeground='white')


    def show_start_screen(self):
        # Detener cronómetro si estaba activo
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()

        # Reset de estado
        self.category_var.set("Seleccionar Categoría")
        self.current_category = None
        self.elapsed_time_var.set("Tiempo: 00:00")
        self.submit_button.config(state=tk.DISABLED)
        self.selected_option.set("")
        self.estadisticas = None

        # Mensaje de inicio
        self.feedback_label.config(text="👋 ¡Selecciona una categoría para empezar!", fg=COLOR_TEXTO, font=FUENTE_TITULO)
        self.feedback_label.grid(row=0, column=0, columnspan=4, pady=50)

    def load_category(self, category_name):
        if self.current_category == category_name:
            return

        # ... (Resto de la lógica de load_category es igual) ...
        # Estado base
        self.current_category = category_name
        self.questions = QUIZ_DATA[category_name][:]  # copia
        random.shuffle(self.questions)
        self.current_q_index = 0
        self.score = 0
        self.mistakes = 0
        self.start_time = time.time()
        self.estadisticas = Estadisticas(category_name)

        # Arrancar
        self.show_question()
        self.start_timer()
        self.submit_button.config(state=tk.NORMAL)


    def start_timer(self):
        # Cancelar timer anterior si existía
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

        def update_time():
            if self.start_time is not None:
                elapsed = int(time.time() - self.start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                self.elapsed_time_var.set(f"Tiempo: {minutes:02d}:{seconds:02d}")
                self.timer_id = self.master.after(1000, update_time)

        update_time()

    def stop_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

    def show_question(self):
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()

        if self.current_q_index < len(self.questions):
            q_data = self.questions[self.current_q_index]

            # Pregunta
            self.question_label.config(text=f"❓ Pregunta {self.current_q_index + 1}: {q_data['pregunta']}")
            self.question_label.grid(row=0, column=0, columnspan=4, pady=(10, 15), sticky="w")

            # Opciones (mezcladas)
            opciones = q_data['opciones'][:]
            random.shuffle(opciones)
            self.selected_option.set("")

            for i, option in enumerate(opciones):
                btn = self.option_buttons[i]
                btn.config(text=option, value=option, state=tk.NORMAL)
                btn.grid(row=i + 1, column=0, columnspan=4, sticky="w", padx=20, pady=5)

            # Botón responder
            self.submit_button.config(text="✅ Responder", command=self.check_answer, state=tk.NORMAL)
            self.submit_button.grid(row=len(opciones) + 1, column=0, columnspan=4, pady=(20, 10))

            # Feedback
            self.feedback_label.config(text="")
            self.feedback_label.grid(row=len(opciones) + 2, column=0, columnspan=4, pady=6)
        else:
            self.show_results()

    def check_answer(self):
        user_answer = self.selected_option.get()
        if not user_answer:
            messagebox.showwarning("Atención", "Por favor, selecciona una opción.")
            return

        correct_answer = self.questions[self.current_q_index]['respuesta']
        pregunta_texto = self.questions[self.current_q_index]['pregunta']

        # Registro de estadísticas
        self.estadisticas.registrar_respuesta(pregunta_texto, user_answer, correct_answer)

        # Feedback
        if user_answer == correct_answer:
            self.score += 1
            feedback_text = "✨ ¡Excelente! Respuesta Correcta."
            feedback_color = COLOR_ACENTO_PRIMARIO
        else:
            self.mistakes += 1
            feedback_text = f"❌ ¡Ups! Respuesta Incorrecta. La correcta era: {correct_answer}"
            feedback_color = COLOR_ERROR

        self.feedback_label.config(text=feedback_text, fg=feedback_color)

        # Siguiente
        self.submit_button.config(text="➡️ Siguiente Pregunta", command=self.next_question, bg=COLOR_ACENTO_SECUNDARIO, activebackground=COLOR_ACENTO_SECUNDARIO)

        # Deshabilitar opciones
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)

    def next_question(self):
        self.current_q_index += 1
        self.show_question()

    def show_results(self):
        self.stop_timer()

        # Cálculo de desempeño
        total_questions = len(self.questions)
        percentage = (self.score / total_questions) * 100 if total_questions > 0 else 0

        if percentage == 100:
            final_message = "🏆 ¡Felicidades! Un desempeño PERFECTO. ¡Eres un maestro!"
            final_color = '#007bff' # Azul fuerte
        elif percentage >= 70:
            final_message = "👍 ¡Muy bien! Un gran desempeño. Puedes mejorar el tiempo."
            final_color = COLOR_ACENTO_PRIMARIO
        else:
            final_message = "💪 ¡Podés mejorar! Sigue practicando."
            final_color = COLOR_ACENTO_TERCIARIO

        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()

        # Título y mensaje
        tk.Label(self.content_frame, text="🎉 *** FIN DEL QUIZ ***", font=('Segoe UI', 18, 'bold'), fg='#8B0000', bg=COLOR_FONDO_SECUNDARIO).grid(row=0, column=0, columnspan=4, pady=(20, 10))
        self.feedback_label.config(text=final_message, font=FUENTE_PREGUNTA, fg=final_color)
        self.feedback_label.grid(row=1, column=0, columnspan=4, pady=10)

        # Resumen rápido (aciertos/errores/tiempo)
        resumen = tk.Label(self.content_frame,
                           text=f"Aciertos: {self.score} | Errores: {self.mistakes} | Tiempo: {self.estadisticas.tiempo_total()} s | Categoría: {self.estadisticas.categoria}",
                           font=FUENTE_GENERAL, bg=COLOR_FONDO_SECUNDARIO, fg=COLOR_TEXTO)
        resumen.grid(row=2, column=0, columnspan=4, pady=8)

        # Botones
        self.details_button.grid(row=3, column=0, columnspan=4, pady=8)
        self.restart_button.grid(row=4, column=0, columnspan=4, pady=10)
        self.feedback_button.grid(row=5, column=0, columnspan=4, pady=10)


# --- 5. INICIO DE LA APP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()