import os
import subprocess
from datetime import datetime

# Función para mostrar el contenido de un archivo .py
def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None

# Función para ejecutar un script .py en otra terminal
def ejecutar_codigo(ruta_script):
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Linux o macOS
            subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")

# Función para buscar scripts por nombre dentro de todas las subcarpetas
def buscar_script(nombre, ruta_base):
    print(f"\n🔎 Buscando scripts que contengan: '{nombre}' ...\n")
    for root, dirs, files in os.walk(ruta_base):
        for file in files:
            if nombre.lower() in file.lower() and file.endswith('.py'):
                ruta_script = os.path.join(root, file)
                print(f"\n✅ Script encontrado: {ruta_script}")
                codigo = mostrar_codigo(ruta_script)
                if codigo:
                    ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ")
                    if ejecutar == '1':
                        ejecutar_codigo(ruta_script)
                    registrar_historial(ruta_script)
                    return
    print("❌ No se encontró ningún script con ese nombre.")

# Función para registrar el historial de scripts ejecutados
def registrar_historial(ruta_script):
    with open("historial_uso.txt", "a") as log:
        log.write(f"{ruta_script} - abierto el {datetime.now()}\n")

# Menú principal para navegar entre unidades o buscar
def mostrar_menu():
    ruta_base = os.path.dirname(__file__)  # Carpeta donde está el Dashboard

    # Detectar carpetas automáticamente como unidades
    unidades = {str(i + 1): carpeta.name for i, carpeta in enumerate(os.scandir(ruta_base)) if carpeta.is_dir()}

    while True:
        print("\n" + "=" * 45)
        print("📘 GESTOR DE PROYECTOS - PROGRAMACIÓN ORIENTADA A OBJETOS")
        print("=" * 45)
        for key in unidades:
            print(f"{key} - {unidades[key]}")
        print("B - Buscar script por nombre")
        print("0 - Salir")

        eleccion = input("\nElige una opción: ")
        if eleccion == '0':
            print("👋 Saliendo del programa.")
            break
        elif eleccion.upper() == 'B':
            nombre = input("🔍 Ingresa parte del nombre del script a buscar: ")
            buscar_script(nombre, ruta_base)
        elif eleccion in unidades:
            ruta_unidad = os.path.join(ruta_base, unidades[eleccion])
            mostrar_sub_menu(ruta_unidad)
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

# Menú para seleccionar subcarpetas dentro de una unidad
def mostrar_sub_menu(ruta_unidad):
    if not os.path.exists(ruta_unidad):
        print("❌ La unidad seleccionada no existe.")
        return

    sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]

    while True:
        print("\n📁 Submenú - Selecciona una subcarpeta")
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar al menú principal")

        eleccion = input("Elige una subcarpeta: ")
        if eleccion == '0':
            break
        try:
            indice = int(eleccion) - 1
            if 0 <= indice < len(sub_carpetas):
                ruta_sub = os.path.join(ruta_unidad, sub_carpetas[indice])
                mostrar_scripts(ruta_sub)
            else:
                print("❌ Opción fuera de rango.")
        except ValueError:
            print("❌ Entrada inválida.")

# Menú para listar y ejecutar scripts .py dentro de una subcarpeta
def mostrar_scripts(ruta_sub_carpeta):
    scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]

    while True:
        print("\n📄 Scripts disponibles:")
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Regresar")
        print("9 - Menú principal")

        eleccion = input("Selecciona un script: ")
        if eleccion == '0':
            break
        elif eleccion == '9':
            return
        try:
            indice = int(eleccion) - 1
            if 0 <= indice < len(scripts):
                ruta_script = os.path.join(ruta_sub_carpeta, scripts[indice])
                codigo = mostrar_codigo(ruta_script)
                if codigo:
                    ejecutar = input("¿Deseas ejecutar este script? (1: Sí, 0: No): ")
                    if ejecutar == '1':
                        ejecutar_codigo(ruta_script)
                    registrar_historial(ruta_script)
                    input("\nPresiona Enter para continuar...")
            else:
                print("❌ Opción fuera de rango.")
        except ValueError:
            print("❌ Entrada inválida.")

# Ejecutar el dashboard si se corre directamente el archivo
if __name__ == "__main__":
    mostrar_menu()
