import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime

# Definir una semilla
semilla = 4
np.random.seed(semilla)



def compra(max, min, tamano):
    # Parámetros de la distribución log-normal
    media_log = np.log((max + min) / 2)  # media en la escala logarítmica
    desviacion_log = (np.log(max) - np.log(min)) / (2 * 1.96)  # desviación estándar en la escala logarítmica
    # Generar una muestra de tamaño 1000
    tamanio_muestra = tamano
    muestra_log_normal = np.random.lognormal(mean=media_log, sigma=desviacion_log, size=tamanio_muestra)
    muestra_en_minutos = muestra_log_normal
    # Graficar un histograma de la muestra
    plt.hist(muestra_en_minutos, bins=30, density=True, alpha=0.5, color='blue', label='Muestra log-normal')
    plt.title('Muestra de una distribución log-normal Compra')
    plt.xlabel('Tiempo (minutos)')
    plt.ylabel('Densidad de probabilidad')
    plt.legend()
    plt.show()
    return muestra_en_minutos

def atencion_normal(max, min, tamano):
    # Parámetros de la distribución log-normal
    media_log = np.log((max + min) / 2)  # media en la escala logarítmica
    desviacion_log = (np.log(max) - np.log(min)) / (2 * 1.96)  # desviación estándar en la escala logarítmica
    # Generar una muestra de tamaño 1000
    tamanio_muestra = tamano
    muestra_log_normal = np.random.lognormal(mean=media_log, sigma=desviacion_log, size=tamanio_muestra)
    muestra_en_minutos = muestra_log_normal
    # Graficar un histograma de la muestra
    plt.hist(muestra_en_minutos, bins=30, density=True, alpha=0.5, color='blue', label='Muestra log-normal')
    plt.title('Muestra de una distribución log-normal Atención Normal')
    plt.xlabel('Tiempo (minutos)')
    plt.ylabel('Densidad de probabilidad')
    plt.legend()
    plt.show()
    return muestra_en_minutos

def atencion_rapida(media, tamano):
    # Parámetros
    tasa = 1 / media  # Tasa de la distribución exponencial (inversa de la media)
    tamaño_muestra = tamano  # Tamaño de la muestra
    # Generar muestra
    muestra_exponencial = np.random.exponential(scale=1/tasa, size=tamaño_muestra)
    # Visualizar la distribución
    plt.hist(muestra_exponencial, bins=30, density=True, alpha=0.5, color='green')
    plt.title('Distribución Exponencial Atención Rápida')
    plt.xlabel('Valor')
    plt.ylabel('Densidad de Probabilidad')
    plt.show()
    return muestra_exponencial

# Datos de tiempos de demora
tiempos_demora_compra = compra(max=50, min=20, tamano=100)
tiempos_atencion_normal = atencion_rapida(media=3, tamano=100)
tiempos_atencion_rapida = atencion_rapida(media=2, tamano=100)

def crear_hojas(datos_compra, datos_normal, datos_rapida):
    # Convertir los tiempos de demora a formato de hora:minuto:segundo
    datos_formateados_1 = pd.to_datetime(datos_compra, unit='m').strftime('%H:%M:%S')
    # Crear un DataFrame con los datos formateados
    df_1 = pd.DataFrame({'TIEMPO': datos_formateados_1})

    # Convertir los tiempos de demora a formato de hora:minuto:segundo
    datos_formateados_2 = pd.to_datetime(datos_normal, unit='m').strftime('%H:%M:%S')
    # Crear un DataFrame con los datos formateados
    df_2 = pd.DataFrame({'TIEMPO': datos_formateados_2})

    # Convertir los tiempos de demora a formato de hora:minuto:segundo
    datos_formateados_3 = pd.to_datetime(datos_rapida, unit='m').strftime('%H:%M:%S')
    # Crear un DataFrame con los datos formateados
    df_3 = pd.DataFrame({'TIEMPO': datos_formateados_3})

    # Guardar el DataFrame en un archivo Excel en la hoja "tiempo_compra"
    archivo_excel_path = 'jumbo/Datos_jumbo.xlsx'
    with pd.ExcelWriter(archivo_excel_path, engine='openpyxl', mode='w') as writer:
        df_1.to_excel(writer, sheet_name="TIEMPO_COMPRANDO", index=False)
        df_2.to_excel(writer, sheet_name="TIEMPO_CAJA_NORMAL", index=False)
        df_3.to_excel(writer, sheet_name="TIEMPO_CAJA_RAPIDA", index=False)

crear_hojas(tiempos_demora_compra, tiempos_atencion_normal, tiempos_atencion_rapida)

