"""
    1) Informar el promedio de temperatura de cada sector.
    2) Determinar el sector con mayor temperatura y el sector con menor temperatura.
    3) Informar la hora de mayor y menor temperatura de cada sector.
    4) Crear el archivo de seguridad respetando el formato requerido.
    5) Informar cuantos tubos deben revisarse.
    6) Informar el sector mas problemático (mayor numero de tubos a revisarse).
"""
import codecs
import csv
import os


def leer_temperaturas(archivo: str) -> dict:
    datos = list()
    temperaturas: dict = {}
    linea = 0

    with codecs.open(os.path.dirname(os.path.abspath(__file__)) + '/' + archivo, "r", encoding='utf-8',
                     errors='ignore') as f:
        lector = csv.reader(f, delimiter=';', quotechar='|')
        # next(lector)  NO TIENE ENCABEZADO
        for row in lector:
            datos.append(row)
    for dato in datos:
        temperaturas[linea] = {'Sector': dato[0], 'Tubo': int(dato[1]), 'Hora': dato[2], 'Temperatura': int(dato[3])}
        linea += 1

    # print('temperaturas: ')
    # print(temperaturas)

    return temperaturas


def leer_seguridad(archivo: str) -> list:
    datos = list()
    seguridad: list = []

    try:
        seguridad_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay seguridad cargados')

    else:
        lector = csv.reader(seguridad_csv, delimiter=';')
        for row in lector:
            datos.append(row)

        for dato in datos:
            segu = [int(dato[0]), dato[1]]
            seguridad.append(segu)

        seguridad_csv.close()

    return seguridad


def promedio_por_sector(temperaturas: dict) -> float:
    suma: int = 0
    contador: int = 0
    for i in temperaturas:
        temperatura = temperaturas[i]['Temperatura']
        suma += temperatura
        contador += 1
    # print(suma, contador)
    promedio = suma / contador

    return promedio


def temperaturas_max_min(temperaturas: dict):
    temperatura_max = 0
    temperatura_min = 0
    sector_max = ' '
    sector_min = ' '

    for i in temperaturas:
        temperatura = temperaturas[i]['Temperatura']
        sector = temperaturas[i]['Sector']

        if temperatura > temperatura_max:
            temperatura_max = temperatura
            sector_max = sector

        if temperatura < temperatura_max:
            temperatura_min = temperatura
            sector_min = sector
            print(temperatura_min)

    print('Temperatura maxima: ', temperatura_max)
    print('Temperatura minima: ', temperatura_min)
    print('sec maxima: ', sector_min)
    print('sec minima: ', sector_max)


def horas_max_min(temperaturas: dict):
    sectores: dict = {}

    for i in temperaturas:

        sector = temperaturas[i]['Sector']
        temperatura = temperaturas[i]['Temperatura']
        hora = temperaturas[i]['Hora']

        valores = []
        valor = [temperatura, hora]

        if sector not in sectores:
            sectores[sector] = valores
            sectores[sector].append(valor)
        else:
            sectores[sector].append(valor)

    t_max = 0
    t_min = 0
    h_max = ' '
    h_min = ' '

    for sec in sectores:
        values = sectores[sec]
        print(sec)
        for t in values:
            temperatura = int(t[0])
            hora = t[1]
            if temperatura > t_max:
                t_max = temperatura
                h_max = hora

            if temperatura < t_max:
                t_min = temperatura
                h_min = hora

        print("min", t_min, h_min)
        print("max", t_max, h_max)

    # print(sectores)


def ingresar_archivo_seguridad(temperaturas: dict, seguridad: list) -> int:
    lista: list = []
    datos: list = []
    revisar: int = 0

    for i in temperaturas:
        temp = temperaturas[i]['Temperatura']
        tubo = temperaturas[i]['Tubo']
        sector = temperaturas[i]['Sector']
        s = sector[0:1:]
        st = s + str(tubo)

        if temp >= 396 or temp <= 385:
            datos = [temp, st]
            lista.append(datos)

    # print(lista)
    ordenada = sorted(lista, key=lambda x: x[0], reverse=True)
    # print(ordenada)
    s = open("seguridad.csv", "a")
    s.truncate(0)
    contador = 0
    for i in ordenada:
        print(i)
        with open("seguridad.csv", "a") as archivo:
            archivo.write(str(i[0]) + ';' + i[1] + '\n')
        contador += 1
    revisar = contador

    return revisar


def sector_problematico(temperaturas: dict):
    problematicos: dict = {}

    for i in temperaturas:
        sector = temperaturas[i]['Sector']
        temperatura = temperaturas[i]['Temperatura']
        tubo = 1

        if temperatura >= 396 or temperatura <= 385:

            if sector in problematicos:
                problematicos[sector] += tubo

            else:
                problematicos[sector] = tubo

    print(problematicos)
    p = 1
    lista_p = []
    sector_p = ''

    for i in problematicos:
        problemas = problematicos[i]

        if problemas >= p:
            p = problemas
            sector_p = i
            lista_p.append(sector_p)

    print('sector mas problematico: ', sector_p)
    print('problematicos', lista_p)
    new_maximum_val = max(problematicos.keys(), key=(lambda new_k: problematicos[new_k]))
    print('Maximum Value: ', problematicos[new_maximum_val])
    new_minimum_val = min(problematicos.keys(), key=(lambda new_k: problematicos[new_k]))
    print('Minimum Value: ', problematicos[new_minimum_val])


def main():
    temperaturas = leer_temperaturas('temperaturas.csv')
    seguridad = leer_seguridad('seguridad.csv')
    revisar: int = 0

    opciones: list = ["Informar el promedio de temperatura de cada sector",
                      "Determinar el sector con mayor temperatura y el sector con menor temperatura ",
                      "Informar la hora de mayor y menor temperatura de cada sector ",
                      "Crear el archivo de seguridad respetando el formato requerido ",
                      "Informar cuantos tubos deben revisarse",
                      "Informar el sector mas problemático (mayor numero de tubos a revisarse)",
                      "Salir"]
    opcion: str = ''

    while opcion != '7':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            promedio = promedio_por_sector(temperaturas)
            print('El promedio de temperaturas es: ', promedio)

        elif opcion == '2':

            if len(temperaturas) != 0:

                temperaturas_max_min(temperaturas)

            else:

                print('el diccionario esta vacio')

        elif opcion == '3':

            if len(temperaturas) != 0:

                horas_max_min(temperaturas)

            else:

                print('el diccionario esta vacio')

        elif opcion == '4':

            if len(temperaturas) != 0:

                revisar = ingresar_archivo_seguridad(temperaturas, seguridad)
                print('opcion 4')

            else:

                print('el diccionario esta vacio')

        elif opcion == '5':

            if len(temperaturas) != 0:

                print('Tubos a revisar', revisar)

            else:

                print('el diccionario esta vacio')

        elif opcion == '6':

            if len(temperaturas) != 0:

                sector_problematico(temperaturas)
                print('opcion 6')

            else:

                print('el diccionario esta vacio')

        elif opcion == '7':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 7")


main()
