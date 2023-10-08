import parametros as p
from supermercado import Supermercado

class Simulacion:

    def __init__(self):
        self.tiempo_actual = 0
        self.supermercado = Supermercado()
        self.dict_promedio_tiempo_espera_cola = {}
        self.dict_promedio_ocupacion = {}

    def simular(self):
        while self.supermercado.estado != "cerrado":
            self.supermercado.actualizar_tiempos()
            proximo_evento, proximo_tiempo = self.supermercado.proximo_evento()

            self.supermercado.ocurre_evento(proximo_evento, proximo_tiempo, proximo_tiempo + \
                                                                            self.tiempo_actual)

            self.supermercado.actualizar_dict_tiempo_anterior(proximo_evento, proximo_tiempo)
            self.tiempo_actual += proximo_tiempo

            if self.tiempo_actual > p.JORNADA * p.MINUTOS_POR_HORA:
                self.supermercado.estado = "por_cerrar"

            if self.tiempo_actual >= p.JORNADA * p.MINUTOS_POR_HORA and \
                self.supermercado.cantidad_clientes_comprando == 0 and \
                            self.supermercado.cantidad_clientes_caja == 0:
                self.supermercado.estado = "cerrado"

        self.tiempo_promedio_espera_cola()
        self.ocupacion_promedio_caja()

    def tiempo_promedio_espera_cola(self):
        for llave in self.supermercado.dict_tiempo_espera_caja.keys():
            suma = 0
            largo = len(self.supermercado.dict_tiempo_espera_caja[llave])
            if largo == 0:
                self.dict_promedio_tiempo_espera_cola[llave] = 0
            else:
                for tiempo in self.supermercado.dict_tiempo_espera_caja[llave]:
                    suma += tiempo
                promedio = suma / largo
                self.dict_promedio_tiempo_espera_cola[llave] = promedio
        return self.dict_promedio_tiempo_espera_cola
    
    def ocupacion_promedio_caja(self):
        for llave in self.supermercado.dict_ocupacion_caja.keys():
            if self.supermercado.dict_ocupacion_caja[llave] == 0:
                self.dict_promedio_ocupacion[llave] = 0
            else:
                self.dict_promedio_ocupacion[llave] = self.supermercado.dict_ocupacion_caja[llave]\
                                                        * 100 / (p.JORNADA * p.MINUTOS_POR_HORA)
        return self.dict_promedio_ocupacion
        

        