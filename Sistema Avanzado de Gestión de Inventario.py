import json
import os

class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def get_info(self):
        return {
            "ID": self.id,
            "Nombre": self.nombre,
            "Cantidad": self.cantidad,
            "Precio": self.precio
        }

    def actualizar(self, cantidad=None, precio=None):
        if cantidad is not None:
            self.cantidad = cantidad
        if precio is not None:
            self.precio = precio

class Inventario:
    def __init__(self):
        self.productos = {}  # Diccionario para acceso rápido por ID

    def añadir_producto(self, producto):
        if producto.id in self.productos:
            raise ValueError("Error: ID ya existe")
        self.productos[producto.id] = producto

    def eliminar_producto(self, id):
        if id not in self.productos:
            raise KeyError("Error: ID no encontrado")
        del self.productos[id]

    def buscar_por_nombre(self, nombre):
        return [p for p in self.productos.values() if p.nombre.lower() == nombre.lower()]

    def actualizar_producto(self, id, cantidad=None, precio=None):
        producto = self.productos.get(id)
        if not producto:
            raise KeyError("Error: Producto no encontrado")
        producto.actualizar(cantidad, precio)

    def mostrar_todo(self):
        return [p.get_info() for p in self.productos.values()]

def guardar_datos(inventario, archivo="inventario.json"):
    with open(archivo, 'w') as f:
        datos = [vars(p) for p in inventario.productos.values()]
        json.dump(datos, f, indent=4)

def cargar_datos(archivo="inventario.json"):
    inventario = Inventario()
    if os.path.exists(archivo):
        with open(archivo, 'r') as f:
            try:
                datos = json.load(f)
                for item in datos:
                    producto = Producto(**item)
                    inventario.añadir_producto(producto)
            except json.JSONDecodeError:
                pass
    return inventario

def menu():
    inventario = cargar_datos()
    
    while True:
        print("\n--- Sistema de Gestión de Inventario ---")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Guardar y salir")
        
        opcion = input("Seleccione una opción: ")
        
        try:
            if opcion == "1":
                id = input("ID del producto: ")
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                producto = Producto(id, nombre, cantidad, precio)
                inventario.añadir_producto(producto)
                print("Producto añadido exitosamente!")
            
            elif opcion == "2":
                id = input("ID del producto a eliminar: ")
                inventario.eliminar_producto(id)
                print("Producto eliminado!")
            
            elif opcion == "3":
                id = input("ID del producto a actualizar: ")
                cantidad = input("Nueva cantidad (dejar vacío para no cambiar): ")
                precio = input("Nuevo precio (dejar vacío para no cambiar): ")
                
                kwargs = {}
                if cantidad: kwargs['cantidad'] = int(cantidad)
                if precio: kwargs['precio'] = float(precio)
                
                inventario.actualizar_producto(id, **kwargs)
                print("Producto actualizado!")
            
            elif opcion == "4":
                nombre = input("Nombre a buscar: ")
                resultados = inventario.buscar_por_nombre(nombre)
                for p in resultados:
                    print(p.get_info())
            
            elif opcion == "5":
                for p in inventario.mostrar_todo():
                    print(p)
            
            elif opcion == "6":
                guardar_datos(inventario)
                print("Datos guardados. ¡Hasta luego!")
                break
            
            else:
                print("Opción no válida")
        
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    menu()