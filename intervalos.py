from guardar_datos import cargar_datos
import parametros as p
import math

class Intervalo:

    def __init__(self):
        self.promedio_espera = cargar_datos(p.LISTA_PATH[3])
        self.promedio_ocupacion = cargar_datos(p.LISTA_PATH[4])
        self.sd_espera = cargar_datos(p.LISTA_PATH[5])
        self.sd_ocupacion = cargar_datos(p.LISTA_PATH[6])
        self.int_espera_95 = {}
        self.int_ocupacion_95 = {}
        self.error_95_espera = {}
        self.error_95_ocupacion = {}

    def definir_valor_t(self, confianza):
        if confianza == 95:
            return 2.042
        
    def calcular_intervalo_espera(self, confianza):
        sqrt_n = math.sqrt(p.REPLICAS)
        valor_t = self.definir_valor_t(confianza)
        min = self.promedio_espera["espera promedio"] - (valor_t * (self.sd_espera["espera sd"] / sqrt_n))
        max = self.promedio_espera["espera promedio"] + (valor_t * (self.sd_espera["espera sd"] / sqrt_n))
        intervalo = [min, max]
        self.calcular_error_espera(min, max, confianza)
        if confianza == 95:
            self.int_espera_95[95] = intervalo
            return self.int_espera_95

    def calcular_intervalo_ocupacion(self, confianza):
        promedio = self.promedio_ocupacion["ocupacion promedio"]
        sd = self.sd_ocupacion["ocupacion sd"]
        sqrt_n = math.sqrt(p.REPLICAS)
        valor_t = self.definir_valor_t(confianza)
        min = promedio - (valor_t * (sd / sqrt_n))
        max = promedio + (valor_t * (sd / sqrt_n))
        intervalo = [min, max]
        self.calcular_error_ocupacion(min, max, confianza)
        if confianza == 95:
            self.int_ocupacion_95[95] = intervalo
            return self.int_ocupacion_95
        
    def calcular_error_espera(self, min, max, confianza):
        promedio = self.promedio_espera["espera promedio"]
        mitad = (max - min) / 2
        error = (mitad) * 100 / promedio
        if confianza == 95:
            self.error_95_espera[95] = error
        
    def calcular_error_ocupacion(self, min, max, confianza):
        promedio = self.promedio_ocupacion["ocupacion promedio"]
        mitad = (max - min) / 2
        error = (mitad) * 100 / promedio
        if confianza == 95:
            self.error_95_ocupacion[95] = error

