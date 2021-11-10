import csv, io, os, datetime, pdb #holidays
import pandas as pd
from energia.ext.EdistribucionAPI import Edistribucion
from itertools import chain

def parseCSV(file):
    # es_holidays=holidays.Spain()
    consumoValle = 0
    consumoLlano = 0
    consumoPunta = 0
    numFilas = 0
    fechaMin = datetime.datetime.max
    fechaMax = datetime.datetime.min

    file = file.read().decode('utf-8')
    reader = csv.DictReader(io.StringIO(file), delimiter=";")
    data = [line for line in reader]

    # print(header)
    for row in data:
        numFilas += 1
        dia = datetime.datetime.strptime(row['Fecha'],"%d/%m/%Y")
        horaFin = int(row['Hora']) # Indica la hora fin
        consumo = float(row['AE_kWh'].replace(',','.'))
        if dia.weekday() > 4 or horaFin <= 8:
            consumoValle += consumo
        elif 8 < horaFin <= 10 or 14 < horaFin <= 18 or horaFin > 22:
            consumoLlano += consumo
        else:
            consumoPunta += consumo
        if dia < fechaMin:
            fechaMin = dia
        if dia > fechaMax:
            fechaMax = dia
    
    return {
        'consumoValle': consumoValle,
        'consumoLlano': consumoLlano,
        'consumoPunta': consumoPunta,
        'consumoTotal': consumoValle + consumoLlano + consumoPunta,
        'consumoMedio': (consumoValle + consumoLlano + consumoPunta) / (fechaMax - fechaMin).days,
        'numFilas': numFilas,
        'fechaMin': fechaMin,
        'fechaMax': fechaMax,
        'numDias': fechaMax - fechaMin,
        }

    print("Consumo Valle: {:.2f}".format(consumoValle))
    print("Consumo Llano: {:.2f}".format(consumoLlano))
    print("Consumo Punta: {:.2f}".format(consumoPunta))
    print("Consumo Total: {:.2f}".format(consumoValle+consumoLlano+consumoPunta))
    print("Número de filas procesadas: {}".format(numFilas))

def getConsumo(data):
    user = data['user']
    password = data['password']
    consulta = data['consulta']
    edis = Edistribucion(user, password)
    edis.login()
    conts = edis.get_list_cups()
    # consumo = edis.get_consumo_byRange(conts[1])
    if consulta == '1':
        consumo = edis.get_consumo(conts[0])
    elif consulta == '2':
        consumo = edis.get_consumo_lastWeek(conts[0])
    elif consulta == '3':
        consumo = edis.get_consumo_lastMonth(conts[0])
    else:
        raise Exception('Consulta incorrecta')
    # Pandas DataFrame from list of lists of dicts: https://stackoverflow.com/a/42304698/1390555
    df = pd.DataFrame(list(chain.from_iterable(consumo)))
    if 'a2' in df:
        return df[['date', 'hourCCH', 'a2', 'value']].to_html()
    return df[['date', 'hourCCH', 'value']].to_html()
    #return consumo