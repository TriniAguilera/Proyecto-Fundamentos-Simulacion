from queue import Queue

class Caja:

    def __init__(self, id) -> None:
        self.id_caja = id
        self.cola_caja = 0
        self.estado = "vacia"
        self.tiempo_llegada_cola = Queue()




        