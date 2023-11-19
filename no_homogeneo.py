import parametros as p

def tasa_no_homogeneo(tiempo_actual):
    hora = int(tiempo_actual / 60)
    minuto = tiempo_actual - hora * 60
    dict_llegada = p.DICCIONARIO_DATOS_LAMBDA
    t = hora + int(minuto / 60)
    tasa = dict_llegada["a"] * t * t + dict_llegada["b"] * t + dict_llegada["c"]
    return tasa
    
