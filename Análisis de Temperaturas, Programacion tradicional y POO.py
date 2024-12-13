# Análisis de Temperaturas

# Módulo de Funciones Tradicionales
def ingresar_temperaturas_tradicional():
    "Función para ingresar temperaturas utilizando programación tradicional"
    temperaturas = []
    dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    print("\n--- Registro de Temperaturas (Enfoque Tradicional) ---")
    for dia in dias:
        while True:
            try:
                temperatura = float(input(f"Ingrese la temperatura para {dia}: "))
                temperaturas.append(temperatura)
                break
            except ValueError:
                print("Error: Ingrese un valor numérico válido.")
    
    return temperaturas

def calcular_promedio_tradicional(temperaturas):
    "Calcula el promedio de temperaturas"
    if not temperaturas:
        return 0
    return sum(temperaturas) / len(temperaturas)

def analizar_temperaturas_tradicional(temperaturas):
    "Analiza las temperaturas con métodos tradicionales"
    promedio = calcular_promedio_tradicional(temperaturas)
    temperatura_maxima = max(temperaturas)
    temperatura_minima = min(temperaturas)
    
    print("\n--- Resultados (Método Tradicional) ---")
    print(f"Temperaturas registradas: {temperaturas}")
    print(f"Promedio semanal: {promedio:.2f}°C")
    print(f"Temperatura máxima: {temperatura_maxima}°C")
    print(f"Temperatura mínima: {temperatura_minima}°C")

# Módulo de Programación Orientada a Objetos
class RegistroClima:
    """Clase para gestionar registros de temperatura utilizando POO"""
    
    def __init__(self, ciudad):
        "Constructor de la clase"
        self.ciudad = ciudad
        self._temperaturas = []  # Atributo privado
        self._dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    def ingresar_temperaturas(self):
        "Método para ingresar temperaturas"
        print(f"\n--- Registro de Temperaturas para {self.ciudad} (POO) ---")
        for dia in self._dias:
            while True:
                try:
                    temperatura = float(input(f"Ingrese la temperatura para {dia}: "))
                    self._temperaturas.append(temperatura)
                    break
                except ValueError:
                    print("Error: Ingrese un valor numérico válido.")
    
    def calcular_promedio(self):
        "Calcula el promedio de temperaturas"
        if not self._temperaturas:
            return 0
        return sum(self._temperaturas) / len(self._temperaturas)
    
    def obtener_estadisticas(self):
        "Método que devuelve estadísticas de temperatura"
        if not self._temperaturas:
            return None
        
        return {
            'promedio': self.calcular_promedio(),
            'maxima': max(self._temperaturas),
            'minima': min(self._temperaturas),
            'temperaturas': self._temperaturas
        }
    
    def mostrar_resultados(self):
        "Muestra los resultados del análisis de temperatura"
        estadisticas = self.obtener_estadisticas()
        
        print(f"\n--- Resultados para {self.ciudad} (POO) ---")
        print(f"Temperaturas registradas: {estadisticas['temperaturas']}")
        print(f"Promedio semanal: {estadisticas['promedio']:.2f}°C")
        print(f"Temperatura máxima: {estadisticas['maxima']}°C")
        print(f"Temperatura mínima: {estadisticas['minima']}°C")

# Clase derivada demostrando herencia y polimorfismo
class RegistroClimaDetallado(RegistroClima):
    "Clase extendida que añade más funcionalidades"
    
    def __init__(self, ciudad, region):
        """Constructor extendido"""
        super().__init__(ciudad)
        self.region = region
    
    def mostrar_resultados(self):
        "Sobrescribe el método para incluir información de región"
        estadisticas = self.obtener_estadisticas()
        
        print(f"\n--- Informe Detallado de {self.ciudad}, {self.region} ---")
        print(f"Temperaturas registradas: {estadisticas['temperaturas']}")
        print(f"Promedio semanal: {estadisticas['promedio']:.2f}°C")
        print(f"Temperatura máxima: {estadisticas['maxima']}°C")
        print(f"Temperatura mínima: {estadisticas['minima']}°C")
        
        # Análisis adicional
        rango_temperaturas = estadisticas['maxima'] - estadisticas['minima']
        print(f"Rango de temperaturas: {rango_temperaturas}°C")

# Función principal para demostrar ambos enfoques
def menu_principal():
    "Menú principal para seleccionar el método de análisis"
    while True:
        print("\n--- Sistema de Análisis de Temperaturas ---")
        print("1. Análisis con Programación Tradicional")
        print("2. Análisis con Programación Orientada a Objetos")
        print("3. Análisis Detallado (POO Extendido)")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            # Método Tradicional
            temperaturas = ingresar_temperaturas_tradicional()
            analizar_temperaturas_tradicional(temperaturas)
        
        elif opcion == '2':
            # Método POO Básico
            ciudad = input("Ingrese el nombre de la ciudad: ")
            registro = RegistroClima(ciudad)
            registro.ingresar_temperaturas()
            registro.mostrar_resultados()
        
        elif opcion == '3':
            # Método POO Extendido
            ciudad = input("Ingrese el nombre de la ciudad: ")
            region = input("Ingrese la región: ")
            registro_detallado = RegistroClimaDetallado(ciudad, region)
            registro_detallado.ingresar_temperaturas()
            registro_detallado.mostrar_resultados()
        
        elif opcion == '4':
            print("Gracias por utilizar el Sistema :)")
            break
        
        else:
            print("Opción inválida. Por favor, intente nuevamente.")

# Punto de entrada del programa
if __name__ == "__main__":
    menu_principal()
    