# Sistema de Mascotas de Juegos Online
# Demuestra conceptos de POO con mascotas que tienen diferentes comportamientos y necesidades
# - Abstracción: Comportamiento de los animales
# - Encapsulación: Su estdo
# - Herencia: Diferentes tipos de animales
# - Polimorfismo: Sus comportamientos

class Mascota:
    """Clase base para todas las mascotas"""
    def __init__(self, nombre, edad):
        self._nombre = nombre
        self._edad = edad
        self._energia = 80
        self._hambre = 5
        self._felicidad = 99
    
    def estado(self):
        print(f"\n{self._nombre}:")
        print(f"·Energía: {self._energia}")
        print(f"·Hambre: {self._hambre}")
        print(f"·Felicidad: {self._felicidad}")
    
    def alimentar(self):
        self._hambre = max(0, self._hambre - 20)
        self._felicidad += 10
        print(f"{self._nombre} ha sido alimentado")
    
    def jugar(self):
        if self._energia >= 20:
            self._energia -= 20
            self._hambre += 15
            self._felicidad += 10
            print(f"{self._nombre} está jugando felizmente")
        else:
            print(f"{self._nombre} está muy cansado para jugar")

class Perro(Mascota):
    def __init__(self, nombre, edad, raza):
        super().__init__(nombre, edad)
        self.raza = raza
        self._lealtad = 50
    
    def pasear(self):
        self._energia -= 20
        self._hambre += 10
        self._lealtad += 20
        print(f"{self._nombre} disfruta del paseo")
    
    def estado(self):
        super().estado()
        print(f"·Lealtad: {self._lealtad}")

class Gato(Mascota):
    def __init__(self, nombre, edad, color):
        super().__init__(nombre, edad)
        self.color = color
        self._independencia = 80
    
    def dormir(self):
        self._energia = min(100, self._energia + 40)
        self._hambre += 5
        print(f"{self._nombre} está durmiendo comodamente")
    
    def estado(self):
        super().estado()
        print(f"·Independencia: {self._independencia}")

# Ejemplo 
def main():
    perro = Perro("Firulais", 3, "Husky siberiano")
    gato = Gato("Haru", 2, "Siamés")
    
    print("=== Estado Inicial ===")
    perro.estado()
    gato.estado()
    
    print("\n=== Interacciones ===")
    perro.pasear()
    perro.alimentar()
    gato.dormir()
    gato.jugar()
    
    print("\n=== Estado Final ===")
    perro.estado()
    gato.estado()

if __name__ == "__main__":
    main()