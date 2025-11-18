import tkinter as tk
from tkinter import messagebox, ttk
import random
import time

# --- 1. DATOS DEL JUEGO (Simula un archivo JSON o carga de datos) ---
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



class QuizApp:
    """Clase principal para la aplicación de Quiz en Tkinter."""
    def __init__(self, master):
        self.master = master
        master.title("Quiz App Modular (Tkinter)")

        # Variables de estado
        self.category_var = tk.StringVar(master)
        self.category_var.set("Seleccionar Categoría")
        self.current_category = None
        self.questions = []
        self.current_q_index = 0
        self.score = 0
        self.mistakes = 0
        
        # Variables del cronómetro (Módulo 2)
        self.start_time = None
        self.timer_id = None
        self.elapsed_time_var = tk.StringVar(master, value="Tiempo: 00:00")
        
        # Variable para la opción seleccionada del usuario
        self.selected_option = tk.StringVar()
        
        self.create_widgets()
        self.show_start_screen()

    def create_widgets(self):
        """Inicializa los frames y widgets de la interfaz."""
        # Configuración principal de la interfaz
        self.main_frame = tk.Frame(self.master, padx=10, pady=10)
        self.main_frame.pack(fill='both', expand=True)
        
        # Módulo 1: Interfaz y navegación (Menú de categorías)
        category_label = tk.Label(self.main_frame, text="Categoría:", font=('Arial', 12))
        category_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        
        categories = list(QUIZ_DATA.keys())
        category_menu = tk.OptionMenu(self.main_frame, self.category_var, *categories, command=self.load_category)
        category_menu.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        # Widget para mostrar el tiempo (Módulo 2: Cronómetro)
        self.timer_label = tk.Label(self.main_frame, textvariable=self.elapsed_time_var, font=('Consolas', 14, 'bold'))
        self.timer_label.grid(row=0, column=3, padx=5, pady=10, sticky="e")

        # Contenedor para el área de preguntas y resultados
        self.content_frame = tk.Frame(self.main_frame, bd=2, relief=tk.SUNKEN, padx=10, pady=10)
        self.content_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=10)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1) # Columna de relleno para alinear timer a la derecha

        # Inicializar widgets de contenido que se actualizarán
        self.question_label = tk.Label(self.content_frame, text="", wraplength=400, font=('Arial', 14, 'bold'))
        self.option_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(self.content_frame, text="", variable=self.selected_option, value="", font=('Arial', 12), anchor="w")
            self.option_buttons.append(btn)
        
        self.submit_button = tk.Button(self.content_frame, text="Responder", command=self.check_answer, state=tk.DISABLED, font=('Arial', 12), bg='#4CAF50', fg='white')
        
        # Módulo 4: Retroalimentación
        self.feedback_label = tk.Label(self.content_frame, text="¡Selecciona una categoría para empezar!", font=('Arial', 14, 'italic'))
        
        # Módulo 3: Tabla de resultados (Treeview para mostrar al final)
        self.results_tree = ttk.Treeview(self.content_frame, columns=("Aciertos", "Errores", "Tiempo"), show="headings", height=1)
        self.results_tree.heading("Aciertos", text="Aciertos")
        self.results_tree.heading("Errores", text="Errores")
        self.results_tree.heading("Tiempo", text="Tiempo Total")
        self.results_tree.column("Aciertos", width=80, anchor=tk.CENTER)
        self.results_tree.column("Errores", width=80, anchor=tk.CENTER)
        self.results_tree.column("Tiempo", width=120, anchor=tk.CENTER)
        
        self.restart_button = tk.Button(self.content_frame, text="Reiniciar Quiz", command=self.show_start_screen, font=('Arial', 12), bg='#2196F3', fg='white')


    def show_start_screen(self):
        """Muestra la pantalla de inicio/selección de categoría."""
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        
        # Limpiar y mostrar solo el mensaje de inicio y el menú
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()
            
        self.category_var.set("Seleccionar Categoría")
        self.current_category = None
        self.elapsed_time_var.set("Tiempo: 00:00")
        self.submit_button.config(state=tk.DISABLED)
        
        self.feedback_label.config(text="¡Selecciona una categoría para empezar!", fg='black')
        self.feedback_label.grid(row=0, column=0, columnspan=4, pady=50)

    # --- Módulo 1: Lógica de categorías y Módulo 2: Cronómetro ---
    def load_category(self, category_name):
        """Carga las preguntas de la categoría seleccionada y empieza el quiz."""
        if self.current_category == category_name:
            return # Ya cargada
            
        self.current_category = category_name
        self.questions = QUIZ_DATA[category_name][:] # Copia las preguntas
        random.shuffle(self.questions) 
        self.current_q_index = 0
        self.score = 0
        self.mistakes = 0
        self.start_time = time.time()
        
        self.show_question()
        self.start_timer()
        self.submit_button.config(state=tk.NORMAL)
        
    def start_timer(self):
        """Inicia y actualiza el cronómetro usando after() de Tkinter."""
        if self.timer_id:
            self.master.after_cancel(self.timer_id) # Cancela el timer anterior

        def update_time():
            if self.start_time is not None:
                elapsed = int(time.time() - self.start_time)
                minutes = elapsed // 60
                seconds = elapsed % 60
                self.elapsed_time_var.set(f"Tiempo: {minutes:02d}:{seconds:02d}")
                # Llama a sí misma después de 1000ms (1 segundo)
                self.timer_id = self.master.after(1000, update_time)
        
        update_time()

    def stop_timer(self):
        """Detiene el cronómetro."""
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

    # --- Módulo 3: Lógica del juego y Módulo 4: Retroalimentación ---
    def show_question(self):
        """Muestra la pregunta actual y sus opciones."""
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()
            
        self.feedback_label.grid_forget()
        self.results_tree.grid_forget()
        self.restart_button.grid_forget()

        if self.current_q_index < len(self.questions):
            q_data = self.questions[self.current_q_index]
            
            # Etiqueta de la pregunta
            self.question_label.config(text=f"Pregunta {self.current_q_index + 1}: {q_data['pregunta']}")
            self.question_label.grid(row=0, column=0, columnspan=4, pady=(20, 10))

            # Opciones de respuesta (RadioButtons)
            random.shuffle(q_data['opciones']) # Opcional: mezclar opciones
            self.selected_option.set("") # Deseleccionar opción anterior
            
            for i, option in enumerate(q_data['opciones']):
                btn = self.option_buttons[i]
                btn.config(text=option, value=option)
                btn.grid(row=i + 1, column=0, columnspan=4, sticky="w", padx=20, pady=5)
            
            self.submit_button.grid(row=len(q_data['opciones']) + 1, column=0, columnspan=4, pady=20)
            self.submit_button.config(text="Responder", state=tk.NORMAL)
            self.feedback_label.config(text="")
            self.feedback_label.grid(row=len(q_data['opciones']) + 2, column=0, columnspan=4, pady=10)

        else:
            self.show_results() # Fin del quiz

    def check_answer(self):
        """Valida la respuesta del usuario y avanza a la siguiente pregunta."""
        user_answer = self.selected_option.get()
        if not user_answer:
            messagebox.showwarning("Atención", "Por favor, selecciona una opción.")
            return

        correct_answer = self.questions[self.current_q_index]['respuesta']

        # Lógica y Retroalimentación (Módulos 3 y 4)
        if user_answer == correct_answer:
            self.score += 1
            feedback_text = "¡Excelente! Respuesta Correcta. 😊"
            feedback_color = 'green'
        else:
            self.mistakes += 1
            feedback_text = f"¡Ups! Respuesta Incorrecta. La correcta era: {correct_answer} 😟"
            feedback_color = 'red'

        self.feedback_label.config(text=feedback_text, fg=feedback_color)
        self.submit_button.config(text="Siguiente Pregunta", command=self.next_question)
        
        # Deshabilitar botones de opción para evitar doble respuesta
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
            
        self.submit_button.config(command=self.next_question)

    def next_question(self):
        """Avanza al siguiente índice y llama a show_question."""
        self.current_q_index += 1
        
        # Re-habilitar botones de opción
        for btn in self.option_buttons:
            btn.config(state=tk.NORMAL, command=self.check_answer) # Restaurar comando
            
        self.show_question()
        self.submit_button.config(command=self.check_answer) # Restaurar comando

    # --- Módulo 3 y 5: Estadística e Integración/Testing ---
    def show_results(self):
        """Muestra la tabla final de resultados."""
        self.stop_timer()
        
        # Calcular tiempo final y mensaje
        final_time = self.elapsed_time_var.get().split(": ")[1]
        
        # Retroalimentación final (Módulo 4)
        total_questions = len(self.questions)
        percentage = (self.score / total_questions) * 100
        
        if percentage == 100:
            final_message = "¡Felicidades! Un desempeño PERFECTO. 🏆"
            final_color = 'blue'
        elif percentage >= 70:
            final_message = "¡Muy bien! Un gran desempeño. Puedes mejorar el tiempo. 👍"
            final_color = 'green'
        else:
            final_message = "¡Podés mejorar! Sigue practicando. 💪"
            final_color = 'orange'
            
        # Limpiar y mostrar resultados
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()
            
        # Título y mensaje
        tk.Label(self.content_frame, text="*** FIN DEL QUIZ ***", font=('Arial', 18, 'bold'), fg='#8B0000').grid(row=0, column=0, columnspan=4, pady=(20, 10))
        self.feedback_label.config(text=final_message, font=('Arial', 14, 'bold'), fg=final_color)
        self.feedback_label.grid(row=1, column=0, columnspan=4, pady=10)

        # Módulo 3: Tabla de Resultados
        self.results_tree.delete(*self.results_tree.get_children()) # Limpiar si hay datos
        self.results_tree.insert("", tk.END, values=(self.score, self.mistakes, final_time))
        self.results_tree.grid(row=2, column=0, columnspan=4, pady=20, padx=50)
        
        # Botón de reinicio
        self.restart_button.grid(row=3, column=0, columnspan=4, pady=10)

# --- Integración y Testing (Módulo 5) ---
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()