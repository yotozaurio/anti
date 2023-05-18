import os
import pwd
import time

# Extensiones sospechosas
extensiones_sospechosas = ['.genx', '.foo']

# Propietario y grupo autorizados
propietario_autorizado = 'recerca'
grupo_autorizado = 'gruprecerca'

# Ruta del directorio a analizar
directorio_raiz = 'DIR_INIT'

def obtener_propietario_grupo(ruta):
    informacion = os.stat(ruta)
    uid = informacion.st_uid
    gid = informacion.st_gid
    propietario = pwd.getpwuid(uid).pw_name
    grupo = pwd.getpwuid(gid).pw_name
    return propietario, grupo

def analisis_rapido():
    # Variables para el informe
    fecha_analisis = time.strftime('%Y-%m-%d %H:%M:%S')
    inicio_analisis = time.time()
    archivos_extension_sospechosa = {}
    archivos_propietario_erroneo = 0
    
    # Recorrer los archivos del directorio raíz y subdirectorios
    for root, dirs, files in os.walk(directorio_raiz):
        for file in files:
            ruta_completa = os.path.join(root, file)
            extension = os.path.splitext(file)[1]
            
            # Verificar extensiones sospechosas
            if extension in extensiones_sospechosas:
                if extension in archivos_extension_sospechosa:
                    archivos_extension_sospechosa[extension] += 1
                else:
                    archivos_extension_sospechosa[extension] = 1
            
            # Verificar propietario y grupo
            propietario, grupo = obtener_propietario_grupo(ruta_completa)
            if propietario != propietario_autorizado or grupo != grupo_autorizado:
                archivos_propietario_erroneo += 1
    
    # Generar el informe
    duracion_analisis = time.time() - inicio_analisis
    informe = f'{fecha_analisis}_fast.log'
    
    with open(informe, 'w') as archivo:
        archivo.write('Fecha del análisis: ' + fecha_analisis + '\n')
        archivo.write('Duración del análisis: ' + time.strftime('%H:%M:%S', time.gmtime(duracion_analisis)) + '\n')
        archivo.write('\n')
        archivo.write('Extensiones sospechosas encontradas:\n')
        for extension, cantidad in archivos_extension_sospechosa.items():
            archivo.write(extension + ': ' + str(cantidad) + '\n')
        archivo.write('\n')
        archivo.write('Cantidad de archivos con propietario o grupos erróneos: ' + str(archivos_propietario_erroneo) + '\n')
        archivo.write('\n')
        archivo.write('Nombre,Ruta,Tamaño,Propietario,Grupo,Extensión\n')
        
        # Agregar información de cada archivo al cuerpo del informe
        for root, dirs, files in os.walk(directorio_raiz):
            for file in files:
                ruta_completa = os.path.join(root, file)
                tamano = os.path.getsize(ruta_completa)
                propietario, grupo = obtener_propietario_grupo(ruta_completa)
                extension = os.path.splitext(file)[1]
                
                archivo.write(file + ',' + ruta_completa + ',' + str(tamano) + ',' + propietario + ',' + grupo + ',' + extension + '\n')
    
    print('Análisis rápido completado.')
    print('Informe generado:', informe)
    print('Duración del análisis:', time.strftime('%H:%M:%S', time.gmtime(duracion_analisis)))

# Ejecutar el análisis rápido
analisis_rapido()