from queue import Queue
from functools import reduce
import operator

class Caja:

    def __init__(self, id, tipo):
        self.id_caja = id
        self.cola_caja = 0
        self.tipo = tipo
        self.estado = "vacia"
        self.tiempo_entra_persona = 0
        self.tiempo_sale_persona = 0
        self.tiempo_llegada_cola = Queue() ### tiempo en que finaliza compra
        self.tiempo_atencion_caja = Queue() ### tiempo de atencion caja normal total, no el del evento
        self.tiempo_evento_atencion = Queue()

    def sumar_atenciones(self):
        suma = reduce(operator.add, list(self.tiempo_evento_atencion.queue))
        return suma


