from queue import Queue

class Caja:

    def __init__(self, id, tipo):
        self.id_caja = id
        self.cola_caja = 0
        self.tipo = tipo
        self.estado = "vacia"
        self.tiempo_llegada_cola = Queue()




        