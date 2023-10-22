from guardar_datos import cargar_datos
import parametros as p

def valor_replica(ruta, rep):
    replica = str(rep - 1)
    dict_ = cargar_datos(ruta)
    for caja in dict_[replica].keys():
        valor = dict_[replica][caja]
        redondeo = round(valor, 2)
        print(redondeo)


def valor_caja(ruta):
    dict_ = cargar_datos(ruta)
    for caja in dict_.keys():
        valor = dict_[caja]
        redondeo = round(valor, 2)
        print(redondeo)

def promedios_error(ruta):
    print("ruta", ruta)
    dict_ = cargar_datos(ruta)
    suma_normal = 0
    suma_rapida = 0
    for caja in dict_.keys():
        error = dict_[caja]
        # print("error", error)
        if 0 <= int(caja) < p.CANTIDAD_CAJAS_NORMALES:
            suma_normal += error
        else:
            suma_rapida += error
    error_normal = round(suma_normal / p.CANTIDAD_CAJAS_NORMALES, 2)
    error_rapida = round(suma_rapida / p.CANTIDAD_CAJAS_RAPIDAS, 2)
    print(f"error normal: {error_normal}, error rapida: {error_rapida}")

def promedios_intervalos(ruta):
    print("ruta", ruta)
    dict_ = cargar_datos(ruta)
    suma_normal_min = 0
    suma_rapida_min = 0
    suma_normal_max = 0
    suma_rapida_max = 0
    for caja in dict_.keys():
        intervalo = dict_[caja]
        minimo = intervalo[0]
        maximo = intervalo[1]
        if 0 <= int(caja) < p.CANTIDAD_CAJAS_NORMALES:
            suma_normal_min += minimo
            suma_normal_max += maximo
        else:
            suma_rapida_min += minimo
            suma_rapida_max += maximo
    normal_min = round(suma_normal_min / p.CANTIDAD_CAJAS_NORMALES, 2)
    normal_max = round(suma_normal_max / p.CANTIDAD_CAJAS_NORMALES, 2)
    rapida_min = round(suma_rapida_min / p.CANTIDAD_CAJAS_RAPIDAS, 2)
    rapida_max = round(suma_rapida_max / p.CANTIDAD_CAJAS_RAPIDAS, 2)
    print(f"normal: [{normal_min}, {normal_max}]")
    print(f"rapida: [{rapida_min}, {rapida_max}]")


# valor_replica(p.LISTA_PATH[1], 30)
# valor_caja(p.LISTA_PATH[1])
for i in range(11, 15):
    promedios_error(p.LISTA_PATH[i])

for j in range(7, 11):
    promedios_intervalos(p.LISTA_PATH[j])

