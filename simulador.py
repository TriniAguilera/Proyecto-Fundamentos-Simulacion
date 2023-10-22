import parametros as p
from simulacion import Simulacion
import time
from guardar_datos import guardar_resultados, crear_archivo, cargar_datos
from intervalos import Intervalo
import math


class Simulador:

    def __init__(self):
        self.dict_duracion_replica = {}
        crear_archivo()
        # self.simulacion = Simulacion()
        # self.intervalo = Intervalo()
        self.dict_espera = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}
        self.dict_ocupacion = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}
        self.espera = {}
        self.ocupacion = {}
        self.sd_espera = {}
        self.sd_ocupacion = {}
        self.int_espera_90 = {}
        self.int_ocupacion_90 = {}
        self.int_espera_95 = {}
        self.int_ocupacion_95 = {}
        self.dict_espera_simulacion = {}
        self.dict_ocupacion_simulacion = {}

    def simular_replica(self):

        for replica in range(p.REPLICAS):

            print(f"replica: {replica} --------------- \n ")

            self.simulacion = Simulacion()
            tiempo_inicio = time.time()

            self.simulacion.simular()
            self.sumar_tiempos_espera_cola()
            self.sumar_porcentaje_ocupacion()
            dict_arreglado_espera = self.arreglar_dict(self.simulacion.dict_promedio_tiempo_espera_cola)
            dict_arreglado_ocupacion = self.arreglar_dict(self.simulacion.dict_promedio_ocupacion)
            self.dict_espera_simulacion[replica] = dict_arreglado_espera
            self.dict_ocupacion_simulacion[replica] = dict_arreglado_ocupacion

            tiempo_fin = time.time()
            duracion_replica = tiempo_fin - tiempo_inicio
            self.dict_duracion_replica[replica] = duracion_replica

        self.espera = self.calcular_espera_promedio()
        self.ocupacion = self.calcular_ocupacion_promedio()
        self.sd_espera = self.calcular_sd_espera()
        self.sd_ocupacion = self.calcular_sd_ocupacion()
        guardar_resultados("datos\espera_replicas.json", self.dict_espera_simulacion)
        guardar_resultados("datos\ocupacion_replicas.json", self.dict_ocupacion_simulacion)
        guardar_resultados("datos\dict_tiempo_de_ejecucion.json", self.dict_duracion_replica)
        guardar_resultados("datos\dict_tiempo_promedio_espera_cola.json", self.espera)
        guardar_resultados("datos\dict_porcentaje_ocupacion_cajas.json", self.ocupacion)
        guardar_resultados("datos\sd_espera.json", self.sd_espera)
        guardar_resultados("datos\sd_ocupacion.json", self.sd_ocupacion)

        self.intervalo = Intervalo()
        
        self.int_espera_90 = self.intervalo.calcular_intervalo_espera(90)
        self.error_90_espera = self.intervalo.error_90_espera
        self.int_ocupacion_90 = self.intervalo.calcular_intervalo_ocupacion(90)
        self.error_90_ocupacion = self.intervalo.error_90_ocupacion
        self.int_espera_95 = self.intervalo.calcular_intervalo_espera(95)
        self.error_95_espera = self.intervalo.error_95_espera
        self.int_ocupacion_95 = self.intervalo.calcular_intervalo_ocupacion(95)
        self.error_95_ocupacion = self.intervalo.error_95_ocupacion
        guardar_resultados("datos\int_90_espera.json", self.int_espera_90)
        guardar_resultados("datos\int_95_espera.json", self.int_espera_95)
        guardar_resultados("datos\int_90_ocupacion.json", self.int_ocupacion_90)
        guardar_resultados("datos\int_95_ocupacion.json", self.int_ocupacion_95)
        guardar_resultados("datos\error_90_espera.json", self.error_90_espera)
        guardar_resultados("datos\error_95_espera.json", self.error_95_espera)
        guardar_resultados("datos\error_90_ocupacion.json", self.error_90_ocupacion)
        guardar_resultados("datos\error_95_ocupacion.json", self.error_95_ocupacion)

        print(f"PROMEDIO ESPERA COLA: {self.espera} \n")
        print(f"PROMEDIO OCUPACION: {self.ocupacion} \n")

    def arreglar_dict(self, dic):
        dict_ = {}
        for tipo_caja in dic.keys():
            for nro in dic[tipo_caja].keys():
                valor = dic[tipo_caja][nro]
                dict_[nro] = valor
        
        # dic_normal = dic["normal"]
        # dic_rapida = dic["rapida"]
        
        # dic_normal.update(dic_rapida)

        return dict_
        


        
        
    def sumar_tiempos_espera_cola(self):
        for tipo_caja in self.simulacion.dict_promedio_tiempo_espera_cola.keys():
            for llave in self.simulacion.dict_promedio_ocupacion[tipo_caja].keys():
                self.dict_espera[llave] += self.simulacion.dict_promedio_tiempo_espera_cola[tipo_caja][llave]

    def sumar_porcentaje_ocupacion(self):
        for tipo_caja in self.simulacion.dict_promedio_ocupacion.keys():
            for llave in self.simulacion.dict_promedio_ocupacion[tipo_caja].keys():
                self.dict_ocupacion[llave] += self.simulacion.dict_promedio_ocupacion[tipo_caja][llave]

    def calcular_espera_promedio(self):
        dict_ = {}
        for llave in self.dict_espera.keys():
            dict_[llave] = self.dict_espera[llave] / p.REPLICAS
        return dict_
    
    # def calcular_sd_espera(self):
    #     total = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}
    #     for caja in self.espera.keys():
    #         suma = 0
    #         for replica in self.dict_espera_simulacion.keys():
    #             for tipo_caja in self.dict_espera_simulacion[replica].keys():
    #                 dict_espera = self.dict_espera_simulacion[replica][tipo_caja]
    #                 for caja_2 in dict_espera.keys():
    #                     if caja == caja_2:
    #                         resta = dict_espera[caja_2] - self.espera[caja]
    #                         cubo = resta * resta
    #                         suma += cubo
    #         total[caja] = math.sqrt(suma / (p.REPLICAS - 1))
    #     return total

    def calcular_sd_espera(self):
        total = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}
        for caja in self.espera.keys():
            suma = 0
            for replica in self.dict_espera_simulacion.keys():
                dict_espera = self.dict_espera_simulacion[replica]
                for caja_2 in dict_espera.keys():
                    if caja == caja_2:
                        resta = dict_espera[caja_2] - self.espera[caja]
                        cubo = resta * resta
                        suma += cubo
            total[caja] = math.sqrt(suma / (p.REPLICAS - 1))
        return total
    
    def calcular_ocupacion_promedio(self):
        dict_ = {}
        for llave in self.dict_ocupacion.keys():
            dict_[llave] = self.dict_ocupacion[llave] / p.REPLICAS
        return dict_
    
    # def calcular_sd_ocupacion(self):
    #     total = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}
    #     for caja in self.ocupacion.keys():
    #         suma = 0
    #         for replica in self.dict_ocupacion_simulacion.keys():
    #             for tipo_caja in self.dict_ocupacion_simulacion[replica].keys():
    #                 dict_ocupacion = self.dict_ocupacion_simulacion[replica][tipo_caja]
    #                 for caja_2 in dict_ocupacion.keys():
    #                     if caja == caja_2:
    #                         resta = dict_ocupacion[caja_2] - self.ocupacion[caja]
    #                         cubo = resta * resta
    #                         suma += cubo
    #         total[caja] = math.sqrt(suma / (p.REPLICAS - 1))
    #     return total
    
    def calcular_sd_ocupacion(self):
        total = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}
        for caja in self.ocupacion.keys():
            suma = 0
            for replica in self.dict_ocupacion_simulacion.keys():
                dict_ocupacion = self.dict_ocupacion_simulacion[replica]
                for caja_2 in dict_ocupacion.keys():
                    if caja == caja_2:
                        resta = dict_ocupacion[caja_2] - self.ocupacion[caja]
                        cubo = resta * resta
                        suma += cubo
            total[caja] = math.sqrt(suma / (p.REPLICAS - 1))
        return total
