import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import json

# AL CORRER ESTE ARCHIVO SE ACTUALIZARAN LOS DATOS DE LA CARPETA 
# JUMBO QUE POSTERIORMENTE SE UTILIZAN EL LOS PARAMETROS DE LA SIMULACION

class Datos:

    def __init__(self, archivo_excel_path):
        self.archivo_excel_path = archivo_excel_path
        self.diccionario_hojas = {}
        self.diccionario_hojas_llegadas = {}
        

    def cargar_datos(self, nombre_hoja, nombre_columna_1=None, nombre_columna_2=None, nombre_columna_3=None, nombre_columna_4=None, nombre_columna_5=None, nombre_columna_6=None):
        try:
            df = pd.read_excel(self.archivo_excel_path, sheet_name=nombre_hoja)

            if nombre_columna_2 == None:
                lista_datos = df[nombre_columna_1].tolist()
                lista_segundos = [(t.second) / 60 + t.minute + t.hour * 60 for t in lista_datos]
                self.diccionario_hojas[nombre_hoja] = lista_segundos

            else:
                lista_datos_1 = df[nombre_columna_1].tolist()
                lista_datos_2 = df[nombre_columna_2].tolist()
                lista_datos_3 = df[nombre_columna_3].tolist()
                lista_datos_4 = df[nombre_columna_4].tolist()
                lista_datos_5 = df[nombre_columna_5].tolist()
                lista_datos_6 = df[nombre_columna_6].tolist()

                for posicion in range(len(lista_datos_1)):
                    hora_inicio = lista_datos_1[posicion]
                    tasa = lista_datos_3[posicion]
                    self.diccionario_hojas_llegadas[hora_inicio] = tasa
                # self.crear_json("jumbo/parametros_llegada.json")

        except Exception as e:
            print(f"Error al procesar el archivo Excel: {e}")

    def cacular_tasa_distribucion(self, nombre_hoja):
        
        if nombre_hoja == "TIEMPO_CAJA_NORMAL" or nombre_hoja == "TIEMPO_CAJA_RAPIDA" or nombre_hoja == "TIEMPO_COMPRANDO":
            datos = self.diccionario_hojas[nombre_hoja]
            parametros = scipy.stats.expon.fit(datos, method= "mle")
            escala = parametros[1]
            tasa = 1 / escala
            self.diccionario_hojas[nombre_hoja] = tasa

        elif nombre_hoja == "LLEGADA_SUPERMERCADO":
            pass

    def crear_json(self, nombre_archivo, diccionario):
        
        with open(nombre_archivo, 'w') as archivo:
            json.dump(diccionario, archivo)

    def graficar_tiempos(self, nombre_hoja, nombre_columna):

        lista = self.diccionario_hojas[nombre_hoja][nombre_columna]
        if nombre_hoja == "TIEMPO_CAJA_NORMAL" or nombre_hoja == "TIEMPO_CAJA_RAPIDA" or nombre_hoja == "TIEMPO_COMPRANDO":
            parametros = scipy.stats.expon.fit(lista, method= "mle")
            escala = parametros[1]
            muestra_simulada = scipy.stats.expon.rvs(scale=escala, size=20)

            plt.hist(muestra_simulada, bins=100, color='red')

        plt.hist(lista, bins=100, color='blue')
        plt.show()

datos = Datos('jumbo/Datos_jumbo.xlsx')

datos.cargar_datos("TIEMPO_CAJA_NORMAL", "TIEMPO")
datos.cargar_datos("TIEMPO_CAJA_RAPIDA", "TIEMPO")
datos.cargar_datos("TIEMPO_COMPRANDO", "TIEMPO")
datos.cargar_datos("LLEGADA_SUPERMERCADO", "INICIO", "FIN", "TASA", "CANTIDAD_30_MINUTOS", "HORA_INICIO", "HORA_FIN")

datos.cacular_tasa_distribucion("TIEMPO_CAJA_NORMAL")
datos.cacular_tasa_distribucion("TIEMPO_CAJA_RAPIDA")
datos.cacular_tasa_distribucion("TIEMPO_COMPRANDO")
datos.cacular_tasa_distribucion("LLEGADA_SUPERMERCADO")

datos.crear_json("jumbo\parametros.json", datos.diccionario_hojas)
datos.crear_json("jumbo\parametros_llegada.json", datos.diccionario_hojas_llegadas)

# datos.graficar_tiempos("TIEMPO_CAJA_NORMAL", "TIEMPO")
# datos.graficar_tiempos("TIEMPO_CAJA_RAPIDA", "TIEMPO")
# datos.graficar_tiempos("TIEMPO_COMPRANDO", "TIEMPO")
