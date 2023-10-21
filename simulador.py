import parametros as p
from simulacion import Simulacion
import time
from guardar_datos import guardar_resultados, crear_archivo, cargar_datos


class Simulador:

    def __init__(self):
        self.dict_duracion_replica = {}
        self.simulacion = Simulacion()
        
        self.dict_espera = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}
        self.dict_ocupacion = {i: 0 for i in range(p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS)}

    def simular_replica(self):

        tiempo_inicio_simulacion_replica = time.time()
        crear_archivo()

        for replica in range(p.REPLICAS):

            print(f"replica: {replica} --------------- ")

            self.simulacion = Simulacion()
            tiempo_inicio = time.time()

            self.simulacion.simular()
            self.sumar_tiempos_espera_cola()
            self.sumar_porcentaje_ocupacion()

            tiempo_fin = time.time()
            duracion_replica = tiempo_fin - tiempo_inicio
            self.dict_duracion_replica[replica] = duracion_replica

            print("\n")

        tiempo_fin_simulacion_replica = time.time()
        duracion_total = tiempo_fin_simulacion_replica - tiempo_inicio_simulacion_replica
        self.dict_duracion_replica["promedio"] = duracion_total / p.REPLICAS
        self.dict_duracion_replica["total"] = duracion_total

        print(f"PROMEDIO ESPERA COLA: {self.calcular_espera_promedio()}")
        print(f"PROMEDIO OCUPACION: {self.calcular_ocupacion_promedio()}")
        
        guardar_resultados("datos\diccionario_tiempo_de_ejecucion.json", self.dict_duracion_replica)

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
            dict_[llave] = self.dict_espera[llave] / 10
        return dict_
    
    def calcular_ocupacion_promedio(self):
        dict_ = {}
        for llave in self.dict_ocupacion.keys():
            dict_[llave] = self.dict_ocupacion[llave] / 10
        return dict_
