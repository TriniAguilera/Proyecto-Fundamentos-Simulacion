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
DICCIONARIO_DATOS_LLEGADAS = abrir_json("jumbo/parametros_llegada.json")

TASA_COMPRA = DICCIONARIO_DATOS["TIEMPO_COMPRANDO"]
TASA_ATENCION_NORMAL = DICCIONARIO_DATOS["TIEMPO_CAJA_NORMAL"]
TASA_ATENCION_RAPIDA = DICCIONARIO_DATOS["TIEMPO_CAJA_RAPIDA"]
TASA_ATENCION = {"normal": TASA_ATENCION_NORMAL, "rapida": TASA_ATENCION_RAPIDA}

CANTIDAD_CAJAS_NORMALES = 33 # NUEVO PARAMETRO
CANTIDAD_CAJAS_RAPIDAS = 12 # NUEVO PARAMETRO
PROBABILIDAD_ELEGIR_CAJA_RAPIDA = (CANTIDAD_CAJAS_RAPIDAS) / (CANTIDAD_CAJAS_NORMALES + CANTIDAD_CAJAS_RAPIDAS)
PROBABILIDAD_ELEGIR_CAJA_NORMAL = 1 - PROBABILIDAD_ELEGIR_CAJA_RAPIDA

MINUTOS_POR_HORA = 60

# ---------------

# tocar ------------

JORNADA = 13
REPLICAS = 30
INFINITO = 9999999999999999999

LISTA_PATH = ["datos\espera_replicas.json",
              "datos\ocupacion_replicas.json",
              "datos\dict_tiempo_de_ejecucion.json",
              "datos\dict_tiempo_promedio_espera_cola.json",
              "datos\dict_porcentaje_ocupacion_cajas.json",
              "datos\sd_espera.json",
              "datos\sd_ocupacion.json",
              "datos\int_90_espera.json",
              "datos\int_90_ocupacion.json",
              "datos\int_95_espera.json",
              "datos\int_95_ocupacion.json",
              "datos\error_90_espera.json",
              "datos\error_95_espera.json",
              "datos\error_90_ocupacion.json",
              "datos\error_95_ocupacion.json"]

# ------------------

# parametros que desapareceran en la entrega final

# CANTIDAD_DE_CAJAS = 16

# -----------------------------------------------