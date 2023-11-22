import parametros as p
from caja import Caja
import numpy
from no_homogeneo import tasa_no_homogeneo
import random
import scipy.stats as sp

### "llegada" = ocurre una llegada y se va a comprar
### "compra" = termina de comprar y se va a cola caja
### "atencion" = termina servicio caja, atiende a uno nuevo
### "clientes comprando" = clientes que estan activamente comprando
### "clientes caja" = idk

class Supermercado:

    def __init__(self):
        self.dict_cajas = {"normal": {}, "rapida": {}}
        self.tipo_caja_actual = None
        self.dict_tiempo_proximo = {"llegada": p.INFINITO, "compra": p.INFINITO, "atencion": p.INFINITO}
        self.dict_evento_anterior = {"evento": "", "tiempo": 0}
        self.cantidad_clientes_comprando = 0
        self.cantidad_clientes_caja = 0
        self.estado = "abierto"
        self.tiempos_fin_compra = {"tiempo_actual": None,
                                    "tiempo_compra": [], ### tiempo llegada + tiempo compra
                                    "tiempo_atencion_normal": [], ### tiempo llegada + tiempo atencion
                                    "tiempo_atencion_rapida": None}

        self.caja_rapida = None
        self.tipo_caja_rapida = None
        self.cantidad_llegadas = 0
        self.cantidad_atenciones = 0
        self.dict_tiempo_espera_caja = {"normal": {}, "rapida": {}}
        self.dict_ocupacion_caja = {"normal": {}, "rapida": {}}

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
            
    def actualizar_tiempos(self, tiempo_actual, entrada):
        # print(f"tiempo actual: {tiempo_actual}")
        eventos = self.verificar_proximo_evento(entrada)
        for evento in eventos:
            self.dict_tiempo_proximo[evento] = self.calcular_tiempos(evento, tiempo_actual)

        # print("tiempos:", self.dict_tiempo_proximo)

    def verificar_proximo_evento(self, entrada):
        if entrada == "simulacion":
            lista = []
            if self.estado == "abierto":
                lista.append("llegada")
            if self.cantidad_clientes_comprando > 0:
                lista.append("compra")
            if self.cantidad_clientes_caja > 0:
                lista.append("atencion")
        elif entrada == "ocurre_evento":
            lista = ["atencion"]
        #print(f"VERIFICAR EVENTO - lista: {lista}")
        return lista

    def calcular_tiempos(self, evento, tiempo_actual):
        # print(f"Calculamos tiempo evento {evento}")
        if evento == "llegada":
            tasa = tasa_no_homogeneo(tiempo_actual)
            llegada = numpy.random.exponential(1 / tasa)
            tiempo = llegada + tiempo_actual
            return tiempo
        elif evento == "compra":
            tiempo = min(self.tiempos_fin_compra["tiempo_compra"])
            return tiempo
        elif evento == "atencion":
            self.caja_rapida, tiempo, self.tipo_caja_rapida = self.caja_mas_rapida()
            return tiempo + tiempo_actual
            
    def calcular_tiempo_compra(self):
        datos_tasa_compra = p.DATOS_COMPRA
        parametros = datos_tasa_compra[1]
        parametro_1 = parametros[0]
        parametro_2 = parametros[1]
        parametro_3 = parametros[2]
        tiempo = sp.lognorm.rvs(s=parametro_1, loc=parametro_2, scale=parametro_3, size=1)
        if tiempo <= 0:
            return self.calcular_tiempo_compra()
        return tiempo
    
    def caja_mas_rapida(self):
        # ##### elegir si es caja normal o rapida
        dict_ = self.carrera_exponencial_cajas()
        # print(f"dict_: {dict_}")
        minimo = p.INFINITO
        llave_oficial = p.INFINITO
        tipo = None
        for llave in dict_.keys():
            # print(f"minimo: {minimo}, valor: {valor}")
            if dict_[llave][0] < minimo:
                # print(f"minimo: {minimo}, valor: {valor}")
                minimo = dict_[llave][0]
                tipo_caja_rapida = dict_[llave][1]
                llave_oficial = llave
        if llave_oficial == p.INFINITO:
            return None
        # print(f"minimo: {minimo}, llave oficial: {llave_oficial}, tipo caja rapida: {tipo_caja_rapida}")
        return llave_oficial, minimo, tipo_caja_rapida

    def carrera_exponencial_cajas(self):
        dict_id_tiempo_caja = {}
        # diccionario_elegido = self.dict_cajas[self.tipo_caja_actual]
        # print(f"CARRERA EXPONENCIAL CAJAS - {diccionario_elegido}")
        for tipo_caja in self.dict_cajas.keys():
            for caja in self.dict_cajas[tipo_caja].values():
                # print(self.tipo_caja_actual)
                # print(f"CARRERA EXPONENCIAL CAJAS - tipo: {tipo_caja}, id: {caja.id_caja}, cola: {caja.cola_caja}")
                if caja.cola_caja > 0:
                    tiempo = self.calcular_tiempo_caja(tipo_caja)
                    dict_id_tiempo_caja[caja.id_caja] = (tiempo, tipo_caja)
                # elif caja.cola_caja > 0 and tipo_caja == "normal":
                #     dict_id_tiempo_caja[caja.id_caja] = (caja.tiempo_evento_atencion.queue[0], tipo_caja)
        return dict_id_tiempo_caja

    def calcular_tiempo_caja(self, tipo_caja):
        
        if tipo_caja == "rapida":
            datos_tasa = p.DATOS_ATENCION["rapida"]
        elif tipo_caja == "normal":
            datos_tasa = p.DATOS_ATENCION["normal"]

        nombre_distribucion = datos_tasa[0]
        parametros = datos_tasa[1]

        if nombre_distribucion == "lognorm":
            parametro_1 = parametros[0]
            parametro_2 = parametros[1]
            parametro_3 = parametros[2]
            tiempo = sp.lognorm.rvs(s=parametro_1, loc=parametro_2, scale=parametro_3, size=1)[0]

        elif nombre_distribucion == "gamma":
            parametro_1 = parametros[0]
            parametro_2 = parametros[1]
            parametro_3 = parametros[2]
            tiempo = sp.gamma.rvs(a=parametro_1, loc=parametro_2, scale=parametro_3, size=1)[0]

        elif nombre_distribucion == "beta":
            parametro_1 = parametros[0]
            parametro_2 = parametros[1]
            parametro_3 = parametros[2]
            parametro_4 = parametros[3]
            tiempo = sp.beta.rvs(a=parametro_1, b=parametro_2, loc=parametro_3, scale=parametro_4, size=1)[0]

        elif nombre_distribucion == "expon":
            parametro_1 = parametros[0]
            parametro_2 = parametros[1]
            tiempo = sp.expon.rvs(loc=parametro_1, scale=parametro_2, size=1)[0]

        elif nombre_distribucion == "uniform":
            parametro_1 = parametros[0]
            parametro_2 = parametros[1]
            tiempo = sp.uniform.rvs(loc=parametro_1, scale=parametro_2, size=1)[0]

        if tiempo < 0:
            return self.calcular_tiempo_caja(tipo_caja)

        return tiempo
    
    def proximo_evento(self, tiempo_actual):
        # print(f"PROXIMO EVENTO: dict eventos: {self.dict_tiempo_proximo}")
        minimo = p.INFINITO
        for evento in self.dict_tiempo_proximo.keys():
            if self.dict_tiempo_proximo[evento] <= minimo:
                minimo = self.dict_tiempo_proximo[evento]
                proxima_accion = evento
        duracion = minimo - tiempo_actual
        # print(f"Proximo evento: {proxima_accion}, duración: {duracion}, tiempo final: {minimo}")
        return proxima_accion, minimo, duracion

    def ocurre_evento(self, evento, tiempo_evento, tiempo_actual):
        # print(f"ANTES - Evento: {evento}, tiempo evento: {tiempo_evento}, tiempo actual: {tiempo_actual}, comprando: {self.cantidad_clientes_comprando}, en fila: {self.cantidad_clientes_caja}, llegadas: {self.cantidad_llegadas}, atenciones: {self.cantidad_atenciones}")
        
        if evento == "llegada":
            self.cantidad_clientes_comprando += 1
            self.cantidad_llegadas += 1
            tiempo_compra = float(self.calcular_tiempo_compra())
            self.tiempos_fin_compra["tiempo_compra"].append(tiempo_compra + tiempo_actual)
            # print("lista en llegada", self.tiempos_fin_compra["tiempo_compra"])

        elif evento == "compra":
            self.cantidad_clientes_comprando -= 1
            self.cantidad_clientes_caja += 1
            # print("lista en compra antes", self.tiempos_fin_compra["tiempo_compra"])
            self.tiempos_fin_compra["tiempo_compra"].remove(tiempo_actual)
            # print("lista en compra despues", self.tiempos_fin_compra["tiempo_compra"])
            ##### elegir si es caja normal o rapida
            self.tipo_caja_actual = self.elegir_tipo_caja()
            #### escogemos cola mas corta
            id_caja = self.cola_caja_mas_corta()
            # print(f"caja tipo: {self.tipo_caja_actual} de id: {id_caja} sube 1")
            self.dict_cajas[self.tipo_caja_actual][id_caja].cola_caja += 1
            self.dict_cajas[self.tipo_caja_actual][id_caja].tiempo_llegada_cola.put(tiempo_actual)

            if self.dict_cajas[self.tipo_caja_actual][id_caja].estado == "vacia":
                self.dict_cajas[self.tipo_caja_actual][id_caja].estado == "ocupada"
                self.tipo_caja_rapida = self.tipo_caja_actual
                self.caja_rapida = id_caja
                tiempo_atencion = self.calcular_tiempo_caja(self.tipo_caja_actual)
                #if self.tipo_caja_rapida == "normal":
                # self.dict_cajas[self.tipo_caja_actual][id_caja].tiempo_atencion_caja.put(tiempo_actual + tiempo_atencion)
                # self.dict_cajas[self.tipo_caja_actual][id_caja].tiempo_evento_atencion.put(tiempo_atencion)
                return self.actualizar_tiempos(tiempo_actual, "ocurre_evento")
            # else: 
            #     #if self.tipo_caja_actual == "normal":
            #         ### calcular tiempo evento atencion normal
            #         tiempo_atencion_normal = self.calcular_tiempo_caja(self.tipo_caja_actual)
            #         prediccion = self.dict_cajas[self.tipo_caja_actual][id_caja].sumar_atenciones()
            #         self.dict_cajas[self.tipo_caja_actual][id_caja].tiempo_atencion_caja.put(tiempo_actual + tiempo_atencion_normal + prediccion)
            #         self.dict_cajas[self.tipo_caja_actual][id_caja].tiempo_evento_atencion.put(tiempo_atencion_normal)
                
        elif evento == "atencion":
            # print(f"Evento atencion y tipo caja: {self.tipo_caja_rapida}")
            self.cantidad_clientes_caja -= 1
            self.cantidad_atenciones += 1            
            instancia_caja = self.dict_cajas[self.tipo_caja_rapida][self.caja_rapida]
            instancia_caja.cola_caja -= 1
            if instancia_caja.cola_caja == 0:
                instancia_caja.estado == "vacia"
            tiempo_llegada = instancia_caja.tiempo_llegada_cola.get()
            # if instancia_caja.tipo == "normal":
            #     tiempo_atencion_caja = instancia_caja.tiempo_atencion_caja.get()
            #     tiempo_evento_atencion = instancia_caja.tiempo_evento_atencion.get()
            #     espera = tiempo_atencion_caja - tiempo_evento_atencion - tiempo_llegada
            #     # print(f"espera normal: {espera}")
            # else:
            espera = tiempo_actual - tiempo_evento - tiempo_llegada 
                # print(f"espera rapida: {espera} = {tiempo_actual} - {tiempo_evento} - {tiempo_llegada}")
            # print(f"espera en cola: {espera}")
            self.dict_tiempo_espera_caja[self.tipo_caja_rapida][instancia_caja.id_caja].append(espera)
        self.agregar_tiempo_ocupacion(tiempo_evento)
        # print(f"DESPUES - Evento: {evento}, tiempo evento: {tiempo_evento}, tiempo actual: {tiempo_actual}, comprando: {self.cantidad_clientes_comprando}, en fila: {self.cantidad_clientes_caja}, llegadas: {self.cantidad_llegadas}, atenciones: {self.cantidad_atenciones}")

    def elegir_tipo_caja(self):
        # print(f"ELEGIR TIPO CAJA - tipo actual: {self.tipo_caja_actual}")
        lista_opciones_valores = []
        for key_tipo_caja in self.dict_cajas.keys():
            for caja in self.dict_cajas[key_tipo_caja].values():
                if key_tipo_caja not in lista_opciones_valores:
                    lista_opciones_valores.append(key_tipo_caja)

        # if self.tipo_caja_actual == None or self.cantidad_clientes_caja == 0 or self.cantidad_clientes_comprando > 0 or evento == "compra":
        if self.tipo_caja_actual == None:
            tipo_caja = random.choices(["rapida", "normal"], weights = [p.PROBABILIDAD_ELEGIR_CAJA_RAPIDA, p.PROBABILIDAD_ELEGIR_CAJA_NORMAL])          
        elif "normal" in lista_opciones_valores and "rapida" in lista_opciones_valores:
            tipo_caja = random.choices(["rapida", "normal"], weights = [p.PROBABILIDAD_ELEGIR_CAJA_RAPIDA, p.PROBABILIDAD_ELEGIR_CAJA_NORMAL])
        elif "normal" in lista_opciones_valores and len(lista_opciones_valores) == 1:
            tipo_caja = random.choices(["rapida", "normal"], weights = [0, 1])
        elif "rapida" in lista_opciones_valores and len(lista_opciones_valores) == 1:
            tipo_caja = random.choices(["rapida", "normal"], weights = [1, 0])
        else:
            print("No se elige el tipo de caja")
        return tipo_caja[0]
    
    def cola_caja_mas_corta(self):
        dict_caja_cola = {}
        # print(F"COLA MAS CORTA - tipo caja actual: {self.tipo_caja_actual}")
        for tipo_caja in self.dict_cajas.keys():
            for caja in self.dict_cajas[tipo_caja].values():
                if self.tipo_caja_actual == tipo_caja:
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
        return id_eleccion

    def agregar_tiempo_ocupacion(self, tiempo):
        for tipo_caja in self.dict_ocupacion_caja.keys():
            for llave in self.dict_cajas[tipo_caja].keys():
                if self.dict_cajas[tipo_caja][llave].cola_caja > 0:
                    self.dict_ocupacion_caja[tipo_caja][llave] += tiempo

    def actualizar_dict_tiempo_anterior(self, evento, tiempo):
        self.dict_evento_anterior["evento"] = evento
        self.dict_evento_anterior["tiempo"] = tiempo
        self.dict_tiempo_proximo = {"llegada": p.INFINITO, "compra": p.INFINITO, "atencion": p.INFINITO}

