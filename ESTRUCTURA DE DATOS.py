# producto.py
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def precio(self):
        return self._precio

    # Setters
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        if nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa")

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio >= 0:
            self._precio = nuevo_precio
        else:
            raise ValueError("El precio no puede ser negativo")

    def __str__(self):
        return f"ID: {self._id} | Nombre: {self._nombre} | Cantidad: {self._cantidad} | Precio: ${self._precio:.2f}"


# inventario.py
class Inventario:
    def __init__(self):
        self.productos = {}
        self._ultimo_id = 0

    def generar_id(self):
        """Genera un ID único para cada producto"""
        self._ultimo_id += 1
        return self._ultimo_id

    def agregar_producto(self, nombre, cantidad, precio):
        """Añade un nuevo producto al inventario"""
        id_producto = self.generar_id()
        nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
        self.productos[id_producto] = nuevo_producto
        return id_producto

    def eliminar_producto(self, id_producto):
        """Elimina un producto del inventario por su ID"""
        if id_producto in self.productos:
            del self.productos[id_producto]
            return True
        return False

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """Actualiza la cantidad o precio de un producto"""
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto].cantidad = cantidad
            if precio is not None:
                self.productos[id_producto].precio = precio
            return True
        return False

    def buscar_por_nombre(self, nombre):
        """Busca productos por nombre (búsqueda parcial)"""
        return [producto for producto in self.productos.values() 
                if nombre.lower() in producto.nombre.lower()]

    def mostrar_inventario(self):
        """Muestra todos los productos en el inventario"""
        return list(self.productos.values())


# main.py
def mostrar_menu():
    print("\n=== SISTEMA DE INVENTARIO DE PRODUCTOS DE BELLEZA PARA UÑAS ===")
    print("1. Agregar nuevo producto")
    print("2. Eliminar producto")
    print("3. Actualizar producto")
    print("4. Buscar productos por nombre")
    print("5. Mostrar todo el inventario")
    print("6. Salir")
    return input("Seleccione una opción: ")

def main():
    inventario = Inventario()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            nombre = input("Ingrese el nombre del producto: ")
            try:
                cantidad = int(input("Ingrese la cantidad: "))
                precio = float(input("Ingrese el precio: "))
                id_producto = inventario.agregar_producto(nombre, cantidad, precio)
                print(f"Producto agregado con ID: {id_producto}")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "2":
            try:
                id_producto = int(input("Ingrese el ID del producto a eliminar: "))
                if inventario.eliminar_producto(id_producto):
                    print("Producto eliminado exitosamente")
                else:
                    print("Producto no encontrado")
            except ValueError:
                print("ID inválido")

        elif opcion == "3":
            try:
                id_producto = int(input("Ingrese el ID del producto a actualizar: "))
                cantidad = input("Nueva cantidad (presione Enter para mantener actual): ")
                precio = input("Nuevo precio (presione Enter para mantener actual): ")
                
                cantidad = int(cantidad) if cantidad else None
                precio = float(precio) if precio else None
                
                if inventario.actualizar_producto(id_producto, cantidad, precio):
                    print("Producto actualizado exitosamente")
                else:
                    print("Producto no encontrado")
            except ValueError as e:
                print(f"Error: Valor inválido ingresado")

        elif opcion == "4":
            nombre = input("Ingrese el nombre a buscar: ")
            productos = inventario.buscar_por_nombre(nombre)
            if productos:
                print("\nProductos encontrados:")
                for producto in productos:
                    print(producto)
            else:
                print("No se encontraron productos con ese nombre")

        elif opcion == "5":
            productos = inventario.mostrar_inventario()
            if productos:
                print("\nInventario completo:")
                for producto in productos:
                    print(producto)
            else:
                print("El inventario está vacío")

        elif opcion == "6":
            print("¡Gracias por usar el sistema!")
            break

        else:
            print("Opción inválida. Por favor, intente nuevamente.")

if __name__ == "__main__":
    main()