import tkinter as tk
import time

# --- Clase Estadisticas ---
class Estadisticas:
    def __init__(self, categoria):
        self.categoria = categoria
        self.aciertos = 0
        self.errores = 0
        self.inicio = time.time()
        self.detalle = []  # (pregunta, respuesta_usuario, respuesta_correcta, estado)

    def registrar_respuesta(self, pregunta, respuesta_usuario):
        # Comprueba si es la respuesta correcta
        correcto = respuesta_usuario == pregunta["respuesta"]

        if correcto:
            self.aciertos += 1
        else:
            self.errores += 1

        # Registra los datos de cada pregunta para el resumen final
        self.detalle.append((
            pregunta["pregunta"],  # texto de la pregunta
            respuesta_usuario,     # lo que eligió el usuario
            pregunta["respuesta"], # la respuesta correcta
            "✔️¡Correcta!" if correcto else "Incorrecta"
        ))

    def tiempo_total(self):
        return round(time.time() - self.inicio, 2)


# --- Función para mostrar estadísticas ---
def mostrar_estadisticas(ventana, estadisticas):
    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.title("Resultados del intento")
    ventana_resultados.geometry("")  # autoajuste al contenido
    ventana_resultados.resizable(False, False)

    titulo = tk.Label(
        ventana_resultados,
        text=f"Resultados - Categoría {estadisticas.categoria}",
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
    resumen.pack(pady=5)

    # Scroll de la tabla
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

    # Encabezado
    encabezado = tk.Frame(scrollable_frame, bg="#d9ead3")
    encabezado.pack(fill="x")
    tk.Label(encabezado, text="Pregunta", width=40, anchor="w", bg="#d9ead3").grid(row=0, column=0)
    tk.Label(encabezado, text="Tu respuesta", width=20, anchor="w", bg="#d9ead3").grid(row=0, column=1)
    tk.Label(encabezado, text="Correcta", width=20, anchor="w", bg="#d9ead3").grid(row=0, column=2)
    tk.Label(encabezado, text="Estado", width=20, anchor="w", bg="#d9ead3").grid(row=0, column=3)

    # Resultados en filas
    for i, (preg, resp_user, resp_ok, estado) in enumerate(estadisticas.detalle, start=1):
        fila = tk.Frame(scrollable_frame)
        fila.pack(fill="x")
        tk.Label(fila, text=preg, width=40, anchor="w").grid(row=i, column=0)
        tk.Label(fila, text=resp_user, width=20, anchor="w").grid(row=i, column=1)
        tk.Label(fila, text=resp_ok, width=20, anchor="w").grid(row=i, column=2)
        tk.Label(fila, text=estado, width=20, anchor="w",
                 fg="#2e8b57" if "✔️" in estado else "#d9534f").grid(row=i, column=3)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Botón cierre
    tk.Button(ventana_resultados, text="Cerrar", command=ventana_resultados.destroy).pack(pady=10)


# --- Ejemplo de uso ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Demo Estadísticas")
    root.geometry("")  # autoajuste
    root.resizable(True, True)

    # Crear estadísticas de prueba
    estadisticas = Estadisticas("HTML")
    pregunta1 = {"pregunta": "¿Qué significa HTML?", "respuesta": "Hyper Text Markup language"}
    pregunta2 = {"pregunta": "¿Es Python compilado?", "respuesta": "No"}

    estadisticas.registrar_respuesta(pregunta1, "Hyper Text Markup language")  # correcta
    estadisticas.registrar_respuesta(pregunta2, "Sí")  # incorrecta

    # Botón para abrir ventana de resultados
    tk.Button(root, text="Mostrar Estadísticas",
              command=lambda: mostrar_estadisticas(root, estadisticas)).pack(pady=20)

    root.mainloop()
