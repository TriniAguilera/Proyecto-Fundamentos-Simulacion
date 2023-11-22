import parametros as p
from simulacion import Simulacion
import time
from guardar_datos import guardar_resultados, crear_archivo, cargar_datos
import math
from intervalos import Intervalo

class Simulador:

    def __init__(self):
        self.dict_duracion_replica = {}
        crear_archivo()
        self.dict_espera = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}
        self.dict_ocupacion = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}
        self.espera = {}
        self.ocupacion = {}
        self.sd_espera = {}
        self.sd_ocupacion = {}
        self.dict_espera_simulacion = {}
        self.dict_ocupacion_simulacion = {}
        self.intervalo = None

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
            self.dict_espera_simulacion[replica] = sum(list(dict_arreglado_espera.values())) / (p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)
            self.dict_ocupacion_simulacion[replica] = sum(list(dict_arreglado_ocupacion.values())) / (p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)

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

        self.int_espera_95 = self.intervalo.calcular_intervalo_espera(95)
        self.error_95_espera = self.intervalo.error_95_espera
        self.int_ocupacion_95 = self.intervalo.calcular_intervalo_ocupacion(95)
        self.error_95_ocupacion = self.intervalo.error_95_ocupacion
        
        guardar_resultados("datos\int_95_espera.json", self.int_espera_95)
        guardar_resultados("datos\int_95_ocupacion.json", self.int_ocupacion_95)
        guardar_resultados("datos\error_95_espera.json", self.error_95_espera)
        guardar_resultados("datos\error_95_ocupacion.json", self.error_95_ocupacion)

    def arreglar_dict(self, dic):
        dict_ = {}
        for tipo_caja in dic.keys():
            for nro in dic[tipo_caja].keys():
                valor = dic[tipo_caja][nro]
                dict_[nro] = valor
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
        suma = 0
        for llave in self.dict_espera.keys():
            dict_[llave] = self.dict_espera[llave] / p.REPLICAS
            suma += self.dict_espera[llave]
        total_1 = suma / (p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)
        total = total_1 / p.REPLICAS
        return {"espera promedio": total}

    def calcular_sd_espera(self):
        suma = 0
        promedio = self.espera["espera promedio"]
        for replica in self.dict_espera_simulacion.keys():
            valor = self.dict_espera_simulacion[replica]
            resta = valor - promedio
            cubo = resta * resta
            suma += cubo
        total = suma / p.REPLICAS
        return {"espera sd": total}
    
    def calcular_ocupacion_promedio(self):
        dict_ = {}
        suma = 0
        for llave in self.dict_ocupacion.keys():
            dict_[llave] = self.dict_ocupacion[llave] / p.REPLICAS
            suma += self.dict_ocupacion[llave]
        total_1 = suma / (p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)
        total = total_1 / p.REPLICAS
        return {"ocupacion promedio": total}
    
    def calcular_sd_ocupacion(self):
        suma = 0
        promedio = self.ocupacion["ocupacion promedio"]
        for replica in self.dict_ocupacion_simulacion.keys():
            valor = self.dict_ocupacion_simulacion[replica]
            resta = valor - promedio
            cubo = resta * resta
            suma += cubo
        total = suma / p.REPLICAS
        return {"ocupacion sd": total}