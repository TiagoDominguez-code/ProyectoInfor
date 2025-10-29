import tkinter as tk

# Preguntas
class Pregunta:
    def __init__(self, categoria, texto, respuesta, opciones):
        self.categoria = categoria
        self.texto = texto
        self.respuesta = respuesta
        self.opciones = opciones

# Lista de preguntas (HTML, CSS, Python)
preguntas = [
    Pregunta("HTML", "¿es un lenguaje de programacion?", "No", [
        "No", "Si", "Es un lenguaje de Datos", "Depende el punto de vista"
    ]),
    Pregunta("HTML", "¿Que significan las siglas HTML?", "Hyper Text Markup language", [
        "Hyper Text Markup language", "High Tech Modern Language", 
        "Hyperlink and Text Management Logic", "Home Tool Markup Language"
    ]),
    Pregunta("HTML", "¿Que etiqueta se utiliza para definir el cuerpo de un HTML donde va todo el contenido visible?", "body", [
        "body", "header", "footer", "main"
    ]),
    Pregunta("HTML", "¿Que etiqueta se usa para crear un enlace (hipervinculo) a otra pagina?", "<a>", [
        "<link>", "<a>", "<href>", "<Url>"
    ]),
    Pregunta("HTML", "Para crear una lista no ordenada, ¿que etiqueta utilizo?", "<ul>", [
        "<ol>", "<li>", "<ul>", "<list>"
    ]),
    Pregunta("CSS", "¿Qué significa CSS?", "Cascading Style Sheets", [
        "Cascading Style Sheets", "Creative Style Syntax", 
        "Computer Style System", "Central Styling Structure"
    ]),
    Pregunta("CSS", "¿Cuál propiedad se usa para cambiar el color del texto?", "color", [
        "text-color", "font-color", "color", "background-color"
    ]),
    Pregunta("CSS", "¿Qué selector se usa para aplicar estilo a todos los elementos de una clase?", ".nombreClase", [
        "#nombreClase", ".nombreClase", "nombreClase", "*nombreClase"
    ]),
    Pregunta("CSS", "¿Cuál propiedad controla el tamaño de la fuente?", "font-size", [
        "text-size", "font-style", "font-size", "size"
    ]),
    Pregunta("CSS", "¿Qué propiedad se usa para agregar espacio interno dentro de un elemento?", "padding", [
        "margin", "spacing", "padding", "border-spacing"
    ]),
    Pregunta("Python", "¿Qué tipo de lenguaje es Python?", "Interpretado", [
        "Compilado", "Interpretado", "Ensamblador", "Binario"
    ]),
    Pregunta("Python", "¿Cuál es la extensión típica de un archivo Python?", ".py", [
        ".py", ".pt", ".python", ".txt"
    ]),
    Pregunta("Python", "¿Qué palabra clave se usa para definir una función?", "def", [
        "func", "define", "def", "function"
    ]),
    Pregunta("Python", "¿Cuál estructura se usa para repetir un bloque de código mientras se cumple una condición?", "while", [
        "for", "repeat", "while", "loop"
    ]),
    Pregunta("Python", "¿Qué tipo de estructura es una lista en Python?", "Mutable", [
        "Inmutable", "Mutable", "Estática", "Constante"
    ]),
]

# Crear la ventana principal
ventana = tk.Tk()
ventana.title('Juego de Preguntas y Respuestas')
ventana.geometry('500x250')
ventana.configure(bg="#f0f8ff")  # Fondo suave

# Crear la barra de menú
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# Crear un submenú
submenu = tk.Menu(barra_menu, tearoff=0)
submenu.add_command(label='HTML')
submenu.add_command(label='CSS')
submenu.add_command(label='Python')
barra_menu.add_cascade(label='Categorías', menu=submenu)

# Mensaje de bienvenida
bienvenida = tk.Label(
    ventana,
    text="🎉 ¡Bienvenido al Juego de Preguntas RE! 🎉\nSeleccioná una categoría en el menú para comenzar.",
    font=("Helvetica", 12, "bold"),
    fg="#2e8b57",
    bg="#f0f8ff",
    pady=20,
    justify="center"
)
bienvenida.pack()

# Ejecutar el bucle principal de la interfaz
ventana.mainloop()
