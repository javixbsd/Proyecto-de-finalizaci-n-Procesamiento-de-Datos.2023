import yfinance as yf
import pandas as pd
import requests
import csv
from datetime import datetime

#Obtencion de datos historicos del las disctintas acciones que conforman el MERVAL

# Definir la lista de símbolos de las acciones del Merval
acciones_merval = ['ALUA.BA', 'BBAR.BA','BMA.BA','BYMA.BA','CEPU.BA','COME.BA','CRES.BA','CVH.BA','EDN.BA','GGAL.BA','LOMA.BA','MIRG.BA','PAMP.BA','SUPV.BA','TECO2.BA','TGNO4.BA','TGSU2.BA','TRAN.BA','TXAR.BA','VALO.BA','YPFD.BA']
#acciones = ['ALUA.BA', 'BBAR.BA']
# Obtener los datos históricos de las acciones del Merval
datos_historicos = yf.download(acciones_merval, start='2020-01-01', end='2023-06-25')

# LIMPIEZ DE DATOS NULOS
print("Limpieza de datos_historicos")
print("Antes de limpieza de datos_historicos")
# Verificar si hay valores nulos en el DataFrame resultante
print("Existen valores nulos? :",datos_historicos.isnull().values.any())

# Contar la cantidad de valores nulos en el DataFrame resultante
print("Cauntos valores nulos existen? ",datos_historicos.isnull().sum().sum())

# Utilizar dropna() para eliminar filas con valores nulos
datos_historicos = datos_historicos.dropna()
print("Despues de limpieza datos_historicos")
# Verificar si hay valores nulos en el DataFrame resultante
print("Existen valores nulos? :",datos_historicos.isnull().values.any())

# Contar la cantidad de valores nulos en el DataFrame resultante
print("Cauntos valores nulos existen? ",datos_historicos.isnull().sum().sum())


# Tratamiento valores at[ipicos por razones de tiempo no calulado
''' No se sugiere sin calcular antes la volatilidad de cada acción, tambien el estudiuo si tuvo pago de divedendos 
    u otro motivo que un valor no sea un falso valor atípico applicar los siguiente:
    Tratar valores atípicos:

    Identificar y tratar los valores atípicos utilizando técnica de la desviación estándar. 
    Eliminar las filas con valores atípicos utilizando el método quantile() para definir un rango de valores aceptables:
    
    limite_inferior = datos_historicos['Columna'].quantile(0.05)
    limite_superior = datos_historicos['Columna'].quantile(0.95)
    datos_historicos = datos_historicos[(datos_historicos['Columna'] >= limite_inferior) & (datos_historicos['Columna'] <= limite_superior)]

'''



# Crea una lista para almacenar las columnas del nuevo DataFrame
columnas = ['Date']

# Recorre las acciones del Merval y agrega una columna para cada acción con el nombre de la acción seguido de 'Close'
for accion in acciones_merval:
    columnas.append(accion + ' Close')

# Crea un nuevo DataFrame con las columnas correspondientes
nuevo_dataframe = pd.DataFrame(columns=columnas)

# Llena el nuevo DataFrame con los datos de fecha y precios de cierre de cada acción
for fecha, fila in datos_historicos.iterrows():
    nueva_fila = [fecha]
    for accion in acciones_merval:
        nueva_fila.append(round(fila['Close'][accion], 2))
    nuevo_dataframe.loc[len(nuevo_dataframe)] = nueva_fila

# Establecer la columna "Date" como índice
nuevo_dataframe.set_index("Date", inplace=True)

# Muestra los primeros registros del nuevo DataFrame
print(nuevo_dataframe.head())

#Guardamos el DataFrame datos_historicos en un archivo CSV,utilizando el método to_csv() de pandas.
nuevo_dataframe.to_csv("historicoMerval.csv")




#////////////////////////////////////////////////////////////////

#Obtencion de los datos historicos del dolar MEP



url = 'https://mercados.ambito.com//dolarrava/mep/historico-general/2020-01-01/2023-06-25'
response = requests.get(url)
data = response.json()

# Ruta de destino para guardar el archivo CSV
ruta_destino = 'historicoMEP.csv'

# Extraer las filas de datos (excepto la primera fila con los encabezados)
filas = data[1:]

# Crear el archivo CSV y escribir los datos
with open(ruta_destino, 'w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)
    writer.writerow(['Date', 'Precio'])  # Escribir encabezados
    writer.writerows(filas)  # Escribir filas de datos

print(f"Los datos se han guardado en: {ruta_destino}")



# Leer el archivo CSV
datos_mep = pd.read_csv('historicoMEP.csv')

# Convertir la columna "Fecha" al formato deseado
datos_mep['Date'] = pd.to_datetime(datos_mep['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

# Ordenar el DataFrame por fecha en orden ascendente
datos_mep.sort_values(by='Date', ascending=True, inplace=True)

# Convertir la columna "Precio" de string a float
datos_mep['Precio'] = datos_mep['Precio'].str.replace(',', '.').astype(float)

# Mostrar los primeros registros del DataFrame ordenado y con los precios convertidos

datos_mep.reset_index(drop=True, inplace=True)

# Guardar los datos en un archivo CSV
datos_mep.to_csv('historicoMEP.csv', index=False)

print("Los datos limpios se han guardado en 'historicoMEP.csv'.")