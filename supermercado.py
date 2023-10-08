import parametros as p
from caja import Caja
from numpy import random

### "llegada" = ocurre una llegada y se va a comprar
### "compra" = termina de comprar y se va a cola caja
### "atencion" = termina servicio caja, atiende a uno nuevo
### "clientes comprando" = clientes que estan activamente comprando
### "clientes caja" = idk

class Supermercado:

    def __init__(self):
        self.dict_cajas = {}
        self.dict_tiempo_proximo = {"llegada": p.INFINITO, "compra": p.INFINITO, "atencion": \
                                                                                        p.INFINITO}
        self.dict_evento_anterior = {"evento": "", "tiempo": 0}
        self.cantidad_clientes_comprando = 0
        self.cantidad_clientes_caja = 0
        self.estado = "abierto"
        self.tiempos_llegadas = []
        self.tiempos_fin_compra = []
        self.caja_rapida = None
        self.cantidad_llegadas = 0
        self.cantidad_atenciones = 0
        self.dict_tiempo_espera_caja = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 
                                        8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 
                                        15: []}
        self.dict_ocupacion_caja = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
                                    10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        self.instanciar_cajas()

    def instanciar_cajas(self):
        for c in range(p.CANTIDAD_DE_CAJAS):
            caja = Caja(c)
            self.dict_cajas[c] = caja
            
    def actualizar_tiempos(self):
        eventos = self.verificar_proximo_evento()
        for evento in eventos:
            self.dict_tiempo_proximo[evento] = self.calcular_tiempos(evento)

    def calcular_tiempos(self, evento):
        if evento == "llegada":
            return random.exponential(p.TASA_LLEGADAS)
        elif evento == "compra":
            tiempo = self.carrera_exponencial_compra()
            return tiempo
        elif evento == "atencion":
            self.caja_rapida, tiempo = self.caja_mas_rapida()
            return tiempo
        
    def carrera_exponencial_cajas(self):
        dict_id_tiempo_caja = {}
        for caja in self.dict_cajas.values():
            if caja.cola_caja > 0:
                tiempo = random.exponential(p.TASA_ATENCION)
                dict_id_tiempo_caja[caja.id_caja] = tiempo
        return dict_id_tiempo_caja
    
    def carrera_exponencial_compra(self):
        minimo = p.INFINITO
        for _ in range(self.cantidad_clientes_comprando):
            tiempo = random.exponential(p.TASA_COMPRA)
            if tiempo < minimo:
                minimo = tiempo
        return minimo

    def caja_mas_rapida(self):
        dict_ = self.carrera_exponencial_cajas()
        minimo = p.INFINITO
        llave_oficial = p.INFINITO
        for llave in dict_.keys():
            if dict_[llave] < minimo:
                minimo = dict_[llave]
                llave_oficial = llave
        return llave_oficial, minimo
    
    def cajas_ocupadas(self):
        lista = []
        for caja in self.dict_cajas.values():
            if caja.cola_caja > 0:
                lista.append(caja.id_caja)
        return lista
        
    def proximo_evento(self):
        minimo = p.INFINITO
        for evento in self.dict_tiempo_proximo.keys():
            if self.dict_tiempo_proximo[evento] <= minimo:
                minimo = self.dict_tiempo_proximo[evento]
                proxima_accion = evento
        return proxima_accion, minimo
    
    def verificar_proximo_evento(self):
        lista = []
        if self.estado == "abierto":
            lista.append("llegada")
        if self.cantidad_clientes_comprando > 0:
            lista.append("compra")
        if self.cantidad_clientes_caja > 0:
            lista.append("atencion")
        return lista
    
    def actualizar_dict_tiempo_anterior(self, evento, tiempo):
        self.dict_evento_anterior["evento"] = evento
        self.dict_evento_anterior["tiempo"] = tiempo
        self.dict_tiempo_proximo = {"llegada": p.INFINITO, "compra": p.INFINITO, "atencion": \
                                                                                        p.INFINITO}

    def ocurre_evento(self, evento, tiempo_evento, tiempo_actual):
        
        if evento == "llegada":
            self.cantidad_clientes_comprando += 1
            self.cantidad_llegadas += 1
            self.tiempos_llegadas.append(tiempo_evento)

        elif evento == "compra":
            self.cantidad_clientes_comprando -= 1
            self.cantidad_clientes_caja += 1
            self.tiempos_fin_compra.append(tiempo_evento)
            #### escogemos cola mas corta
            id_caja = self.cola_caja_mas_corta()
            self.dict_cajas[id_caja].cola_caja += 1

            #### la persona queda en la cola, falta atenderla
            self.dict_cajas[id_caja].tiempo_llegada_cola.put(tiempo_actual)

        elif evento == "atencion":
            self.cantidad_clientes_caja -= 1
            self.cantidad_atenciones += 1
            instancia_caja = self.dict_cajas[self.caja_rapida]
            instancia_caja.cola_caja -= 1
            tiempo_llegada = instancia_caja.tiempo_llegada_cola.get()
            espera = tiempo_actual - tiempo_evento - tiempo_llegada
            self.dict_tiempo_espera_caja[instancia_caja.id_caja].append(espera)
        self.agregar_tiempo_ocupacion(tiempo_evento)

    def cola_caja_mas_corta(self):
        dict_caja_cola = {}
        for caja in self.dict_cajas.values():
            dict_caja_cola[caja.cola_caja] = caja.id_caja

        menor_cola = min(dict_caja_cola.keys())
        id_caja = dict_caja_cola[menor_cola]

        #### elegimos caja aleatoria del largo minimo
        minimo_largo = self.dict_cajas[id_caja].cola_caja
        lista_eleccion = []
        for caja in self.dict_cajas.values():
            if caja.cola_caja == minimo_largo:
                lista_eleccion.append(caja)
        eleccion = random.choice(lista_eleccion)
        id_eleccion = eleccion.id_caja
        id_caja = id_eleccion

        return id_caja

    def agregar_tiempo_ocupacion(self, tiempo):
        for llave in self.dict_ocupacion_caja.keys():
            if self.dict_cajas[llave].cola_caja > 0:
                self.dict_ocupacion_caja[llave] += tiempo






