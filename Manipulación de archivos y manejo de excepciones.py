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
import os

class Inventario:
    def __init__(self, archivo='inventario.txt'):
        self.archivo = archivo
        self.productos = {}
        self._ultimo_id = 0
        self._cargar_inventario()

    def _cargar_inventario(self):
        """Carga el inventario desde el archivo"""
        try:
            if not os.path.exists(self.archivo):
                open(self.archivo, 'w').close()
                
            with open(self.archivo, 'r') as f:
                for linea in f:
                    datos = linea.strip().split(',')
                    if len(datos) != 4:
                        continue
                    try:
                        id_prod = int(datos[0])
                        nombre = datos[1]
                        cantidad = int(datos[2])
                        precio = float(datos[3])
                        self.productos[id_prod] = Producto(id_prod, nombre, cantidad, precio)
                        self._ultimo_id = max(self._ultimo_id, id_prod)
                    except (ValueError, IndexError):
                        print(f"Advertencia: Formato inválido en línea: {linea}")
        except PermissionError:
            print("Error: Sin permisos para leer el archivo de inventario")
        except Exception as e:
            print(f"Error inesperado al cargar inventario: {str(e)}")

    def _guardar_inventario(self):
        """Guarda todo el inventario en el archivo"""
        try:
            with open(self.archivo, 'w') as f:
                for producto in self.productos.values():
                    f.write(f"{producto.id},{producto.nombre},{producto.cantidad},{producto.precio}\n")
            return True
        except PermissionError:
            print("Error: Sin permisos para escribir en el archivo")
            return False
        except Exception as e:
            print(f"Error al guardar inventario: {str(e)}")
            return False

    def generar_id(self):
        self._ultimo_id += 1
        return self._ultimo_id

    def agregar_producto(self, nombre, cantidad, precio):
        try:
            id_producto = self.generar_id()
            nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
            self.productos[id_producto] = nuevo_producto
            if self._guardar_inventario():
                return id_producto
            else:
                del self.productos[id_producto]
                self._ultimo_id -= 1
                return None
        except Exception as e:
            print(f"Error al agregar producto: {str(e)}")
            return None

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            producto = self.productos.pop(id_producto)
            if self._guardar_inventario():
                return True
            else:
                self.productos[id_producto] = producto
                return False
        return False

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto in self.productos:
            producto = self.productos[id_producto]
            original = (producto.cantidad, producto.precio)
            
            try:
                if cantidad is not None:
                    producto.cantidad = cantidad
                if precio is not None:
                    producto.precio = precio
            except ValueError as e:
                print(f"Error: {str(e)}")
                return False
            
            if self._guardar_inventario():
                return True
            else:
                producto.cantidad, producto.precio = original
                return False
        return False

    def buscar_por_nombre(self, nombre):
        return [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]

    def mostrar_inventario(self):
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
            nombre = input("Ingrese el nombre del producto: ").strip()
            try:
                cantidad = int(input("Ingrese la cantidad: "))
                precio = float(input("Ingrese el precio: "))
                id_producto = inventario.agregar_producto(nombre, cantidad, precio)
                if id_producto:
                    print(f"Producto agregado con ID: {id_producto} y guardado exitosamente")
                else:
                    print("Error: No se pudo guardar el producto en el archivo")
            except ValueError as e:
                print(f"Error en los datos ingresados: {str(e)}")

        elif opcion == "2":
            try:
                id_producto = int(input("Ingrese el ID del producto a eliminar: "))
                if inventario.eliminar_producto(id_producto):
                    print("Producto eliminado y cambios guardados exitosamente")
                else:
                    print("Error al eliminar o guardar los cambios")
            except ValueError:
                print("ID inválido")

        elif opcion == "3":
            try:
                id_producto = int(input("Ingrese el ID del producto a actualizar: "))
                cantidad = input("Nueva cantidad (dejar vacío para mantener): ").strip()
                precio = input("Nuevo precio (dejar vacío para mantener): ").strip()
                
                nueva_cantidad = int(cantidad) if cantidad else None
                nuevo_precio = float(precio) if precio else None
                
                if inventario.actualizar_producto(id_producto, nueva_cantidad, nuevo_precio):
                    print("Producto actualizado y cambios guardados exitosamente")
                else:
                    print("Error al actualizar o guardar los cambios")
            except ValueError as e:
                print(f"Error en los datos ingresados: {str(e)}")

        elif opcion == "4":
            nombre = input("Ingrese el nombre a buscar: ").strip()
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                print("\nResultados de búsqueda:")
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos")

        elif opcion == "5":
            inventario_completo = inventario.mostrar_inventario()
            if inventario_completo:
                print("\nInventario completo:")
                for p in inventario_completo:
                    print(p)
            else:
                print("El inventario está vacío")

        elif opcion == "6":
            print("¡Gracias por usar el sistema!")
            break

        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()