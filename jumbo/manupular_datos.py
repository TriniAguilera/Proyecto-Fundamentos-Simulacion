import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import json
import numpy as np
from scipy.optimize import curve_fit
from datetime import datetime, time

class Datos:

    def __init__(self, archivo_excel_path):
        self.archivo_excel_path = archivo_excel_path
        self.diccionario_hojas = {}
        self.diccionario_hojas_llegadas_tasas = {}

    def cargar_datos(self, nombre_hoja, nombre_columna_1=None, nombre_columna_2=None, nombre_columna_3=None, nombre_columna_4=None, nombre_columna_5=None, nombre_columna_6=None, nombre_columna_7=None):
        try:
            df = pd.read_excel(self.archivo_excel_path, sheet_name=nombre_hoja)

            if nombre_columna_2 == None:
                lista_datos = df[nombre_columna_1].tolist()
                print(f"lista {nombre_hoja}:", lista_datos , "\n")
                lista_datos_date = [datetime.strptime(tiempo, '%H:%M:%S').time() for tiempo in lista_datos]
                lista_datos = lista_datos_date
                lista_segundos = [(t.second) / 60 + t.minute + t.hour * 60 for t in lista_datos]
                self.diccionario_hojas[nombre_hoja] = lista_segundos

            else:
                print("creando archivo llegadas", nombre_hoja)
                lista_datos_1 = df[nombre_columna_1].tolist()
                lista_datos_2 = df[nombre_columna_2].tolist()
                lista_datos_3 = df[nombre_columna_3].tolist()
                lista_datos_4 = df[nombre_columna_4].tolist()
                lista_datos_5 = df[nombre_columna_5].tolist()
                lista_datos_6 = df[nombre_columna_6].tolist()
                lista_datos_7 = df[nombre_columna_7].tolist()

                for posicion in range(len(lista_datos_1)):
                    hora_inicio = lista_datos_1[posicion]
                    cantidad = lista_datos_4[posicion]
                    self.diccionario_hojas_llegadas_tasas[hora_inicio] = cantidad * 2 / 60 

        except Exception as e:
            print(f"Error al procesar el archivo Excel: {e}")

    def calcular_tasa_distribucion(self, nombre_hoja):

        if nombre_hoja == "TIEMPO_CAJA_NORMAL" or nombre_hoja == "TIEMPO_CAJA_RAPIDA" or nombre_hoja == "TIEMPO_COMPRANDO":
            datos = self.diccionario_hojas[nombre_hoja]

            distribuciones = ['lognorm', 'expon']
            # distribuciones = ['lognorm', 'expon', 'uniform', 'norm', 'beta', 'gamma', 'chi2', 'cauchy', 't', 'laplace', 'cosine']

            resultados = []

            for dist_name in distribuciones:
                dist = getattr(stats, dist_name)
                params = dist.fit(datos)
                log_likelihood = dist.logpdf(datos, *params).sum()
                k = len(params)
                n = len(datos)
                aic = 2 * k - 2 * log_likelihood
                resultados.append({'DISTRIBUCION': dist_name,
                          'PARAMETROS': params, 'AIC': aic})
                
            resultados = sorted(resultados, key=lambda x: x['AIC'])
            self.diccionario_hojas[nombre_hoja] = (resultados[0]['DISTRIBUCION'], resultados[0]['PARAMETROS'])

    def crear_json(self, nombre_archivo, diccionario):
        
        with open(nombre_archivo, 'w') as archivo:
            json.dump(diccionario, archivo)

    def curva(self):
        
        datos = self.diccionario_hojas_llegadas_tasas
        print(datos)

        # Convertir el diccionario a listas de intervalos y llegadas
        intervalos = np.array(list(datos.keys()))
        llegadas = np.array(list(datos.values()))

        # Definir una función cuadrática que modele la tasa de llegadas en función del tiempo
        def tasa_llegadas(t, a, b, c):
            return a * t**2 + b * t + c

        # Ajustar la función a los datos
        params, covariance = curve_fit(tasa_llegadas, intervalos, llegadas)

        # Generar puntos para la curva ajustada
        x = np.linspace(min(intervalos), max(intervalos), 1000)
        y_pred = tasa_llegadas(x, *params)

        # Visualizar los datos y la curva ajustada
        plt.bar(intervalos, llegadas, label='Datos observados', alpha=0.7)
        plt.plot(x, y_pred, 'r--', label='Curva ajustada')
        plt.xlabel('Intervalos de Tiempo [Hora]')
        plt.ylabel('Llegadas [personas/minuto]')
        plt.legend()
        plt.show()

        print("Parámetros de la función ajustada (a * t^2 + b * t + c):", params)
        datos_lambda_t = {"a": params[0], "b": params[1], "c": params[2]}
        self.crear_json("jumbo\lambda_t.json", datos_lambda_t)

datos = Datos('jumbo/Datos_jumbo.xlsx')
tasas = Datos("jumbo/Llegadas.xlsx")

datos.cargar_datos("TIEMPO_CAJA_NORMAL", "TIEMPO")
datos.cargar_datos("TIEMPO_CAJA_RAPIDA", "TIEMPO")
datos.cargar_datos("TIEMPO_COMPRANDO", "TIEMPO")
tasas.cargar_datos("LLEGADA_SUPERMERCADO", "INICIO", "FIN", "TASA", "CANTIDAD_30_MINUTOS", "CANT_HORA", "HORA_INICIO", "HORA_FIN")

datos.calcular_tasa_distribucion("TIEMPO_CAJA_NORMAL")
datos.calcular_tasa_distribucion("TIEMPO_CAJA_RAPIDA")
datos.calcular_tasa_distribucion("TIEMPO_COMPRANDO")

datos.crear_json("jumbo\parametros.json", datos.diccionario_hojas)

tasas.curva()
