# Sistema de Gestión de Empleados

# Clase base: Empleado
class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre  # Atributo público
        self.__salario = salario  # Atributo privado (Encapsulación)

    # Método para acceder al salario 
    def get_salario(self):
        return self.__salario

    # Método para modificar el salario 
    def set_salario(self, salario):
        if salario > 0:
            self.__salario = salario
        else:
            print("El salario debe ser positivo.")

    def descripcion(self):
        return f"Empleado: {self.nombre}, Salario: {self.__salario}"


# Clase derivada: Gerente 
class Gerente(Empleado):
    def __init__(self, nombre, salario, departamento):
        super().__init__(nombre, salario)  # Llamada al constructor de la clase base
        self.departamento = departamento  # Atributo específico de Gerente

    # Sobrescritura de método (Polimorfismo)
    def descripcion(self):
        return f"Gerente: {self.nombre}, Departamento: {self.departamento}, Salario: {self.get_salario()}"


# Clase derivada: Tecnico (hereda de Empleado)
class Tecnico(Empleado):
    def __init__(self, nombre, salario, especialidad):
        super().__init__(nombre, salario)  # Llamada al constructor de la clase base
        self.especialidad = especialidad  # Atributo específico de Tecnico

    # Sobrescritura de método (Polimorfismo)
    def descripcion(self):
        return f"Técnico: {self.nombre}, Especialidad: {self.especialidad}, Salario: {self.get_salario()}"


# Crear instancias de las clases
empleado1 = Empleado("David Ortiz", 25000)
gerente1 = Gerente("Keyla Cedillo", 45000, "Marketing")
tecnico1 = Tecnico("Juan Ramirez", 30000, "Soporte Técnico")

# Uso de encapsulación
print("\nSalario original del técnico:", tecnico1.get_salario())
tecnico1.set_salario(38000)
print("Salario modificado del técnico:", tecnico1.get_salario())

# Demostración de polimorfismo
print("\nDescripciones de empleados:")
print(empleado1.descripcion())
print(gerente1.descripcion())
print(tecnico1.descripcion())

