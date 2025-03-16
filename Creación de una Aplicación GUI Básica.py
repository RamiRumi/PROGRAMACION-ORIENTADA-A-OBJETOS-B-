import tkinter as tk
from tkinter import ttk, messagebox

class AplicacionDatos:
    def __init__(self, root):
        self.root = root
        self.configurar_ventana()
        self.crear_componentes()
        
    def configurar_ventana(self):
        self.root.title("Gestor de Datos v2.0")
        self.root.geometry("500x400")
        self.root.minsize(400, 300)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        
    def crear_componentes(self):
        # Etiqueta
        ttk.Label(self.root, text="Ingrese dato:").grid(
            row=0, column=0, padx=10, pady=10, sticky="e")
            
        # Campo de texto
        self.entrada = ttk.Entry(self.root)
        self.entrada.grid(
            row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entrada.bind("<Return>", lambda e: self.agregar_dato())
        
        # Botón Agregar
        ttk.Button(self.root, text="Agregar", 
                 command=self.agregar_dato).grid(
                     row=0, column=2, padx=10, pady=10)
                     
        # Lista con scroll
        self.lista = tk.Listbox(self.root, selectmode=tk.SINGLE)
        scroll = ttk.Scrollbar(self.root, 
                             orient="vertical", 
                             command=self.lista.yview)
        self.lista.configure(yscrollcommand=scroll.set)
        
        self.lista.grid(row=2, column=0, columnspan=2, 
                      padx=10, pady=10, sticky="nsew")
        scroll.grid(row=2, column=2, sticky="ns")
        
        # Botón Limpiar
        ttk.Button(self.root, text="Limpiar", 
                 command=self.limpiar).grid(
                     row=3, column=0, columnspan=3, 
                     padx=10, pady=10, sticky="ew")
                     
    def agregar_dato(self):
        dato = self.entrada.get().strip()
        if dato:
            self.lista.insert(tk.END, dato)
            self.entrada.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "El campo no puede estar vacío")
            
    def limpiar(self):
        # Eliminar selección de la lista
        if self.lista.curselection():
            self.lista.delete(self.lista.curselection())
        # Limpiar campo de entrada
        self.entrada.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionDatos(root)
    root.mainloop()