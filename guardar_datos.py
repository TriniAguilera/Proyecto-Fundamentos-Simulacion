import parametros as ps
import json

def crear_archivo():
    for path in ps.LISTA_PATH:
        with open(path, "w") as archivo:
            datos_vacios = {}
            json.dump(datos_vacios, archivo, indent=4)

def cargar_datos(path):
    with open(path, "r") as archivo:
        diccionario = json.load(archivo)
    return diccionario
        
def guardar_resultados(path, texto):
    #print("SIMULADOR guardando resultados")
    
    contenido = cargar_datos(path)
    contenido.update(texto)

    with open(path, "w") as archivo:
        json.dump(contenido, archivo, indent=4)
