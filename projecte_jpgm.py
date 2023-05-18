import os

# -------------------------------#
# Paso - 1: Configuración inicial#
# -------------------------------#

configuracion = {
    "DIR_INIT": "DIR_INIT",
    "DIR_LOGS": "DIR_LOGS",
    "DIR_QUARANTENA": "DIR_QUARANTENA",
    "LOGS_EXTRA_CONTENT_EXTENSION": "LOGS_EXTRA_CONTENT_EXTENSION",
    "ZIP_FILE": "ZIP_FILE",
}

# Función para mostrar la configuración actual
def mostrar_configuracion(configuracion):
    print("Configuración actual:")
    for parametro, valor in configuracion.items():
        print(f"{parametro}: {valor}")

# Función para cargar la configuración desde un archivo
def cargar_configuracion():
    nombre_archivo = input("Introduce el nombre del archivo de configuración: ")
    try:
        with open(nombre_archivo, "r") as archivo:
            lineas = archivo.readlines()
            configuracion = {}
            for linea in lineas:
                parametro, valor = linea.strip().split("=")
                configuracion[parametro] = valor
            print("Configuración cargada correctamente.")
            return configuracion
    except FileNotFoundError:
        print("El archivo no existe.")
    except IOError:
        print("No se puede abrir el archivo.")
    return None

# Función para cambiar un parámetro de configuración
def cambiar_parametro(configuracion):
    parametro = input("Introduce el nombre del parámetro que deseas cambiar: ")
    if parametro not in configuracion:
        print("El parámetro no existe.")
        return
    nuevo_valor = input("Introduce el nuevo valor para el parámetro: ")
    configuracion[parametro] = nuevo_valor
    print("Parámetro actualizado correctamente.")

# Función para guardar la configuración en un archivo
def guardar_configuracion(configuracion):
    nombre_archivo = input("Introduce el nombre del archivo de configuración a crear (por defecto: config.cfg): ")
    if nombre_archivo == "":
        nombre_archivo = "config.cfg"  # Nombre por defecto

    # Verificar si el archivo ya existe
    if os.path.exists(nombre_archivo):
        sobreescribir = input("El archivo ya existe. ¿Deseas sobreescribirlo? (s/n): ")
        if sobreescribir.lower() != "s":
            print("No se realizará la operación.")
            return

    try:
        with open(nombre_archivo, "w") as archivo:
            for parametro, valor in configuracion.items():
                archivo.write(f"{parametro}={valor}\n")
        print("Configuración guardada correctamente.")
    except IOError:
        print("No se puede guardar la configuración en el archivo.")

# Menú principal
while True:
    print("------ MENÚ PRINCIPAL ------")
    print("1. Opciones de configuración")
    print("2. Analisis Rápido")
    print("3. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        # Menú de configuración
        while True:
            print("------ MENÚ DE CONFIGURACIÓN ------")
            print("1. Ver config")
            print("2. Cargar config")
            print("3. Cambiar parámetros")
            print("4. Guardar config")
            print("5. Volver al menú principal")
            opcion_configuracion = input("Seleccione una opción: ")

            if opcion_configuracion == "1":
                mostrar_configuracion(configuracion)
            elif opcion_configuracion == "2":
                nueva_configuracion = cargar_configuracion()
                if nueva_configuracion is not None:
                    configuracion = nueva_configuracion
            elif opcion_configuracion == "3":
                cambiar_parametro(configuracion)
            elif opcion_configuracion == "4":
                guardar_configuracion(configuracion)
            elif opcion_configuracion == "5":
                break
            else:
                print("Opción inválida. Intente de nuevo.")
    

    elif opcion == "2":
        
        pass

    elif opcion == "3":
        break
    else:
        print("Opción inválida. Intente de nuevo.")