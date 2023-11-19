import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt
import json


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


def calcular_tiempo_caja(tipo_caja):
    DICCIONARIO_DATOS = abrir_json("jumbo/parametros.json")
    cantidad = 30
    DATOS_ATENCION_NORMAL = DICCIONARIO_DATOS["TIEMPO_CAJA_NORMAL"]
    DATOS_ATENCION_RAPIDA = DICCIONARIO_DATOS["TIEMPO_CAJA_RAPIDA"]
    DATOS_ATENCION = {"normal": DATOS_ATENCION_NORMAL, "rapida": DATOS_ATENCION_RAPIDA}

    
    if tipo_caja == "rapida":
        datos_tasa = DATOS_ATENCION["rapida"]
    elif tipo_caja == "normal":
        datos_tasa = DATOS_ATENCION["normal"]
    elif tipo_caja == "compra":
        datos_tasa = DICCIONARIO_DATOS["TIEMPO_COMPRANDO"]

    nombre_distribucion = datos_tasa[0]
    parametros = datos_tasa[1]

    if nombre_distribucion == "lognorm":
        tiempo = sp.lognorm.rvs(*parametros, size=cantidad)

    elif nombre_distribucion == "gamma":
        tiempo = sp.gamma.rvs(*parametros, size=cantidad)

    elif nombre_distribucion == "beta":
        tiempo = sp.beta.rvs(*parametros, size=cantidad)

    elif nombre_distribucion == "expon":
        tiempo = sp.expon.rvs(*parametros, size=cantidad)

    elif nombre_distribucion == "uniform":
        tiempo = sp.uniform.rvs(*parametros, size=cantidad)

    tiempo = tiempo[tiempo >= 0]  # Filtrar valores negativos

    # Graficar los tiempos obtenidos
    plt.hist(tiempo, bins=20, density=True, alpha=0.5, label=f'Tiempos ({tipo_caja})')
    plt.title(f'Distribución de Tiempos para Caja {tipo_caja.capitalize()}')
    plt.xlabel('Tiempo')
    plt.ylabel('Densidad de probabilidad')
    plt.legend()
    plt.show()

# Generar y graficar tiempos para cajas "rapida" y "normal"
calcular_tiempo_caja("rapida")
calcular_tiempo_caja("normal")
calcular_tiempo_caja("compra")
