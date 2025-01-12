"""
Calculadora de Geometría
Este programa calcula el área y perímetro de diferentes figuras geométricas:
- Círculo
- Rectángulo
- Triángulo
"""

import math

class FiguraGeometrica:
    "Clase base para figuras geométricas"
    def calcular_area(self):
        pass
    
    def calcular_perimetro(self):
        pass

class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = float(radio)
    
    def calcular_area(self):
        return math.pi * self.radio ** 2
    
    def calcular_perimetro(self):
        return 2 * math.pi * self.radio

class Rectangulo(FiguraGeometrica):
    def __init__(self, base, altura):
        self.base = float(base)
        self.altura = float(altura)
    
    def calcular_area(self):
        return self.base * self.altura
    
    def calcular_perimetro(self):
        return 2 * (self.base + self.altura)

class Triangulo(FiguraGeometrica):
    def __init__(self, base, altura, lado2, lado3):
        self.base = float(base)
        self.altura = float(altura)
        self.lado2 = float(lado2)
        self.lado3 = float(lado3)
    
    def calcular_area(self):
        return (self.base * self.altura) / 2
    
    def calcular_perimetro(self):
        return self.base + self.lado2 + self.lado3

def mostrar_menu():
    "Muestra el menú de opciones"
    print("\nCalculadora de Geometría")
    print("1. Círculo")
    print("2. Rectángulo")
    print("3. Triángulo")
    print("4. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una figura (1-4): ")
        
        if opcion == "4":
            print("¡Hasta luego!")
            break
            
        if opcion == "1":
            radio = float(input("Ingrese el radio del círculo: "))
            figura = Circulo(radio)
        elif opcion == "2":
            base = float(input("Ingrese la base del rectángulo: "))
            altura = float(input("Ingrese la altura del rectángulo: "))
            figura = Rectangulo(base, altura)
        elif opcion == "3":
            base = float(input("Ingrese la base del triángulo: "))
            altura = float(input("Ingrese la altura del triángulo: "))
            lado2 = float(input("Ingrese el segundo lado del triángulo: "))
            lado3 = float(input("Ingrese el tercer lado del triángulo: "))
            figura = Triangulo(base, altura, lado2, lado3)
        else:
            print("Opción no válida")
            continue
        
        # Calcular y mostrar resultados
        area = figura.calcular_area()
        perimetro = figura.calcular_perimetro()
        
        print(f"\nResultados:")
        print(f"Área: {area:.2f}")
        print(f"Perímetro: {perimetro:.2f}")

if __name__ == "__main__":
    main()