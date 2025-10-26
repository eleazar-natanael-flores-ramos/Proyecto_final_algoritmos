import tkinter as tk
from tkinter import ttk
from fractions import Fraction
import subprocess

# ---------------- Funciones ----------------

def generar_campos():
    for widget in frame_campos.winfo_children():
        widget.destroy()

    try:
        n = int(combo_tamano.get())
    except ValueError:
        mostrar_resultado("Error", "Seleccione un tamaño válido.")
        return

    global entradas
    entradas = []

    # Etiquetas para columnas
    for j in range(n):
        tk.Label(frame_campos, text=f"x{j+1}", font=("Arial", 10, "bold")).grid(row=0, column=j, padx=5, pady=5)
    tk.Label(frame_campos, text="=", font=("Arial", 10, "bold")).grid(row=0, column=n, padx=5, pady=5)

    for i in range(n):
        fila = []
        for j in range(n):
            entry = tk.Entry(frame_campos, width=6, justify="center")
            entry.grid(row=i+1, column=j, padx=5, pady=5)
            fila.append(entry)
        entry_ind = tk.Entry(frame_campos, width=6, justify="center", bg="#f0f0f0")
        entry_ind.grid(row=i+1, column=n, padx=5, pady=5)
        fila.append(entry_ind)
        entradas.append(fila)

# ---------------- Métodos de resolución ----------------

def resolver_gauss_jordan(matriz):
    n = len(matriz)
    for i in range(n):
        if abs(matriz[i][i]) < 1e-12:
            for k in range(i+1, n):
                if abs(matriz[k][i]) > 1e-12:
                    matriz[i], matriz[k] = matriz[k], matriz[i]
                    break
        divisor = matriz[i][i]
        if abs(divisor) < 1e-12:
            continue
        for j in range(n+1):
            matriz[i][j] /= divisor
        for k in range(n):
            if k != i:
                factor = matriz[k][i]
                for j in range(n+1):
                    matriz[k][j] -= factor * matriz[i][j]
    return matriz

def diagnosticar(matriz):
    n = len(matriz)
    soluciones = [0]*n
    tipo = "única"
    for i in range(n):
        fila = matriz[i]
        coef = fila[:-1]
        indep = fila[-1]
        if all(abs(c) < 1e-12 for c in coef) and abs(indep) > 1e-12:
            return "sin solución", None
        elif all(abs(c) < 1e-12 for c in coef) and abs(indep) < 1e-12:
            tipo = "infinitas"
    if tipo == "infinitas":
        return "infinitas", None
    for i in range(n):
        soluciones[i] = matriz[i][-1]
    return "única", soluciones

def determinante(matriz):
    n = len(matriz)
    if n == 1:
        return matriz[0][0]
    if n == 2:
        return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]
    det = 0
    for c in range(n):
        submatriz = [fila[:c]+fila[c+1:] for fila in matriz[1:]]
        det += ((-1)**c) * matriz[0][c] * determinante(submatriz)
    return det

def resolver_cramer(matriz):
    n = len(matriz)
    coef = [fila[:-1] for fila in matriz]
    indep = [fila[-1] for fila in matriz]
    det_principal = determinante(coef)
    if abs(det_principal) > 1e-12:
        soluciones = []
        for i in range(n):
            temp = [fila[:] for fila in coef]
            for j in range(n):
                temp[j][i] = indep[j]
            det_i = determinante(temp)
            soluciones.append(det_i/det_principal)
        return "única", soluciones
    else:
        todos_det = []
        for i in range(n):
            temp = [fila[:] for fila in coef]
            for j in range(n):
                temp[j][i] = indep[j]
            det_i = determinante(temp)
            todos_det.append(det_i)
        if all(abs(d) < 1e-12 for d in todos_det):
            return "infinitas", None
        else:
            return "sin solución", None

# ---------------- Formatear resultados ----------------

def formatear_resultado(valor):
    if abs(valor - round(valor)) < 1e-12:
        return str(int(round(valor)))
    else:
        frac = Fraction(valor).limit_denominator()
        return f"{frac.numerator}/{frac.denominator}"

# ---------------- Ventana de resultados ----------------

def mostrar_resultado(titulo, mensaje):
    ventana = tk.Toplevel(root)
    ventana.title(titulo)
    ventana.resizable(False, False)

    ancho = 400
    alto = 300
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    # Frame principal
    frame = tk.Frame(ventana, padx=10, pady=10)
    frame.pack(expand=True, fill="both")

    # Text para mostrar mensaje
    text = tk.Text(frame, wrap="word", font=("Arial", 12), height=10)
    text.insert("1.0", mensaje)
    text.configure(state="disabled")
    text.pack(expand=True, fill="both")

    # Frame para el botón
    frame_btn = tk.Frame(ventana)
    frame_btn.pack(pady=5)

    tk.Button(frame_btn, text="Cerrar", command=ventana.destroy, bg="#4CAF50", fg="white").pack()

# ---------------- Resolver sistema ----------------

def resolver_sistema():
    try:
        n = int(combo_tamano.get())
        matriz = []
        for i in range(n):
            fila = []
            for j in range(n+1):
                valor = float(entradas[i][j].get())
                fila.append(valor)
            matriz.append(fila)

        metodo = combo_metodo.get()
        if metodo == "Gauss-Jordan":
            matriz_gj = resolver_gauss_jordan([fila[:] for fila in matriz])
            tipo, soluciones = diagnosticar(matriz_gj)
        else:
            tipo, soluciones = resolver_cramer(matriz)

        if tipo == "única":
            resultado = "\n".join([f"x{i+1} = {formatear_resultado(soluciones[i])}" for i in range(n)])
            mostrar_resultado("Solución única", resultado)
        elif tipo == "infinitas":
            mostrar_resultado("Resultado", "El sistema tiene infinitas soluciones.")
        else:
            mostrar_resultado("Resultado", "El sistema no tiene solución.")

    except ValueError:
        mostrar_resultado("Error", "Todos los campos deben ser numéricos.")
    except ZeroDivisionError:
        mostrar_resultado("Error", "División por cero detectada.")

def regresar():
    root.destroy()
    subprocess.run(['python', 'PROYECTO_FINAL/Algebra/Main_algebra.py'])

# ---------------- Interfaz gráfica ----------------

root = tk.Tk()
root.title("Sistemas Lineales")
root.geometry("600x480")
root.state("zoomed")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Tamaño:").pack(side="left")
combo_tamano = ttk.Combobox(frame_top, values=["2","3","4"], width=5, state="readonly")
combo_tamano.pack(side="left", padx=5)
combo_tamano.set("2")

tk.Label(frame_top, text="Método:").pack(side="left", padx=(20,0))
combo_metodo = ttk.Combobox(frame_top, values=["Gauss-Jordan","Cramer"], width=12, state="readonly")
combo_metodo.pack(side="left", padx=5)
combo_metodo.set("Gauss-Jordan")

tk.Button(frame_top, text="Generar campos", command=generar_campos).pack(side="left", padx=10)

frame_campos = tk.Frame(root)
frame_campos.pack(pady=10)

tk.Button(root, text="Resolver sistema", command=resolver_sistema, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(root, text="Regresar al menú principal", command=regresar, bg="#f44336", fg="white").pack(pady=5)

generar_campos()
root.mainloop()
