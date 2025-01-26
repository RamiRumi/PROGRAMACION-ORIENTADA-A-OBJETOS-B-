import os
import logging
import threading
import sqlite3

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

class RecursoArchivo:
    """Maneja recursos de archivos con gestión de cierre"""
    def __init__(self, ruta, modo='r'):
        """Constructor que abre y prepara el archivo"""
        try:
            self.ruta = ruta
            self.archivo = open(ruta, modo)
            logging.info(f"Archivo {ruta} abierto exitosamente")
        except IOError as e:
            logging.error(f"Error al abrir el archivo: {e}")
            raise

    def __del__(self):
        """Destructor para cerrar recursos del archivo"""
        try:
            if hasattr(self, 'archivo'):
                self.archivo.close()
                logging.info(f"Archivo {self.ruta} cerrado correctamente")
        except Exception as e:
            logging.error(f"Error al cerrar el archivo: {e}")

class ConexionBaseDatos:
    """Gestiona conexiones a bases de datos SQLite"""
    def __init__(self, nombre_db='datos.sqlite'):
        """Constructor que establece conexión y crea tabla"""
        self.nombre_db = nombre_db
        self.conexion = sqlite3.connect(nombre_db)
        self.cursor = self.conexion.cursor()
        
        # Crear tabla de ejemplo
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                email TEXT
            )
        ''')
        self.conexion.commit()
        logging.info(f"Conexión a {nombre_db} establecida")

    def __del__(self):
        """Destructor para cerrar conexión de base de datos"""
        try:
            if hasattr(self, 'conexion'):
                self.conexion.close()
                logging.info(f"Conexión a {self.nombre_db} cerrada")
        except Exception as e:
            logging.error(f"Error al cerrar conexión: {e}")

class GestorTareas:
    """Administra tareas con hilos y mutex"""
    def __init__(self, num_hilos=5):
        """Constructor que inicializa hilos y semáforos"""
        self.num_hilos = num_hilos
        self.mutex = threading.Lock()
        self.tareas_pendientes = []
        self.hilos = []
        
        # Iniciar hilos de trabajo
        for i in range(num_hilos):
            hilo = threading.Thread(target=self._trabajador, daemon=True)
            hilo.start()
            self.hilos.append(hilo)
        
        logging.info(f"Gestor de tareas iniciado con {num_hilos} hilos")

    def _trabajador(self):
        """Método interno para procesar tareas"""
        while True:
            with self.mutex:
                if self.tareas_pendientes:
                    tarea = self.tareas_pendientes.pop(0)
                    tarea()

    def __del__(self):
        """Destructor para limpiar recursos de hilos"""
        for hilo in self.hilos:
            hilo.join(timeout=1)
        logging.info("Recursos de hilos liberados")

class MonitorRecursos:
    """Supervisa y limita el uso de recursos del sistema"""
    def __init__(self, limite_memoria_mb=100):
        """Constructor que establece límites de recursos"""
        self.limite_memoria = limite_memoria_mb * 1024 * 1024  # Convertir a bytes
        self.pid = os.getpid()
        
        # Registro de inicialización
        logging.info(f"Monitor de recursos iniciado para PID {self.pid}")
        logging.info(f"Límite de memoria establecido: {limite_memoria_mb} MB")

    def __del__(self):
        """Destructor que libera y registra la finalización"""
        logging.info(f"Monitor de recursos finalizado para PID {self.pid}")
        # Lógica adicional de liberación si es necesario

# Ejemplo de uso
def main():
    # Demostración de RecursoArchivo
    try:
        with RecursoArchivo('ejemplo.txt', 'w') as archivo:
            archivo.archivo.write("Hola, mundo!")
    except Exception as e:
        logging.error(f"Error en RecursoArchivo: {e}")

    # Demostración de ConexionBaseDatos
    db = ConexionBaseDatos()
    db.cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", 
                      ("Juan Pérez", "juan@example.com"))
    db.conexion.commit()

    # Demostración de GestorTareas
    gestor = GestorTareas(3)
    gestor.tareas_pendientes.append(lambda: print("Tarea 1"))
    gestor.tareas_pendientes.append(lambda: print("Tarea 2"))

    # Demostración de MonitorRecursos
    monitor = MonitorRecursos(200)

if __name__ == "__main__":
    main()
    