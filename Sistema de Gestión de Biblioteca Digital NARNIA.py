"""
Sistema de Gestión de Biblioteca Digital
----------------------------------------
Este sistema permite administrar una biblioteca digital completa,
gestionando libros, usuarios, préstamos y devoluciones.
Especializado en libros que han sido adaptados a series de TV o películas.
"""

class Libro:
    """
    Clase que representa un libro en la biblioteca.
    Utiliza tuplas para almacenar datos inmutables como autor y título.
    """
    def __init__(self, titulo, autor, categoria, isbn, adaptacion=None):
        self.__datos_inmutables = (titulo, autor)  # Tupla para datos que no cambiarán
        self.__categoria = categoria
        self.__isbn = isbn
        self.__disponible = True
        self.__adaptacion = adaptacion  # Información sobre la adaptación a serie/película

    @property
    def titulo(self):
        return self.__datos_inmutables[0]
    
    @property
    def autor(self):
        return self.__datos_inmutables[1]
    
    @property
    def categoria(self):
        return self.__categoria
    
    @categoria.setter
    def categoria(self, nueva_categoria):
        self.__categoria = nueva_categoria
        
    @property
    def isbn(self):
        return self.__isbn
    
    @property
    def disponible(self):
        return self.__disponible
    
    @disponible.setter
    def disponible(self, estado):
        self.__disponible = estado
        
    @property
    def adaptacion(self):
        return self.__adaptacion
    
    @adaptacion.setter
    def adaptacion(self, info_adaptacion):
        self.__adaptacion = info_adaptacion
        
    def __str__(self):
        estado = "Disponible" if self.__disponible else "Prestado"
        adaptacion_info = f" - Adaptado a: {self.__adaptacion}" if self.__adaptacion else ""
        return f"'{self.titulo}' por {self.autor} - {self.categoria} - ISBN: {self.isbn}{adaptacion_info} - {estado}"


class Usuario:
    """
    Clase que representa a un usuario de la biblioteca.
    Mantiene un registro de los libros prestados al usuario.
    """
    def __init__(self, nombre, id_usuario):
        self.__nombre = nombre
        self.__id_usuario = id_usuario
        self.__libros_prestados = []  # Lista para almacenar los libros prestados
        
    @property
    def nombre(self):
        return self.__nombre
    
    @property
    def id_usuario(self):
        return self.__id_usuario
    
    @property
    def libros_prestados(self):
        return self.__libros_prestados
    
    def prestar_libro(self, libro):
        """Añade un libro a la lista de libros prestados del usuario"""
        self.__libros_prestados.append(libro)
        
    def devolver_libro(self, isbn):
        """Elimina un libro de la lista de libros prestados del usuario"""
        for i, libro in enumerate(self.__libros_prestados):
            if libro.isbn == isbn:
                return self.__libros_prestados.pop(i)
        return None
    
    def listar_libros_prestados(self):
        """Retorna una lista de los libros prestados al usuario"""
        return self.__libros_prestados
    
    def __str__(self):
        return f"Usuario: {self.__nombre} (ID: {self.__id_usuario}) - Libros prestados: {len(self.__libros_prestados)}"


class Biblioteca:
    """
    Clase principal que gestiona toda la biblioteca digital.
    Utiliza diccionarios para almacenar y acceder eficientemente a los libros.
    Utiliza conjuntos para asegurar IDs de usuario únicos.
    """
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__libros = {}  # Diccionario para almacenar libros (clave: ISBN, valor: objeto Libro)
        self.__usuarios = {}  # Diccionario para almacenar usuarios (clave: ID, valor: objeto Usuario)
        self.__ids_usuario = set()  # Conjunto para garantizar IDs únicos
        self.__historial_prestamos = []  # Lista para registrar el historial de préstamos
        
    @property
    def nombre(self):
        return self.__nombre
    
    def agregar_libro(self, libro):
        """
        Añade un nuevo libro a la biblioteca.
        Si ya existe un libro con el mismo ISBN, devuelve False.
        """
        if libro.isbn in self.__libros:
            return False
        self.__libros[libro.isbn] = libro
        return True
    
    def eliminar_libro(self, isbn):
        """Elimina un libro de la biblioteca por su ISBN"""
        if isbn in self.__libros and self.__libros[isbn].disponible:
            del self.__libros[isbn]
            return True
        return False
    
    def registrar_usuario(self, nombre, id_usuario):
        """
        Registra un nuevo usuario en la biblioteca.
        Si ya existe un usuario con el mismo ID, devuelve False.
        """
        if id_usuario in self.__ids_usuario:
            return False
        nuevo_usuario = Usuario(nombre, id_usuario)
        self.__usuarios[id_usuario] = nuevo_usuario
        self.__ids_usuario.add(id_usuario)
        return True
    
    def dar_baja_usuario(self, id_usuario):
        """
        Da de baja a un usuario de la biblioteca.
        Solo si no tiene libros prestados.
        """
        if id_usuario in self.__usuarios:
            usuario = self.__usuarios[id_usuario]
            if not usuario.libros_prestados:
                del self.__usuarios[id_usuario]
                self.__ids_usuario.remove(id_usuario)
                return True
        return False
    
    def prestar_libro(self, isbn, id_usuario):
        """
        Realiza el préstamo de un libro a un usuario.
        Retorna True si el préstamo fue exitoso, False en caso contrario.
        """
        if isbn in self.__libros and id_usuario in self.__usuarios:
            libro = self.__libros[isbn]
            usuario = self.__usuarios[id_usuario]
            
            if libro.disponible:
                libro.disponible = False
                usuario.prestar_libro(libro)
                # Registrar préstamo en el historial
                self.__historial_prestamos.append({"tipo": "préstamo", "isbn": isbn, "id_usuario": id_usuario})
                return True
        return False
    
    def devolver_libro(self, isbn, id_usuario):
        """
        Procesa la devolución de un libro prestado.
        Retorna True si la devolución fue exitosa, False en caso contrario.
        """
        if isbn in self.__libros and id_usuario in self.__usuarios:
            libro = self.__libros[isbn]
            usuario = self.__usuarios[id_usuario]
            
            libro_devuelto = usuario.devolver_libro(isbn)
            if libro_devuelto:
                libro.disponible = True
                # Registrar devolución en el historial
                self.__historial_prestamos.append({"tipo": "devolución", "isbn": isbn, "id_usuario": id_usuario})
                return True
        return False
    
    def buscar_libro_por_isbn(self, isbn):
        """Busca un libro por su ISBN"""
        return self.__libros.get(isbn)
    
    def buscar_libros_por_titulo(self, titulo):
        """Busca libros que contengan el título especificado"""
        return [libro for libro in self.__libros.values() 
                if titulo.lower() in libro.titulo.lower()]
    
    def buscar_libros_por_autor(self, autor):
        """Busca libros escritos por el autor especificado"""
        return [libro for libro in self.__libros.values() 
                if autor.lower() in libro.autor.lower()]
    
    def buscar_libros_por_categoria(self, categoria):
        """Busca libros de la categoría especificada"""
        return [libro for libro in self.__libros.values() 
                if categoria.lower() == libro.categoria.lower()]
    
    def buscar_libros_por_adaptacion(self, adaptacion):
        """Busca libros adaptados a una serie o película específica"""
        return [libro for libro in self.__libros.values() 
                if libro.adaptacion and adaptacion.lower() in libro.adaptacion.lower()]
    
    def listar_libros_prestados_usuario(self, id_usuario):
        """Lista todos los libros prestados a un usuario específico"""
        if id_usuario in self.__usuarios:
            return self.__usuarios[id_usuario].listar_libros_prestados()
        return []
    
    def listar_todos_libros(self):
        """Lista todos los libros de la biblioteca"""
        return list(self.__libros.values())
    
    def listar_usuarios(self):
        """Lista todos los usuarios registrados"""
        return list(self.__usuarios.values())
    
    def obtener_usuario(self, id_usuario):
        """Obtiene un usuario por su ID"""
        return self.__usuarios.get(id_usuario)


def mostrar_menu():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*60)
    print(f"{'SISTEMA DE GESTIÓN DE BIBLIOTECA DE LIBROS ADAPTADOS A SERIES':^60}")
    print("="*60)
    print(" 1. Gestión de Libros")
    print(" 2. Gestión de Usuarios")
    print(" 3. Préstamos y Devoluciones")
    print(" 4. Búsquedas")
    print(" 5. Informes")
    print(" 0. Salir del Sistema")
    print("="*60)
    return input("Seleccione una opción: ")


def menu_gestion_libros(biblioteca):
    """Submenú para gestión de libros"""
    while True:
        print("\n" + "-"*50)
        print(f"{'GESTIÓN DE LIBROS':^50}")
        print("-"*50)
        print(" 1. Añadir un nuevo libro")
        print(" 2. Eliminar un libro")
        print(" 3. Listar todos los libros")
        print(" 4. Ver detalles de un libro")
        print(" 0. Volver al menú principal")
        print("-"*50)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            titulo = input("Título del libro: ")
            autor = input("Autor del libro: ")
            categoria = input("Categoría del libro: ")
            isbn = input("ISBN del libro: ")
            adaptacion = input("Adaptación (serie/película) o deje en blanco si no tiene: ")
            
            if not adaptacion:
                adaptacion = None
                
            libro = Libro(titulo, autor, categoria, isbn, adaptacion)
            if biblioteca.agregar_libro(libro):
                print("\n✅ Libro añadido con éxito.")
            else:
                print("\n❌ Ya existe un libro con ese ISBN.")
                
        elif opcion == "2":
            isbn = input("Ingrese el ISBN del libro a eliminar: ")
            if biblioteca.eliminar_libro(isbn):
                print("\n✅ Libro eliminado con éxito.")
            else:
                print("\n❌ No se pudo eliminar el libro. Verifique que exista y no esté prestado.")
                
        elif opcion == "3":
            libros = biblioteca.listar_todos_libros()
            if libros:
                print("\nCATÁLOGO DE LIBROS:")
                for i, libro in enumerate(libros, 1):
                    print(f"{i}. {libro}")
            else:
                print("\n📚 No hay libros en la biblioteca.")
                
        elif opcion == "4":
            isbn = input("Ingrese el ISBN del libro: ")
            libro = biblioteca.buscar_libro_por_isbn(isbn)
            if libro:
                print(f"\nDETALLES DEL LIBRO:")
                print(f"Título: {libro.titulo}")
                print(f"Autor: {libro.autor}")
                print(f"Categoría: {libro.categoria}")
                print(f"ISBN: {libro.isbn}")
                if libro.adaptacion:
                    print(f"Adaptación: {libro.adaptacion}")
                print(f"Estado: {'Disponible' if libro.disponible else 'Prestado'}")
            else:
                print("\n❌ Libro no encontrado.")
                
        elif opcion == "0":
            break
            
        else:
            print("\n❌ Opción inválida, intente nuevamente.")


def menu_gestion_usuarios(biblioteca):
    """Submenú para gestión de usuarios"""
    while True:
        print("\n" + "-"*50)
        print(f"{'GESTIÓN DE USUARIOS':^50}")
        print("-"*50)
        print(" 1. Registrar nuevo usuario")
        print(" 2. Dar de baja a un usuario")
        print(" 3. Listar todos los usuarios")
        print(" 4. Ver detalles de un usuario")
        print(" 0. Volver al menú principal")
        print("-"*50)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            nombre = input("Nombre del usuario: ")
            id_usuario = input("ID del usuario: ")
            
            if biblioteca.registrar_usuario(nombre, id_usuario):
                print("\n✅ Usuario registrado con éxito.")
            else:
                print("\n❌ Ya existe un usuario con ese ID.")
                
        elif opcion == "2":
            id_usuario = input("Ingrese el ID del usuario a dar de baja: ")
            if biblioteca.dar_baja_usuario(id_usuario):
                print("\n✅ Usuario dado de baja con éxito.")
            else:
                print("\n❌ No se pudo dar de baja al usuario. Verifique que exista y no tenga libros prestados.")
                
        elif opcion == "3":
            usuarios = biblioteca.listar_usuarios()
            if usuarios:
                print("\nUSUARIOS REGISTRADOS:")
                for i, usuario in enumerate(usuarios, 1):
                    print(f"{i}. {usuario}")
            else:
                print("\n👤 No hay usuarios registrados.")
                
        elif opcion == "4":
            id_usuario = input("Ingrese el ID del usuario: ")
            usuario = biblioteca.obtener_usuario(id_usuario)
            if usuario:
                print(f"\nDETALLES DEL USUARIO:")
                print(f"Nombre: {usuario.nombre}")
                print(f"ID: {usuario.id_usuario}")
                print(f"Libros prestados: {len(usuario.libros_prestados)}")
                
                if usuario.libros_prestados:
                    print("\nLIBROS PRESTADOS:")
                    for i, libro in enumerate(usuario.libros_prestados, 1):
                        print(f"{i}. {libro.titulo} (ISBN: {libro.isbn})")
            else:
                print("\n❌ Usuario no encontrado.")
                
        elif opcion == "0":
            break
            
        else:
            print("\n❌ Opción inválida, intente nuevamente.")


def menu_prestamos_devoluciones(biblioteca):
    """Submenú para préstamos y devoluciones"""
    while True:
        print("\n" + "-"*50)
        print(f"{'PRÉSTAMOS Y DEVOLUCIONES':^50}")
        print("-"*50)
        print(" 1. Prestar un libro")
        print(" 2. Devolver un libro")
        print(" 3. Ver libros prestados a un usuario")
        print(" 0. Volver al menú principal")
        print("-"*50)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            id_usuario = input("ID del usuario: ")
            isbn = input("ISBN del libro: ")
            
            usuario = biblioteca.obtener_usuario(id_usuario)
            libro = biblioteca.buscar_libro_por_isbn(isbn)
            
            if not usuario:
                print("\n❌ Usuario no encontrado.")
            elif not libro:
                print("\n❌ Libro no encontrado.")
            elif not libro.disponible:
                print("\n❌ El libro no está disponible actualmente.")
            elif biblioteca.prestar_libro(isbn, id_usuario):
                print(f"\n✅ Libro '{libro.titulo}' prestado con éxito a {usuario.nombre}.")
            else:
                print("\n❌ No se pudo realizar el préstamo.")
                
        elif opcion == "2":
            id_usuario = input("ID del usuario: ")
            isbn = input("ISBN del libro: ")
            
            usuario = biblioteca.obtener_usuario(id_usuario)
            libro = biblioteca.buscar_libro_por_isbn(isbn)
            
            if not usuario:
                print("\n❌ Usuario no encontrado.")
            elif not libro:
                print("\n❌ Libro no encontrado.")
            elif biblioteca.devolver_libro(isbn, id_usuario):
                print(f"\n✅ Libro '{libro.titulo}' devuelto con éxito por {usuario.nombre}.")
            else:
                print("\n❌ No se pudo realizar la devolución. Verifique que el libro esté prestado a este usuario.")
                
        elif opcion == "3":
            id_usuario = input("ID del usuario: ")
            usuario = biblioteca.obtener_usuario(id_usuario)
            
            if usuario:
                libros_prestados = biblioteca.listar_libros_prestados_usuario(id_usuario)
                if libros_prestados:
                    print(f"\nLIBROS PRESTADOS A {usuario.nombre.upper()}:")
                    for i, libro in enumerate(libros_prestados, 1):
                        print(f"{i}. {libro.titulo} (ISBN: {libro.isbn})")
                else:
                    print(f"\n📚 El usuario {usuario.nombre} no tiene libros prestados.")
            else:
                print("\n❌ Usuario no encontrado.")
                
        elif opcion == "0":
            break
            
        else:
            print("\n❌ Opción inválida, intente nuevamente.")


def menu_busquedas(biblioteca):
    """Submenú para búsquedas"""
    while True:
        print("\n" + "-"*50)
        print(f"{'BÚSQUEDAS':^50}")
        print("-"*50)
        print(" 1. Buscar por título")
        print(" 2. Buscar por autor")
        print(" 3. Buscar por categoría")
        print(" 4. Buscar por ISBN")
        print(" 5. Buscar por adaptación")
        print(" 0. Volver al menú principal")
        print("-"*50)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            titulo = input("Ingrese el título a buscar: ")
            resultados = biblioteca.buscar_libros_por_titulo(titulo)
            mostrar_resultados_busqueda(resultados)
                
        elif opcion == "2":
            autor = input("Ingrese el autor a buscar: ")
            resultados = biblioteca.buscar_libros_por_autor(autor)
            mostrar_resultados_busqueda(resultados)
                
        elif opcion == "3":
            categoria = input("Ingrese la categoría a buscar: ")
            resultados = biblioteca.buscar_libros_por_categoria(categoria)
            mostrar_resultados_busqueda(resultados)
                
        elif opcion == "4":
            isbn = input("Ingrese el ISBN a buscar: ")
            libro = biblioteca.buscar_libro_por_isbn(isbn)
            if libro:
                print("\nRESULTADO DE LA BÚSQUEDA:")
                print(f"1. {libro}")
            else:
                print("\n📚 No se encontraron resultados.")
                
        elif opcion == "5":
            adaptacion = input("Ingrese la adaptación a buscar (serie/película): ")
            resultados = biblioteca.buscar_libros_por_adaptacion(adaptacion)
            mostrar_resultados_busqueda(resultados)
                
        elif opcion == "0":
            break
            
        else:
            print("\n❌ Opción inválida, intente nuevamente.")


def mostrar_resultados_busqueda(resultados):
    """Muestra los resultados de una búsqueda"""
    if resultados:
        print("\nRESULTADOS DE LA BÚSQUEDA:")
        for i, libro in enumerate(resultados, 1):
            print(f"{i}. {libro}")
    else:
        print("\n📚 No se encontraron resultados.")


def menu_informes(biblioteca):
    """Submenú para informes"""
    while True:
        print("\n" + "-"*50)
        print(f"{'INFORMES':^50}")
        print("-"*50)
        print(" 1. Listado de libros disponibles")
        print(" 2. Listado de libros prestados")
        print(" 3. Estadísticas de la biblioteca")
        print(" 4. Listado de libros por adaptación")
        print(" 0. Volver al menú principal")
        print("-"*50)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            libros = biblioteca.listar_todos_libros()
            disponibles = [libro for libro in libros if libro.disponible]
            
            if disponibles:
                print("\nLIBROS DISPONIBLES:")
                for i, libro in enumerate(disponibles, 1):
                    print(f"{i}. {libro}")
                print(f"\nTotal: {len(disponibles)} libros disponibles")
            else:
                print("\n📚 No hay libros disponibles.")
                
        elif opcion == "2":
            libros = biblioteca.listar_todos_libros()
            prestados = [libro for libro in libros if not libro.disponible]
            
            if prestados:
                print("\nLIBROS PRESTADOS:")
                for i, libro in enumerate(prestados, 1):
                    print(f"{i}. {libro}")
                print(f"\nTotal: {len(prestados)} libros prestados")
            else:
                print("\n📚 No hay libros prestados actualmente.")
                
        elif opcion == "3":
            libros = biblioteca.listar_todos_libros()
            usuarios = biblioteca.listar_usuarios()
            
            total_libros = len(libros)
            disponibles = sum(1 for libro in libros if libro.disponible)
            prestados = total_libros - disponibles
            
            print("\nESTADÍSTICAS DE LA BIBLIOTECA:")
            print(f"Total de libros: {total_libros}")
            print(f"Libros disponibles: {disponibles}")
            print(f"Libros prestados: {prestados}")
            print(f"Porcentaje de préstamo: {(prestados/total_libros*100) if total_libros else 0:.2f}%")
            print(f"Total de usuarios: {len(usuarios)}")
            
            # Categorías más populares
            categorias = {}
            for libro in libros:
                categorias[libro.categoria] = categorias.get(libro.categoria, 0) + 1
            
            if categorias:
                print("\nCategorías de libros:")
                for categoria, cantidad in sorted(categorias.items(), key=lambda x: x[1], reverse=True):
                    print(f"- {categoria}: {cantidad} libros")
                    
            # Adaptaciones más populares
            adaptaciones = {}
            for libro in libros:
                if libro.adaptacion:
                    adaptaciones[libro.adaptacion] = adaptaciones.get(libro.adaptacion, 0) + 1
            
            if adaptaciones:
                print("\nLibros por adaptación:")
                for adaptacion, cantidad in sorted(adaptaciones.items(), key=lambda x: x[1], reverse=True):
                    print(f"- {adaptacion}: {cantidad} libros")
                
        elif opcion == "4":
            libros = biblioteca.listar_todos_libros()
            adaptados = {}
            
            for libro in libros:
                if libro.adaptacion:
                    if libro.adaptacion not in adaptados:
                        adaptados[libro.adaptacion] = []
                    adaptados[libro.adaptacion].append(libro)
            
            if adaptados:
                print("\nLIBROS POR ADAPTACIÓN:")
                for adaptacion, lista_libros in sorted(adaptados.items()):
                    print(f"\n== {adaptacion.upper()} ==")
                    for i, libro in enumerate(lista_libros, 1):
                        print(f"{i}. {libro.titulo} por {libro.autor}")
                print(f"\nTotal: {sum(len(libros) for libros in adaptados.values())} libros adaptados")
            else:
                print("\n📚 No hay libros con adaptaciones registradas.")
                
        elif opcion == "0":
            break
            
        else:
            print("\n❌ Opción inválida, intente nuevamente.")


def main():
    """Función principal del programa"""
    print("\n¡Bienvenido al Sistema de Gestión de Biblioteca de Libros Adaptados a Series!")
    nombre_biblioteca = input("Ingrese el nombre de la biblioteca: ")
    biblioteca = Biblioteca(nombre_biblioteca)
    
    # Agregar datos de ejemplo con libros adaptados a series
    cargar_datos_ejemplo(biblioteca)
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            menu_gestion_libros(biblioteca)
        elif opcion == "2":
            menu_gestion_usuarios(biblioteca)
        elif opcion == "3":
            menu_prestamos_devoluciones(biblioteca)
        elif opcion == "4":
            menu_busquedas(biblioteca)
        elif opcion == "5":
            menu_informes(biblioteca)
        elif opcion == "0":
            print("\n¡Gracias por utilizar el Sistema de Gestión de Biblioteca Digital!")
            break
        else:
            print("\n❌ Opción inválida, intente nuevamente.")


def cargar_datos_ejemplo(biblioteca):
    """Carga datos de ejemplo para demostración - Libros adaptados a series/películas"""
    # Crear libros famosos adaptados a series/películas
    libros = [
        Libro("Juego de Tronos", "George R.R. Martin", "Fantasía Épica", "9788496208964", "Game of Thrones (HBO)"),
        Libro("Los Juegos del Hambre", "Suzanne Collins", "Distopía/Aventura", "9788427202122", "The Hunger Games (Película)"),
        Libro("Harry Potter y la Piedra Filosofal", "J.K. Rowling", "Fantasía Juvenil", "9788478884452", "Harry Potter (Saga de películas)"),
        Libro("El Hobbit", "J.R.R. Tolkien", "Fantasía", "9788445073803", "El Hobbit (Trilogía de películas)"),
        Libro("The Witcher: El último deseo", "Andrzej Sapkowski", "Fantasía", "9788498890785", "The Witcher (Netflix)"),
        Libro("Fundación", "Isaac Asimov", "Ciencia Ficción", "9788497594257", "Foundation (Apple TV+)"),
        Libro("Outlander", "Diana Gabaldon", "Romance Histórico", "9788498387087", "Outlander (STARZ)"),
        Libro("American Gods", "Neil Gaiman", "Fantasía Contemporánea", "9788498005516", "American Gods (STARZ)"),
        Libro("Altered Carbon", "Richard Morgan", "Ciencia Ficción", "9788496940000", "Altered Carbon (Netflix)"),
        Libro("Buenos Presagios", "Terry Pratchett y Neil Gaiman", "Comedia Fantástica", "9788448006426", "Good Omens (Amazon Prime)"),
        Libro("El Cuento de la Criada", "Margaret Atwood", "Distopía", "9788423353897", "The Handmaid's Tale (Hulu)"),
        Libro("Soy Leyenda", "Richard Matheson", "Terror/Ciencia Ficción", "9788445076538", "I Am Legend (Película)")
    ]
    
    # Agregar libros a la biblioteca
    for libro in libros:
        biblioteca.agregar_libro(libro)
    
    # Crear algunos usuarios
    usuarios = [
        ("Ana García", "U001"),
        ("Carlos López", "U002"),
        ("María Rodríguez", "U003"),
        ("Pedro Sánchez", "U004"),
        ("Laura Martínez", "U005")
    ]
    
    # Registrar usuarios
    for nombre, id_usuario in usuarios:
        biblioteca.registrar_usuario(nombre, id_usuario)
    
    # Realizar algunos préstamos
    biblioteca.prestar_libro("9788498890785", "U001")  # The Witcher para Ana
    biblioteca.prestar_libro("9788496208964", "U002")  # Juego de Tronos para Carlos
    biblioteca.prestar_libro("9788498005516", "U003")  # American Gods para María
    biblioteca.prestar_libro("9788445076538", "U004")  # Soy Leyenda para Pedro
    biblioteca.prestar_libro("9788423353897", "U005")  # El Cuento de la Criada para Laura
    biblioteca.prestar_libro("9788448006426", "U001")  # Buenos Presagios para Ana


if __name__ == "__main__":
    main()