from guardar_datos import cargar_datos
import parametros as p
import pandas as pd

dict_espera = cargar_datos(p.LISTA_PATH[3])
dict_ocupacion = cargar_datos(p.LISTA_PATH[4])
dict_sd_espera = cargar_datos(p.LISTA_PATH[5])
dict_sd_ocupacion = cargar_datos(p.LISTA_PATH[6])
dict_int_90_espera = cargar_datos(p.LISTA_PATH[7])
dict_int_90_ocupacion = cargar_datos(p.LISTA_PATH[8])
dict_int_95_espera = cargar_datos(p.LISTA_PATH[9])
dict_int_95_ocupacion = cargar_datos(p.LISTA_PATH[10])
dict_err_90_espera = cargar_datos(p.LISTA_PATH[11])
dict_err_90_ocupacion = cargar_datos(p.LISTA_PATH[12])
dict_err_95_espera = cargar_datos(p.LISTA_PATH[13])
dict_err_95_ocupacion = cargar_datos(p.LISTA_PATH[14])
dict_espera_replicas = cargar_datos(p.LISTA_PATH[0])
dict_ocupacion_replicas = cargar_datos(p.LISTA_PATH[1])

df_espera = pd.DataFrame(list(dict_espera.items()), columns=["Caja", "Tiempo de Espera [min] promedio"])
df_espera.to_excel("excel/tiempos_espera_promedio.xlsx", index=False)

df_ocupacion = pd.DataFrame(list(dict_ocupacion.items()), columns=["Caja", "Porcentaje de Ocupación [%] promedio"])
df_ocupacion.to_excel("excel/porcentaje_ocupacion_promedio.xlsx", index=False)

df_sd_espera = pd.DataFrame(list(dict_sd_espera.items()), columns=["Caja", "Dev. Estándar Espera"])
df_sd_espera.to_excel("excel/sd_espera.xlsx", index=False)

df_sd_ocupacion = pd.DataFrame(list(dict_sd_ocupacion.items()), columns=["Caja", "Dev. Estándar Ocupación"])
df_sd_ocupacion.to_excel("excel/sd_ocupacion.xlsx", index=False)

df_int_90_espera = pd.DataFrame(dict_int_90_espera.items(), columns=['Caja', 'Intervalo Espera [min] al 90%'])
df_int_90_espera.to_excel('excel/int_90_espera.xlsx', index=False)

df_int_95_espera = pd.DataFrame(dict_int_95_espera.items(), columns=['Caja', 'Intervalo Espera [min] al 95%'])
df_int_95_espera.to_excel('excel/int_95_espera.xlsx', index=False)

df_int_90_ocupacion = pd.DataFrame(dict_int_90_ocupacion.items(), columns=['Caja', 'Intervalo Ocupación [%] al 90%'])
df_int_90_ocupacion.to_excel('excel/int_90_ocupacion.xlsx', index=False)

df_int_95_ocupacion = pd.DataFrame(dict_int_95_ocupacion.items(), columns=['Caja', 'Intervalo Ocupación [%] al 95%'])
df_int_95_ocupacion.to_excel('excel/int_95_ocupacion.xlsx', index=False)

df_err_90_esperado = pd.DataFrame(dict_err_90_espera.items(), columns=['Caja', 'Error Espera al 90%'])
df_err_90_esperado.to_excel('excel/err_90_espera.xlsx', index=False)

df_err_90_ocupacion = pd.DataFrame(dict_err_90_ocupacion.items(), columns=['Caja', 'Error Ocupación al 90%'])
df_err_90_ocupacion.to_excel('excel/err_90_ocupacion.xlsx', index=False)

df_err_95_esperado = pd.DataFrame(dict_err_95_espera.items(), columns=['Caja', 'Error Espera al 95%'])
df_err_95_esperado.to_excel('excel/err_95_espera.xlsx', index=False)

df_err_95_ocupacion = pd.DataFrame(dict_err_95_ocupacion.items(), columns=['Caja', 'Error Ocupación al 95%'])
df_err_95_ocupacion.to_excel('excel/err_95_ocupacion.xlsx', index=False)

replicas = []
cajas = []
valores = []
for replica, data in dict_espera_replicas.items():
    for caja, valor in data.items():
        replicas.append(replica)
        cajas.append(caja)
        valores.append(valor)
df_espera_replicas = pd.DataFrame({
    'Réplica': replicas,
    'Caja': cajas,
    'Valor [min]': valores})
df_espera_replicas.to_excel("excel/espera_replicas.xlsx", index=False)

replicas = []
cajas = []
valores = []
for replica, data in dict_ocupacion_replicas.items():
    for caja, valor in data.items():
        replicas.append(replica)
        cajas.append(caja)
        valores.append(valor)
df_ocupacion_replicas = pd.DataFrame({
    'Réplica': replicas,
    'Caja': cajas,
    'Valor [%]': valores})
df_ocupacion_replicas.to_excel("excel/ocupacion_replicas.xlsx", index=False)