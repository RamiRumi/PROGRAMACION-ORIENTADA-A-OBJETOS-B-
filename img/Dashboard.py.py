import os
import subprocess
from colorama import init, Fore, Style

# Inicializar colorama para colores en consola
init()

def mostrar_codigo(ruta_script):
    """Muestra el contenido de un script con resaltado de ruta"""
    try:
        with open(ruta_script, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n{Fore.CYAN}--- Código de {ruta_script} ---{Style.RESET_ALL}\n")
            print(f"{Fore.WHITE}{codigo}{Style.RESET_ALL}")
            return codigo
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Archivo no encontrado.{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}Error al leer archivo: {e}{Style.RESET_ALL}")
        return None

def ejecutar_codigo(ruta_script):
    """Ejecuta el script en una nueva terminal manteniendo la sesión"""
    try:
        ruta_absoluta = os.path.abspath(ruta_script)
        if os.name == 'nt':
            # Windows: Usar comillas para rutas con espacios
            subprocess.Popen(f'start cmd /k "python "{ruta_absoluta}""', shell=True)
        else:
            # Linux/macOS: Usar xterm si está disponible
            subprocess.Popen(['xterm', '-hold', '-e', f'python3 "{ruta_absoluta}"'])
    except Exception as e:
        print(f"{Fore.RED}Error al ejecutar: {e}{Style.RESET_ALL}")

def mostrar_menu_principal():
    """Muestra el menú principal con unidades disponibles"""
    while True:
        print(f"\n{Fore.GREEN}=== MENÚ PRINCIPAL ==={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1 - Unidad 1")
        print(f"{Fore.YELLOW}2 - Unidad 2")
        print(f"{Fore.RED}0 - Salir{Style.RESET_ALL}")
        
        opcion = input(f"{Fore.CYAN}Seleccione una opción: {Style.RESET_ALL}").strip()
        
        if opcion == '0':
            print(f"{Fore.MAGENTA}Saliendo del sistema...{Style.RESET_ALL}")
            break
        elif opcion in {'1', '2'}:
            mostrar_submenus(f"Unidad {opcion}")
        else:
            print(f"{Fore.RED}Opción inválida. Intente nuevamente.{Style.RESET_ALL}")

def mostrar_submenus(ruta_unidad):
    """Muestra submenús jerárquicos para cada unidad"""
    ruta_completa = os.path.join(os.path.dirname(__file__), ruta_unidad)
    
    while True:
        try:
            elementos = next(os.walk(ruta_completa))[1]  # Listar solo directorios
        except StopIteration:
            print(f"{Fore.RED}Unidad no encontrada!{Style.RESET_ALL}")
            return

        print(f"\n{Fore.BLUE}=== {ruta_unidad.upper()} ==={Style.RESET_ALL}")
        for idx, carpeta in enumerate(elementos, 1):
            print(f"{Fore.YELLOW}{idx} - {carpeta}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}0 - Regresar\n{Fore.RED}9 - Menú Principal{Style.RESET_ALL}")
        
        opcion = input(f"{Fore.CYAN}Seleccione subcarpeta: {Style.RESET_ALL}").strip()
        
        if opcion == '0':
            return
        if opcion == '9':
            mostrar_menu_principal()
            return
        if opcion.isdigit() and 0 < int(opcion) <= len(elementos):
            gestionar_scripts(os.path.join(ruta_completa, elementos[int(opcion)-1]))
        else:
            print(f"{Fore.RED}Opción inválida!{Style.RESET_ALL}")

def gestionar_scripts(ruta_carpeta):
    """Gestiona la selección y ejecución de scripts"""
    while True:
        try:
            scripts = [f for f in os.listdir(ruta_carpeta) if f.endswith('.py')]
        except FileNotFoundError:
            print(f"{Fore.RED}Carpeta no encontrada!{Style.RESET_ALL}")
            return

        print(f"\n{Fore.BLUE}=== SCRIPTS DISPONIBLES ==={Style.RESET_ALL}")
        for idx, script in enumerate(scripts, 1):
            print(f"{Fore.YELLOW}{idx} - {script}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}0 - Regresar\n{Fore.RED}9 - Menú Principal{Style.RESET_ALL}")
        
        opcion = input(f"{Fore.CYAN}Seleccione script: {Style.RESET_ALL}").strip()
        
        if opcion == '0':
            return
        if opcion == '9':
            mostrar_menu_principal()
            return
        if opcion.isdigit() and 0 < int(opcion) <= len(scripts):
            script_path = os.path.join(ruta_carpeta, scripts[int(opcion)-1])
            if mostrar_codigo(script_path):
                if input(f"{Fore.CYAN}¿Ejecutar script? (s/n): {Style.RESET_ALL}").lower() == 's':
                    ejecutar_codigo(script_path)
        else:
            print(f"{Fore.RED}Opción inválida!{Style.RESET_ALL}")

if __name__ == "__main__":
    mostrar_menu_principal()
    