import parametros as p

def tasa_no_homogeneo(minutos):
    dict_llegada = p.DICCIONARIO_DATOS_LLEGADAS
    # if minutos == p.JORNADA * p.MINUTOS_POR_HORA:
    #     jornada = p.JORNADA - 1
    #     return dict_llegada[f"{jornada}"]
    hora = int(minutos / p.MINUTOS_POR_HORA)
    tasa_llegada = dict_llegada[str(hora)]
    return tasa_llegada
    
