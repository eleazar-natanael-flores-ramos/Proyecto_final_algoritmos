import tkinter as tk
from tkinter import ttk, messagebox
import subprocess


def multiplicar_matrices_manual(matriz_a, matriz_b):
    """Realiza la multiplicación de dos matrices (A * B)."""
    try:
        filas_a = len(matriz_a)
        cols_a = len(matriz_a[0]) if filas_a > 0 and matriz_a[0] else 0
        filas_b = len(matriz_b)
        cols_b = len(matriz_b[0]) if filas_b > 0 and matriz_b[0] else 0
    except (IndexError, TypeError):
        return "Error: Asegúrate de que ambas matrices estén completamente llenas con datos válidos."

    if cols_a != filas_b:
        return f"Error: No se pueden multiplicar. El número de columnas de A ({cols_a}) debe ser igual al número de filas de B ({filas_b})."

    resultado = [[0 for _ in range(cols_b)] for _ in range(filas_a)]
    for i in range(filas_a):
        for j in range(cols_b):
            resultado[i][j] = sum(matriz_a[i][k] * matriz_b[k][j] for k in range(cols_a))
    return resultado


# ----------------------------------------------------
# INTERFAZ TKINTER
# ----------------------------------------------------

class MatrixApp:
    def __init__(self, master):
        master.title("Multiplicación de Matrices Dinámica")
        master.geometry("1000x700")  # tamaño ajustable
        master.minsize(800, 600)     # tamaño mínimo
        master.state("zoomed")       # inicia maximizada, pero con barra normal

        self.master = master
        self.MAX_DIMENSION = 4
        self.entry_a = []
        self.entry_b = []
        self.rows_a = tk.IntVar(value=2)
        self.cols_a = tk.IntVar(value=2)
        self.rows_b = tk.IntVar(value=2)
        self.cols_b = tk.IntVar(value=2)

        # --- Frame principal centrado ---
        self.main_frame = tk.Frame(master)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")  # centra todo

        # Sincronización automática de dimensiones
        self.cols_a.trace_add("write", lambda *args: self.sync_b_rows())
        self.rows_b.trace_add("write", lambda *args: self.sync_a_cols())

        self.create_widgets()

    def regresar(self):
        self.master.destroy()
        subprocess.run(['python', 'PROYECTO_FINAL/Algebra/Main_algebra.py'])

    def sync_b_rows(self):
        try:
            if self.rows_b.get() != self.cols_a.get():
                self.rows_b.set(self.cols_a.get())
                self.update_matrices()
        except tk.TclError:
            pass

    def sync_a_cols(self):
        try:
            if self.cols_a.get() != self.rows_b.get():
                self.cols_a.set(self.rows_b.get())
                self.update_matrices()
        except tk.TclError:
            pass

    def create_widgets(self):
        # --- Frame superior de controles ---
        frame_controls = tk.LabelFrame(self.main_frame, text=f"Definir Dimensiones (Máx {self.MAX_DIMENSION}x{self.MAX_DIMENSION})")
        frame_controls.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Controles de A
        tk.Label(frame_controls, text="Matriz A (Filas x Cols):").grid(row=0, column=0, padx=5, pady=2)
        ttk.Entry(frame_controls, textvariable=self.rows_a, width=4).grid(row=0, column=1)
        tk.Label(frame_controls, text="x").grid(row=0, column=2)
        ttk.Entry(frame_controls, textvariable=self.cols_a, width=4).grid(row=0, column=3)

        # Controles de B
        tk.Label(frame_controls, text="Matriz B (Filas x Cols):").grid(row=1, column=0, padx=5, pady=2)
        ttk.Entry(frame_controls, textvariable=self.rows_b, width=4).grid(row=1, column=1)
        tk.Label(frame_controls, text="x").grid(row=1, column=2)
        ttk.Entry(frame_controls, textvariable=self.cols_b, width=4).grid(row=1, column=3)

        ttk.Button(frame_controls, text="Aplicar", command=self.update_matrices).grid(row=0, column=4, rowspan=2, padx=10)
        ttk.Button(frame_controls, text="Regresar al menú principal", command=self.regresar).grid(row=0, column=5, rowspan=2, padx=10)

        # --- Contenedor de matrices ---
        self.container_matrices = tk.Frame(self.main_frame)
        self.container_matrices.grid(row=1, column=0, columnspan=2, pady=10)

        self.frame_a = tk.LabelFrame(self.container_matrices, text="Matriz A")
        self.frame_a.grid(row=0, column=0, padx=10, pady=10)

        self.frame_b = tk.LabelFrame(self.container_matrices, text="Matriz B")
        self.frame_b.grid(row=0, column=1, padx=10, pady=10)

        # --- Botón de calcular ---
        tk.Button(self.main_frame, text="Multiplicar A * B", command=self.calcular).grid(row=2, column=0, columnspan=2, pady=10)

        # --- Resultado ---
        tk.Label(self.main_frame, text="Resultado (Matriz C):").grid(row=3, column=0, columnspan=2, sticky='w', padx=10)
        self.result_text = tk.Text(self.main_frame, height=6, width=50, state='disabled')
        self.result_text.grid(row=4, column=0, columnspan=2, pady=10)

        self.update_matrices()

    def update_matrices(self):
        try:
            r_a, c_a, r_b, c_b = self.rows_a.get(), self.cols_a.get(), self.rows_b.get(), self.cols_b.get()
        except tk.TclError:
            messagebox.showerror("Error", "Las dimensiones deben ser números enteros.")
            return

        if any(x > self.MAX_DIMENSION for x in [r_a, c_a, r_b, c_b]):
            messagebox.showwarning("Límite", f"El tamaño máximo es {self.MAX_DIMENSION}x{self.MAX_DIMENSION}.")
            self.rows_a.set(min(r_a, self.MAX_DIMENSION))
            self.cols_a.set(min(c_a, self.MAX_DIMENSION))
            self.rows_b.set(min(r_b, self.MAX_DIMENSION))
            self.cols_b.set(min(c_b, self.MAX_DIMENSION))
            return

        if c_a != r_b:
            messagebox.showinfo("Ajuste", f"Col(A) ≠ Fil(B). Se ajustó Fil(B) a {c_a}.")
            self.rows_b.set(c_a)
            r_b = c_a

        for w in self.frame_a.winfo_children(): w.destroy()
        for w in self.frame_b.winfo_children(): w.destroy()
        self.entry_a.clear()
        self.entry_b.clear()

        self.frame_a.config(text=f"Matriz A ({r_a}x{c_a})")
        self.create_matrix_inputs(self.frame_a, self.entry_a, r_a, c_a)
        self.frame_b.config(text=f"Matriz B ({r_b}x{c_b})")
        self.create_matrix_inputs(self.frame_b, self.entry_b, r_b, c_b)

    def create_matrix_inputs(self, frame, entry_list, rows, cols):
        for r in range(rows):
            fila = []
            for c in range(cols):
                e = tk.Entry(frame, width=5, justify="center")
                e.insert(0, "0")
                e.grid(row=r, column=c, padx=4, pady=4)
                fila.append(e)
            entry_list.append(fila)

    def get_matrix_data(self, entry_list, rows, cols):
        try:
            return [[float(entry_list[r][c].get()) for c in range(cols)] for r in range(rows)]
        except ValueError:
            messagebox.showerror("Error", "Solo se permiten números válidos.")
            return None

    def display_result(self, result):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        if isinstance(result, str):
            self.result_text.insert(tk.END, result)
        else:
            for row in result:
                fila = "  ".join(f"{x:7.2f}" for x in row)
                self.result_text.insert(tk.END, f"[ {fila} ]\n")
        self.result_text.config(state="disabled")

    def calcular(self):
        r_a, c_a, r_b, c_b = self.rows_a.get(), self.cols_a.get(), self.rows_b.get(), self.cols_b.get()
        a = self.get_matrix_data(self.entry_a, r_a, c_a)
        b = self.get_matrix_data(self.entry_b, r_b, c_b)
        if a is None or b is None:
            return
        res = multiplicar_matrices_manual(a, b)
        self.display_result(res)


# ----------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ----------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixApp(root)
    root.mainloop()
