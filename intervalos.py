from guardar_datos import cargar_datos
import parametros as p
import math

class Intervalo:

    def __init__(self):
        self.dict_espera = cargar_datos(p.LISTA_PATH[3])
        self.dict_ocupacion = cargar_datos(p.LISTA_PATH[4])
        self.sd_espera = cargar_datos(p.LISTA_PATH[5])
        self.sd_ocupacion = cargar_datos(p.LISTA_PATH[6])
        self.int_espera_90 = {}
        self.int_ocupacion_90 = {}
        self.int_espera_95 = {}
        self.int_ocupacion_95 = {}
        self.error_90_espera = {}
        self.error_90_ocupacion = {}
        self.error_95_espera = {}
        self.error_95_ocupacion = {}

    def definir_valor_t(self, confianza):
        if confianza == 90:
            return 1.697
        elif confianza == 95:
            return 2.042
        
    def calcular_intervalo_espera(self, confianza):
        for caja in self.dict_espera.keys():
            promedio = self.dict_espera[caja]
            sd = self.sd_espera[caja]
            sqrt_n = math.sqrt(p.REPLICAS)
            valor_t = self.definir_valor_t(confianza)
            min = promedio - (valor_t * (sd / sqrt_n))
            max = promedio + (valor_t * (sd / sqrt_n))
            intervalo = [min, max]
            self.calcular_error_espera(min, max, caja, confianza)
            if confianza == 90:
                self.int_espera_90[caja] = intervalo
            elif confianza == 95:
                self.int_espera_95[caja] = intervalo
        if confianza == 90:
            return self.int_espera_90
        elif confianza == 95:
            return self.int_espera_95

    def calcular_intervalo_ocupacion(self, confianza):
        for caja in self.dict_ocupacion.keys():
            promedio = self.dict_ocupacion[caja]
            sd = self.sd_ocupacion[caja]
            sqrt_n = math.sqrt(p.REPLICAS)
            valor_t = self.definir_valor_t(confianza)
            min = promedio - (valor_t * (sd / sqrt_n))
            max = promedio + (valor_t * (sd / sqrt_n))
            intervalo = [min, max]
            self.calcular_error_ocupacion(min, max, caja, confianza)
            if confianza == 90:
                self.int_ocupacion_90[caja] = intervalo
            elif confianza == 95:
                self.int_ocupacion_95[caja] = intervalo
        if confianza == 90:
            return self.int_ocupacion_90
        elif confianza == 95:
            return self.int_ocupacion_95
        
    def calcular_error_espera(self, min, max, llave, confianza):
        promedio = self.dict_espera[llave]
        diferencia = max - min
        mitad = (max - min) / 2
        error = (mitad) * 100 / promedio
        if confianza == 90:
            self.error_90_espera[llave] = error
        elif confianza == 95:
            self.error_95_espera[llave] = error
        
    def calcular_error_ocupacion(self, min, max, llave, confianza):
        promedio = self.dict_ocupacion[llave]
        mitad = (max - min) / 2
        error = (mitad) * 100 / promedio
        if confianza == 90:
            self.error_90_ocupacion[llave] = error
        elif confianza == 95:
            self.error_95_ocupacion[llave] = error


# inter = Intervalo()
# inter.calcular_intervalo_espera()
# inter.calcular_intervalo_ocupacion()