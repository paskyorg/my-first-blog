import csv, io, os, datetime, pdb #holidays

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