from guardar_datos import cargar_datos
import parametros as p
import pandas as pd

dict_espera_replicas = cargar_datos(p.LISTA_PATH[0])
dict_ocupacion_replicas = cargar_datos(p.LISTA_PATH[1])
dict_espera = cargar_datos(p.LISTA_PATH[3])
dict_ocupacion = cargar_datos(p.LISTA_PATH[4])
dict_sd_espera = cargar_datos(p.LISTA_PATH[5])
dict_sd_ocupacion = cargar_datos(p.LISTA_PATH[6])
dict_int_95_espera = cargar_datos(p.LISTA_PATH[7])
dict_int_95_ocupacion = cargar_datos(p.LISTA_PATH[8])
dict_err_95_espera = cargar_datos(p.LISTA_PATH[9])
dict_err_95_ocupacion = cargar_datos(p.LISTA_PATH[10])

df_espera = pd.DataFrame(list(dict_espera.items()), columns=["Replica", "Tiempo de Espera [min] promedio"])
df_espera.to_excel("excel/tiempos_espera_promedio.xlsx", index=False)

df_ocupacion = pd.DataFrame(list(dict_ocupacion.items()), columns=["Replica", "Porcentaje de Ocupación [%] promedio"])
df_ocupacion.to_excel("excel/porcentaje_ocupacion_promedio.xlsx", index=False)

df_sd_espera = pd.DataFrame(list(dict_sd_espera.items()), columns=["Replica", "Dev. Estándar Espera"])
df_sd_espera.to_excel("excel/sd_espera.xlsx", index=False)

df_sd_ocupacion = pd.DataFrame(list(dict_sd_ocupacion.items()), columns=["Replica", "Dev. Estándar Ocupación"])
df_sd_ocupacion.to_excel("excel/sd_ocupacion.xlsx", index=False)

df_int_95_espera = pd.DataFrame(dict_int_95_espera.items(), columns=['Replica', 'Intervalo Espera [min] al 95%'])
df_int_95_espera.to_excel('excel/int_95_espera.xlsx', index=False)

df_int_95_ocupacion = pd.DataFrame(dict_int_95_ocupacion.items(), columns=['Replica', 'Intervalo Ocupación [%] al 95%'])
df_int_95_ocupacion.to_excel('excel/int_95_ocupacion.xlsx', index=False)

df_err_95_esperado = pd.DataFrame(dict_err_95_espera.items(), columns=['Replica', 'Error Espera al 95%'])
df_err_95_esperado.to_excel('excel/err_95_espera.xlsx', index=False)

df_err_95_ocupacion = pd.DataFrame(dict_err_95_ocupacion.items(), columns=['Replica', 'Error Ocupación al 95%'])
df_err_95_ocupacion.to_excel('excel/err_95_ocupacion.xlsx', index=False)

df_espera_replicas = pd.DataFrame(dict_espera_replicas.items(), columns=['Replica', 'Tiempo de Espera [min] promedio'])
df_espera_replicas.to_excel('excel/espera_replicas.xlsx', index=False)

df_ocupacion_replicas = pd.DataFrame(dict_ocupacion_replicas.items(), columns=['Replica', 'Porcentaje de Ocupación [%] promedio'])
df_ocupacion_replicas.to_excel('excel/ocupacion_replicas.xlsx', index=False)
