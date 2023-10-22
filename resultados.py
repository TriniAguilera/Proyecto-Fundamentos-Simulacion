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

# valor_replica(p.LISTA_PATH[1], 30)
valor_caja(p.LISTA_PATH[1])

