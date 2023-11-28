import csv
import sys
import os
import pandas as pd


def rutas(ruta):
    try:
        rutabase = sys.__MEIPASS
    except Exception:
        rutabase = os.path.abspath(".")
    return os.path.join(rutabase, ruta)
def cargar_datos():

    with open("datos/27 nov 2023.csv", 'r') as f:
        dialect = csv.Sniffer().sniff(f.read())
    df = pd.read_csv("datos/27 nov 2023.csv", delimiter=dialect.delimiter, skiprows=1)
    df.columns = ['columna 1', 'pH bocatoma (ph)', 'pH salida (pH)', 'Turbiedad (NTU)', 'Cloro residual (PPM)',
                  'QE1 (L/s)', 'QE2 (L/s)',
                  'QS1 (L/s)', 'QS2 (L/s)', 'Sensor de nivel (m)']

    # Ahora puedes dividir la primera columna (que ahora se llama 'columna1')
    df[['Fecha', 'Hora']] = df['columna 1'].str.split(' ', expand=True)

    # eliminar la columna original
    df = df.drop(columns=['columna 1'])

    dfnuevo = df.iloc[:, :-2]
    dfnuevo = dfnuevo.apply(pd.to_numeric)
    dfnuevo = dfnuevo / 100
    dfnuevo['Sensor de nivel (m)'] = dfnuevo['Sensor de nivel (m)'] / 10
    dfnuevo['Sensor de nivel (m)'] = dfnuevo['Sensor de nivel (m)'].round(3)

    df[dfnuevo.columns] = dfnuevo

    # Reordena las columnas para que 'fecha' y 'hora' sean las dos primeras
    df = df[['Fecha', 'Hora'] + [c for c in df.columns if c not in ['Fecha', 'Hora']]]

    # Convierte la fecha al formato deseado
    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.strftime('%Y-%m-%d')
    df['Fecha'] = df['Fecha'].astype(str)

    # Asegúrate de que la hora esté en el formato correcto
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.time
    df['Hora'] = df['Hora'].astype(str)

    df['QTE (L/s)'] = df['QE1 (L/s)'] + df['QE2 (L/s)']
    df['QTE (L/s)'] = df['QTE (L/s)'].round(2)
    df['QTS (L/s)'] = df['QS1 (L/s)'] + df['QS2 (L/s)']
    df['QTS (L/s)'] = df['QTS (L/s)'].round(2)
    # Agrega una nueva columna que es la suma del dato actual y el dato anterior en 'Macro 1+2'
    df['V horario E'] = df['QTE (L/s)'] + df['QTE (L/s)'].shift(1)
    df['V horario E'] = df['V horario E'].fillna(df['QTE (L/s)'] * 7200 / 1000)

    # Agrega una nueva columna que es la suma del dato actual y el dato anterior en 'Macro 3+4'
    df['V horario S'] = df['QTS (L/s)'] + df['QTS (L/s)'].shift(1)
    df['V horario S'] = df['V horario S'].fillna(df['QTS (L/s)'] * 7200 / 1000)

    # Multiplica todas las filas excepto la primera por 3,6 en 'Macro 1+2 acumulado'
    df.loc[1:, 'V horario E'] *= 3.6
    df['V horario E'] = df['V horario E'].round(2)

    # Multiplica todas las filas excepto la primera por 3,6 en 'Macro 3+4 acumulado'
    df.loc[1:, 'V horario S'] *= 3.6
    df['V horario S'] = df['V horario S'].round(2)

    # Crea una nueva columna que es la suma del dato de la fila anterior y la resta de 'Macro 1+2 acumulado' y 'Macro 3+4 acumulado'
    df['V regulacion'] = df['V horario E'] - df['V horario S']
    df['V real'] = df['V regulacion']
    df['V regulacion'] = df['V regulacion'].shift(1) + df['V regulacion']
    df['V regulacion'] = df['V regulacion'].fillna(0)
    df['V regulacion'] = df['V regulacion'].round(2)
    df['V real'] = df['V real'].shift(1) + df['V real']
    df['V real'] = df['V real'].fillna(0)
    df['V real'] = df['V real'].round(2)

    return df
