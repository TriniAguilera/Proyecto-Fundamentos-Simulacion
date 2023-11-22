import parametros as p
from supermercado import Supermercado

class Simulacion:

    def __init__(self):
        self.tiempo_actual = 0
        self.supermercado = Supermercado()
        self.dict_promedio_tiempo_espera_cola = {"normal": {}, "rapida": {}}
        self.dict_promedio_ocupacion = {"normal": {}, "rapida": {}}

    def simular(self):
        while self.supermercado.estado != "cerrado":
            # print(f"minuto actual simulacion: {self.tiempo_actual}")
            self.supermercado.actualizar_tiempos(self.tiempo_actual, "simulacion")
            proximo_evento, proximo_tiempo, duracion_evento = self.supermercado.proximo_evento(self.tiempo_actual)
            self.supermercado.ocurre_evento(proximo_evento, duracion_evento, proximo_tiempo)
            self.supermercado.actualizar_dict_tiempo_anterior(proximo_evento, proximo_tiempo)
            
            self.tiempo_actual = proximo_tiempo

            if self.tiempo_actual > p.JORNADA * p.MINUTOS_POR_HORA:
                self.supermercado.estado = "por_cerrar"

            if self.tiempo_actual >= p.JORNADA * p.MINUTOS_POR_HORA and \
                    self.supermercado.cantidad_clientes_comprando == 0 and \
                    self.supermercado.cantidad_clientes_caja == 0:
                self.supermercado.estado = "cerrado"

        self.tiempo_promedio_espera_cola()
        self.ocupacion_promedio_caja()

    def tiempo_promedio_espera_cola(self):
        for tipo_caja in self.supermercado.dict_tiempo_espera_caja.keys():
            for llave in self.supermercado.dict_tiempo_espera_caja[tipo_caja].keys():
                suma = 0
                largo = len(self.supermercado.dict_tiempo_espera_caja[tipo_caja][llave])
                if largo == 0:
                    self.dict_promedio_tiempo_espera_cola[tipo_caja][llave] = 0
                else:
                    for tiempo in self.supermercado.dict_tiempo_espera_caja[tipo_caja][llave]:
                        suma += tiempo
                    promedio = suma / largo
                    self.dict_promedio_tiempo_espera_cola[tipo_caja][llave] = promedio
        return self.dict_promedio_tiempo_espera_cola
    
    def ocupacion_promedio_caja(self):
        for tipo_caja in self.supermercado.dict_ocupacion_caja.keys():
            for llave in self.supermercado.dict_ocupacion_caja[tipo_caja].keys():  
                if self.supermercado.dict_ocupacion_caja[tipo_caja][llave] == 0:
                    self.dict_promedio_ocupacion[tipo_caja][llave] = 0
                else:
                    self.dict_promedio_ocupacion[tipo_caja][llave] = self.supermercado.dict_ocupacion_caja[tipo_caja][llave]\
                                                            * 100 / (p.JORNADA * p.MINUTOS_POR_HORA)
        return self.dict_promedio_ocupacion

