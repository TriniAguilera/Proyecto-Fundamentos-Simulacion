import parametros as p
from caja import Caja
import numpy
from no_homogeneo import tasa_no_homogeneo
import random

### "llegada" = ocurre una llegada y se va a comprar
### "compra" = termina de comprar y se va a cola caja
### "atencion" = termina servicio caja, atiende a uno nuevo
### "clientes comprando" = clientes que estan activamente comprando
### "clientes caja" = idk

class Supermercado:

    def __init__(self):
        self.dict_cajas = {"normal": {}, "rapida": {}}
        self.tipo_caja_actual = "normal"
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
        self.dict_tiempo_espera_caja = {"normal": {}, "rapida": {}}
        # self.dict_tiempo_espera_caja = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 
        #                                 8: [], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 
        #                                 15: []}
        self.dict_ocupacion_caja = {"normal": {}, "rapida": {}}
        # self.dict_ocupacion_caja = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
        #                             10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
        self.instanciar_cajas()

    def instanciar_cajas(self):
        
        for c in range(p.CANTIDAD_CAJAS_NORMALES):
          # print(f"Creo caja NORMAL de id {c}")
            caja = Caja(c, "normal")
            self.dict_cajas["normal"][c] = caja
            self.dict_tiempo_espera_caja["normal"][c] = []
            self.dict_ocupacion_caja["normal"][c] = 0

        for cr in range(p.CANTIDAD_CAJAS_NORMALES, p.CANTIDAD_CAJAS_NORMALES + p.CANTIDAD_CAJAS_RAPIDAS):
          # print(f"Creo caja RAPIDA de id {cr}")
            caja = Caja(cr, "rapida")
            self.dict_cajas["rapida"][cr] = caja
            self.dict_tiempo_espera_caja["rapida"][cr] = []
            self.dict_ocupacion_caja["rapida"][cr] = 0
            
    def actualizar_tiempos(self, tiempo_actual):
        eventos = self.verificar_proximo_evento()
        for evento in eventos:
            self.dict_tiempo_proximo[evento] = self.calcular_tiempos(evento, tiempo_actual)

    def calcular_tiempos(self, evento, tiempo_actual):
        if evento == "llegada":
            tasa = tasa_no_homogeneo(tiempo_actual)
            return numpy.random.exponential(tasa)
        elif evento == "compra":
            tiempo = self.carrera_exponencial_compra()
            return tiempo
        elif evento == "atencion":
            self.caja_rapida, tiempo = self.caja_mas_rapida()
            return tiempo
        
    def carrera_exponencial_cajas(self):
        dict_id_tiempo_caja = {}
        diccionario_elegido = self.dict_cajas[self.tipo_caja_actual]
        for caja in diccionario_elegido.values():
            if caja.cola_caja > 0:
                tiempo = numpy.random.exponential(p.TASA_ATENCION[self.tipo_caja_actual])
                dict_id_tiempo_caja[caja.id_caja] = tiempo
        return dict_id_tiempo_caja
    
    def carrera_exponencial_compra(self):
        minimo = p.INFINITO
        for _ in range(self.cantidad_clientes_comprando):
            tiempo = numpy.random.exponential(p.TASA_COMPRA)
            if tiempo < minimo:
                minimo = tiempo
        return minimo

    def caja_mas_rapida(self):
        ##### elegir si es caja normal o rapida
        self.tipo_caja_actual = self.elegir_tipo_caja()

        dict_ = self.carrera_exponencial_cajas()
      # print(f"dict_: {dict_}")
        minimo = p.INFINITO
        llave_oficial = p.INFINITO
        for llave in dict_.keys():
            valor = dict_[llave]
            # print(f"minimo: {minimo}, valor: {valor}")
            if dict_[llave] < minimo:
                # print(f"minimo: {minimo}, valor: {valor}")
                minimo = dict_[llave]
                llave_oficial = llave
        if llave_oficial == p.INFINITO:
          # print(self.tipo_caja_actual, self.dict_cajas[self.tipo_caja_actual])
          # print("CAGAMOS")
            return None
      # print(f"minimo: {minimo}, llave oficial: {llave_oficial}")
        return llave_oficial, minimo
    
    def elegir_tipo_caja(self):
        lista_opciones_valores = []

        for tipo_caja in self.dict_cajas.keys():
            for caja in self.dict_cajas[tipo_caja].values():
                if caja.cola_caja > 0 and tipo_caja not in lista_opciones_valores:
                    lista_opciones_valores.append(tipo_caja)
                    
        if "normal" in lista_opciones_valores and "rapida" in lista_opciones_valores:
            tipo_caja = random.choices(["rapida", "normal"], weights = [p.PROBABILIDAD_ELEGIR_CAJA_RAPIDA, p.PROBABILIDAD_ELEGIR_CAJA_NORMAL])
        elif "normal" in lista_opciones_valores and len(lista_opciones_valores) == 1:
            tipo_caja = random.choices(["rapida", "normal"], weights = [0, 1])
        elif "rapida" in lista_opciones_valores and len(lista_opciones_valores) == 1:
            tipo_caja = random.choices(["rapida", "normal"], weights = [1, 0])
        else:
            print("QUEDO LA CAGAAAAAAAAAAAAA")
            
        return tipo_caja[0]

    # def cajas_ocupadas(self):
    #     lista = []
    #     for caja in self.dict_cajas.values():
    #         if caja.cola_caja > 0:
    #             lista.append(caja.id_caja)
    #     return lista
        
    def proximo_evento(self):
        minimo = p.INFINITO
        for evento in self.dict_tiempo_proximo.keys():
            if self.dict_tiempo_proximo[evento] <= minimo:
                minimo = self.dict_tiempo_proximo[evento]
                proxima_accion = evento
      # print(f"proxima accion {proxima_accion}, minimo: {minimo}")
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
      # print(f"Evento: {evento}, tiempo evento: {tiempo_evento}")
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
          # print(f"caja tipo: {self.tipo_caja_actual} de id: {id_caja} sube 1")
            self.dict_cajas[self.tipo_caja_actual][id_caja].cola_caja += 1

            #### la persona queda en la cola, falta atenderla
            self.dict_cajas[self.tipo_caja_actual][id_caja].tiempo_llegada_cola.put(tiempo_actual)

        elif evento == "atencion":
            self.cantidad_clientes_caja -= 1
            self.cantidad_atenciones += 1
            # print(f"holaaaaaa {self.dict_cajas[self.tipo_caja_actual]}")
            # print(f"caja tipo: {self.tipo_caja_actual} de id: {id_caja} baja 1")
            instancia_caja = self.dict_cajas[self.tipo_caja_actual][self.caja_rapida]
            instancia_caja.cola_caja -= 1
            tiempo_llegada = instancia_caja.tiempo_llegada_cola.get()
            espera = tiempo_actual - tiempo_evento - tiempo_llegada
            self.dict_tiempo_espera_caja[self.tipo_caja_actual][instancia_caja.id_caja].append(espera)
        self.agregar_tiempo_ocupacion(tiempo_evento)

    def cola_caja_mas_corta(self):
        dict_caja_cola = {}
        for caja in self.dict_cajas[self.tipo_caja_actual].values():
            dict_caja_cola[caja.cola_caja] = caja.id_caja

        menor_cola = min(dict_caja_cola.keys())
        id_caja = dict_caja_cola[menor_cola]

        #### elegimos caja aleatoria del largo minimo
        minimo_largo = self.dict_cajas[self.tipo_caja_actual][id_caja].cola_caja
        lista_eleccion = []
        for caja in self.dict_cajas[self.tipo_caja_actual].values():
            if caja.cola_caja == minimo_largo:
                lista_eleccion.append(caja)
        eleccion = random.choice(lista_eleccion)
        id_eleccion = eleccion.id_caja
        id_caja = id_eleccion

        return id_caja

    def agregar_tiempo_ocupacion(self, tiempo):
        for tipo_caja in self.dict_ocupacion_caja.keys():
            for llave in self.dict_cajas[tipo_caja].keys():
                if self.dict_cajas[tipo_caja][llave].cola_caja > 0:
                    self.dict_ocupacion_caja[tipo_caja][llave] += tiempo






