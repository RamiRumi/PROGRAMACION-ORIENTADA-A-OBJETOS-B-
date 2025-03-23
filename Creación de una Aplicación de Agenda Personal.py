import tkinter as tk
from tkinter import ttk, messagebox

class AgendaBasica:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Básica")

        # Frame principal
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # TreeView para eventos
        self.tree = ttk.Treeview(self.main_frame, columns=("Fecha", "Hora", "Descripción"), show="headings")
        self.tree.heading("Fecha", text="Fecha (DD/MM/AAAA)")
        self.tree.heading("Hora", text="Hora (HH:MM)")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.pack()

        # Frame para entrada de datos
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(pady=10)

        # Campos de entrada
        ttk.Label(self.input_frame, text="Fecha:").grid(row=0, column=0, padx=5)
        self.date_entry = ttk.Entry(self.input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5)
        self.date_entry.insert(0, "DD/MM/AAAA")

        ttk.Label(self.input_frame, text="Hora:").grid(row=0, column=2, padx=5)
        self.time_entry = ttk.Entry(self.input_frame, width=10)
        self.time_entry.grid(row=0, column=3, padx=5)
        self.time_entry.insert(0, "HH:MM")

        ttk.Label(self.input_frame, text="Descripción:").grid(row=1, column=0, padx=5)
        self.desc_entry = ttk.Entry(self.input_frame, width=30)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, sticky="we")

        # Botones
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=5)

        ttk.Button(self.button_frame, text="Agregar", command=self.agregar_evento).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Eliminar", command=self.eliminar_evento).pack(side="left", padx=5)
        ttk.Button(self.button_frame, text="Salir", command=root.quit).pack(side="left", padx=5)

    def agregar_evento(self):
        fecha = self.date_entry.get()
        hora = self.time_entry.get()
        desc = self.desc_entry.get()

        if fecha and hora and desc and fecha != "DD/MM/AAAA" and hora != "HH:MM":
            self.tree.insert("", "end", values=(fecha, hora, desc))
            self.date_entry.delete(0, "end")
            self.time_entry.delete(0, "end")
            self.desc_entry.delete(0, "end")
        else:
            messagebox.showwarning("Error", "¡Datos inválidos o incompletos!")

    def eliminar_evento(self):
        seleccionado = self.tree.selection()
        if seleccionado:
            self.tree.delete(seleccionado)
        else:
            messagebox.showwarning("Error", "¡Selecciona un evento!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaBasica(root)
    root.mainloop()