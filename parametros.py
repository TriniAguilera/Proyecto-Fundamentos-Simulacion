import json

# no tocar ------

def abrir_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            datos = json.load(archivo)
        return datos
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar el JSON en '{nombre_archivo}'.")
        return None

DICCIONARIO_DATOS = abrir_json("jumbo/parametros.json")


TASA_COMPRA = DICCIONARIO_DATOS["TIEMPO_COMPRANDO"]
TASA_ATENCION = DICCIONARIO_DATOS["TIEMPO_CAJA_NORMAL"]
TASA_ATENCION_RAPIDA = DICCIONARIO_DATOS["TIEMPO_CAJA_RAPIDA"]

CANTIDAD_CAJAS_NORMALES = 33 # NUEVO PARAMETRO
CANTIDAD_CAJAS_RAPIDAS = 12 # NUEVO PARAMETRO

MINUTOS_POR_HORA = 60

# PROBABILIDAD_CAJA = XXXX # NUEVO PARAMETRO

# ---------------

# tocar ------------

JORNADA = 10
TASA_LLEGADAS = 1/3 
REPLICAS = 10
INFINITO = 1000000000

LISTA_PATH = ["datos\diccionario_datos_tiempo_promedio_espera_cola.json",
              "datos\diccionario_datos_porcentaje_ocupacion_cajas.json",
              "datos\diccionario_tiempo_de_ejecucion.json",
              "datos\dict_tiempo_promedio_espera_cola.json",
              "datos\dict_porcentaje_ocupacion_cajas.json"]

# ------------------


# parametros que desapareceran en la entrega final

CANTIDAD_DE_CAJAS = 16

# -----------------------------------------------