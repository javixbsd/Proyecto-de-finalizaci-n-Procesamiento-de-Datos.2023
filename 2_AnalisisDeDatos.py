import pandas as pd
import matplotlib.pyplot as plt

import numpy as np

# Leer el archivo CSV y cargarlo en un DataFrame
historicoMerval = pd.read_csv("historicoMerval.csv")
historicoMEP = pd.read_csv("historicoMEP.csv")

# Cálculo de estadísticas descriptivas para las acciones del Merval
estadisticas_acciones = historicoMerval.describe()
print("Estadísticas descriptivas para las acciones del Merval:")
print(estadisticas_acciones)

# Cálculo de estadísticas descriptivas para el precio del dólar MEP
estadisticas_dolar_mep = historicoMEP.describe()
print("\nEstadísticas descriptivas para el precio del dólar MEP:")
print(estadisticas_dolar_mep)


# Gráfico de barras para las estadísticas de las acciones del Merval
plt.figure(figsize=(8, 6))
estadisticas_acciones.plot(kind='bar', legend=True)
plt.title('Estadísticas descriptivas para las acciones del Merval')
plt.xlabel('Estadísticas')
plt.ylabel('Valores')
plt.xticks(rotation=0)
plt.show(block=True)

# Gráfico de barras para las estadísticas del precio del dólar MEP
plt.figure(figsize=(8, 6))
estadisticas_dolar_mep.plot(kind='bar', legend=True)
plt.title('Estadísticas descriptivas para el precio del dólar MEP')
plt.xlabel('Estadísticas')
plt.ylabel('Valores')
plt.xticks(rotation=0)
plt.show(block=True)



'''#Calculo de correlacion 
historicoMerval['Date'] = pd.to_datetime(historicoMerval['Date'])
historicoMEP['Date'] = pd.to_datetime(historicoMEP['Date'])

merged_df = pd.merge(historicoMerval, historicoMEP, on='Date')

correlation = merged_df['YPFD.BA Close'].corr(merged_df['Precio'])
print("Correlación entre las acciones de YPFD.BA Close y el precio del dólar MEP:", correlation)
'''

historicoMerval['Date'] = pd.to_datetime(historicoMerval['Date'])
historicoMEP['Date'] = pd.to_datetime(historicoMEP['Date'])

merged_df = pd.merge(historicoMerval, historicoMEP, on='Date')

acciones_merval = [col for col in merged_df.columns if col.endswith('.BA Close')]

correlations = {}

for accion in acciones_merval:
    correlation = merged_df[accion].corr(merged_df['Precio'])
    correlations[accion] = correlation

# Imprimir las correlaciones
for accion, correlation in correlations.items():
    print(f"Correlación entre {accion} y el precio del dólar MEP: {correlation}")



#Caclular remndimientos cual fue la merjor inversion
historicoMerval['Date'] = pd.to_datetime(historicoMerval['Date'])
historicoMEP['Date'] = pd.to_datetime(historicoMEP['Date'])

# Obtener las columnas de cierre del Merval
columnas_merval = [col for col in historicoMerval.columns if col.endswith('.BA Close')]
merval_cierres = historicoMerval[columnas_merval]

# Calcular los rendimientos diarios de cada acción del Merval
merval_returns = merval_cierres.pct_change()

# Calcular los rendimientos acumulados de cada acción del Merval
merval_cumulative_returns = (1 + merval_returns).cumprod() - 1

# Calcular el rendimiento total promedio de las acciones del Merval al final del período
merval_total_return = merval_cumulative_returns.iloc[-1].mean()

# Calcular el rendimiento del dólar MEP
mep_returns = historicoMEP['Precio'].pct_change()
mep_cumulative_returns = (1 + mep_returns).cumprod() - 1
mep_total_return = mep_cumulative_returns.iloc[-1]

# Comparar los rendimientos
if merval_total_return > mep_total_return:
    mejor_inversion = 'Acciones del Merval'
    mejor_retorno = merval_total_return
else:
    mejor_inversion = 'Dólar MEP'
    mejor_retorno = mep_total_return

# Visualizar los rendimientos acumulados de las acciones del Merval
plt.plot(historicoMerval['Date'], merval_cumulative_returns)
plt.xlabel('Fecha')
plt.ylabel('Rendimiento acumulado')
plt.title('Rendimiento acumulado: Acciones del Merval')
plt.show()

print(f"La mejor inversión desde 1 de enero 2020 hasta el 25 de junio 2023 fue: {mejor_inversion}")
print(f"Rendimiento acumulado: {mejor_retorno:.2%}")
