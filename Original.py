import tkinter as tk

#Importar tiempo para las estadisticas
import time 


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

#---------------------------------------------------------

#Estadisticas (Aciertos, Errores, tiempo, categoría) | Tabla de Resultados 

class Estadisticas:
    def __init__(self, categoria):
        self.categoria = categoria
        self.aciertos = 0
        self.errores = 0
        self.inicio = time.time() # Momento en el que se inicia
        self.detalle = [] #Lista de tuplas con (pregunta, respuesta_usuario, respuesta_correcta, estado)
    

    #Registrar respuestas
    def registrar_respuesta(self, pregunta, respuesta_usuario):
        #Comprueba si es la respuesta correcta
        correcto = respuesta_usuario == pregunta.respuesta

        if correcto:
            self.aciertos += 1
        else:
            self.errores += 1
        
        #Registra los datos de cada pregunta para el resumen final


        #Revisar esto para corroborar si da bien el resultado en |Resultado en Filas|

        self.detalle.append((
            pregunta.texto, # texto de la pregunta
            respuesta_usuario, # lo que eligio el usuario
            pregunta.respuesta, # la respuesta correcta
            "✔️¡Correcta!" if correcto else "Incorrecta")) # Corrobora si lo que eligio el usuario es Correcto o Incorrecto.

    #Calcular tiempo total en segundos
    def tiempo_total(self):
        return round(time.time() - self.inicio, 2)


#Grafico

def mostrar_estadisticas(ventana, estadisticas):
    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.title("Resultados del intento")
    ventana_resultados.geometry("600x400")

    titulo = tk.Label(
        ventana_resultados,
        text=f"Resultados - Categoria {estadisticas.categoria}",
        font=("Helvetica", 14, "bold"),
        fg="#2e8b57"
    )
    titulo.pack(pady=10)

    resumen = tk.Label(
        ventana_resultados,
        text=f"Aciertos: {estadisticas.aciertos} | Errores: {estadisticas.errores} | "
        f"Tiempo: {estadisticas.tiempo_total()} segundos",
        font=("Helvetica", 11),
        fg="#333"
    )
    titulo.pack(pady=5)

    #Scroll de la tabla

    frame_tabla = tk.Frame(ventana_resultados)
    frame_tabla.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_tabla)
    scrollbar = tk.Scrollbar(frame_tabla, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)


    #Encabezado

    encabezado = tk.Frame(scrollable_frame, bg="#d9ead3")
    encabezado.pack(fill="x")
    tk.Label(encabezado, text="Pregunta", width=40, anchor="w",bg="#d9ead3").grid(row=0,column=0)
    tk.Label(encabezado, text="Tu respuesta", width=20, anchor="w",bg="#d9ead3").grid(row=0,column=1)
    tk.Label(encabezado, text="Correcta", width=20, anchor="w",bg="#d9ead3").grid(row=0,column=2)
    tk.Label(encabezado, text="Estado", width=20, anchor="w",bg="#d9ead3").grid(row=0,column=3)


    #Resultados en filas

    #-----------aca revisar el LABEL ESTADO y testearlo-----------

    for i, (preg, resp_user, resp_ok, estado) in enumerate(estadisticas.detalle, start=1):
        fila = tk.Frame(scrollable_frame)
        fila.pack(fill="x")
        tk.Label(fila, text=preg, width=40, anchor="w").grid(row=i, column=0)
        tk.Label(fila,text=resp_user, width=20, anchor="w").grid(row=i, column=1)
        tk.Label(fila,text=resp_ok, width=20, anchor="w").grid(row=i, column=2)
        tk.Label(fila,text=estado, width=20, anchor="w", fg="#2e8b57" if "✔️" in estado else "#d9534f").grid(row=i, column=3)


    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")




    #Boton cierre

    tk.Button(ventana_resultados,text="Cerrar", command=ventana_resultados.destroy).pack(pady=10)

#------------------------------------------------------


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
