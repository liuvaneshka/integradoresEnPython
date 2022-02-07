"""
    El programa deberá tener un menú poder cumplir lo siguiente:
    1. Procesar información de entrada
    2. Determinar la marca que mayor $ vendió
    3. Reporte de cantidades de artículos (artículo y cantidad) vendidos por año, ordenado por
    año ascendente y por cantidad descendente.
    4. Importe $ promedio por operación y cuantas operaciones estuvieron por encima de
    dicho promedio
    5. Para un determinado año y marca indicar en qué % del total de operaciones participó
    dicha marca.
"""

import codecs
import csv
import os


def lectura_ventas(archivo: str) -> dict:
    """
        Precondicion: nombre-archivo, es una varible tipo cadena, str, excata al nombre del archivo a leer
        Postcondicion: Abre y lee el archivo, crean una lista con las lineas del archivo, arma el diccionario pedidos
                    agrega sus respectivas claves {'Cliente':cadena, 'fecha':cadena}

    """
    datos = list()
    ventas: dict = {}

    with codecs.open(os.path.dirname(os.path.abspath(__file__)) + '/' + archivo, "r", encoding='utf-8',
                     errors='ignore') as f:
        lector = csv.reader(f, delimiter=';', quotechar='|')
        next(lector)
        for row in lector:
            datos.append(row)

    for dato in datos:

        if dato[0] not in ventas:
            ventas[int(dato[0])] = {'Cliente': dato[1], 'AAAAMMDD': dato[2]}
    """ 
    print('ventas: ')
    print(ventas)
    """

    return ventas


def leer_detalles(archivo: str) -> dict:
    """
        Precondicion: nombre-archivo, es una varible tipo cadena, str, excata al nombre del archivo a leer
        Postcondicion: Abre y lee el archivo, crean una lista con las lineas del archivo, arma el diccionario pedidos
                    agrega sus respectivas claves {'Cliente':cadena, 'fecha':cadena}

    """
    datos = list()
    detalles: dict = {}

    with codecs.open(os.path.dirname(os.path.abspath(__file__)) + '/' + archivo, "r", encoding='utf-8',
                     errors='ignore') as f:
        lector = csv.reader(f, delimiter=';', quotechar='|')
        next(lector)
        for row in lector:
            datos.append(row)

    for dato in datos:

        if int(dato[0]) not in detalles:
            detalles[int(dato[0])] = {'Articulo': {int(dato[1]): {'Cantidad': int(dato[2]), 'Importe': int(dato[3])}}}
        elif int(dato[1]) in detalles[int(dato[0])]['Articulo']:
            detalles[int(dato[0])]['Articulo'][int(dato[1])] = {'Cantidad': int(dato[2]), 'Importe': int(dato[3])}
        else:
            detalles[int(dato[0])]['Articulo'][int(dato[1])] = {'Cantidad': int(dato[2]), 'Importe': int(dato[3])}
    """
    print('detalles')
    for i in detalles:
        print(i, detalles[i])
    print('detalles: ')
    print(detalles)
    """

    return detalles


def leer_marcas(archivo: str) -> dict:
    """
        Precondicion: nombre-archivo, es una varible tipo cadena, str, excata al nombre del archivo a leer
        Postcondicion: Abre y lee el archivo, crean una lista con las lineas del archivo, arma el diccionario pedidos
                    agrega sus respectivas claves {'Cliente':cadena, 'fecha':cadena}

    """
    datos = list()
    marcas: dict = {}

    with codecs.open(os.path.dirname(os.path.abspath(__file__)) + '/' + archivo, "r", encoding='utf-8',
                     errors='ignore') as f:
        lector = csv.reader(f, delimiter=';', quotechar='|')
        next(lector)
        for row in lector:
            datos.append(row)

    for dato in datos:

        if int(dato[0]) not in marcas:
            marcas[int(dato[0])] = {'Nombre': dato[1], 'Marca': dato[2]}
    """ 
    print('marcas:  ')
    print(marcas)
    """
    return marcas


def determinar_galleta_mas_vendida(detalles: dict, marcas: dict) -> str:
    ventas_por_marca: dict = {}
    maximo: int = 0
    nro_articulo: int = 0
    nombre: str = ' '

    for operacion in detalles:
        # print(detalles[operacion]['Articulo'])
        articulos = detalles[operacion]['Articulo']

        for articulo in articulos:

            # print(detalles[operacion]['Articulo'][art]['Importe'])
            cantidad = articulos[articulo]['Cantidad']

            if articulo in ventas_por_marca:
                ventas_por_marca[articulo] += cantidad
            else:
                ventas_por_marca[articulo] = int(cantidad)

    for i in ventas_por_marca:

        max_tmp = ventas_por_marca[i]
        if max_tmp >= maximo:
            maximo = max_tmp
            nro_articulo = i

    for i in marcas:
        if nro_articulo == i:
            nombre = marcas[i]['Nombre']

    """
    print('maximo:',maximo)
    print('articulo: ',nro_articulo)
    print('nombre: ',nombre)
    print(ventas_por_marca)
    """

    return nombre


def determinar_marca_millonaria(detalles: dict, marcas: dict) -> str:
    marca_millonaria: str = ' '
    marca_millio: dict = {}
    temp: dict = {}
    plata: int = 0
    maximo: int = 0

    for operacion in detalles:
        articulos = detalles[operacion]['Articulo']

        for articulo in articulos:
            # print('art:',articulo)
            importe = articulos[articulo]['Importe']
            # print('impo:',importe)

            if articulo not in temp:
                temp[articulo] = importe

            else:
                temp[articulo] += importe

    for marca in marcas:
        # print(marcas[marca]['Marca'])
        llave = marcas[marca]['Marca']
        id = marca
        # print(id)
        if llave not in marca_millio:

            if id in temp:
                # print('importe:', temp[id])
                plata = temp[id]
                marca_millio[llave] = plata
            else:
                marca_millio[llave] += plata

        else:
            if id in temp:
                # print('importe:', temp[id])
                plata = temp[id]
                marca_millio[llave] += plata
            else:
                marca_millio[llave] += plata

    # print(marca_millio)
    # print(temp)

    for i in marca_millio:
        max_tmp = marca_millio[i]
        if max_tmp >= maximo:
            maximo = max_tmp
            marca_millonaria = i

    return marca_millonaria


def reporte(ventas: dict, detalles: dict, marcas: dict):
    anio = ' '
    articulos = {}
    for v in ventas:

        for d in detalles[v]:
            # print(detalles[v][d])
            operacion = detalles[v][d]

            for op in operacion:
                fecha = ventas[v]['AAAAMMDD']
                anio = fecha[0:4:]
                # print(anio)
                articulo = op
                cantidad = operacion[op]['Cantidad']

                if articulo not in articulos:

                    articulos[articulo] = {'Anio': {anio: {'Cantidad': cantidad}}}

                else:
                    articulos[articulo]['Anio'][anio] = {'Cantidad': cantidad}

    # print('articulos')
    # print(articulos)
    for i in articulos:
        dic = articulos[i]['Anio']
        sdic = sorted(dic.items(), reverse=True)

        print(marcas[i]['Nombre'], sdic)

    """
    #sorted(dic,key=lambda key: dic[key])

    lista =[]
    lista.sort(key=lambda x: x[1]['Anio'], reverse=False)
    print(lista)
    print(informados)
    
    #sorted(dic,key=dic.get)

    """

    """
     nombres_cursos_ordenados: list = []
     for curso in cursos:
         nombres_cursos_ordenados.append(cursos[curso][0])
         diccionario[cursos[curso][0]] = cursos[curso][3]
     nombres_cursos_ordenados.sort()
     for i in nombres_cursos_ordenados:
         print(i)
         for x in diccionario[i]:
             print(x)
    """


def importe_promedio(detalles: dict):
    dic_importes = {}

    for i in detalles:
        suma = 0
        contador = 0
        operacion = detalles[i]
        for j in operacion:
            articulo = operacion[j]
            for k in articulo:
                importe = articulo[k]['Importe']
                suma += importe
                contador += 1

        promedio_operacion = suma / contador
        dic_importes[i] = promedio_operacion

    # print(dic_importes)

    suma = 0
    promedio = 0
    ct = 0

    for key in dic_importes:
        suma += dic_importes[key]
        ct += 1
    promedio = suma / ct
    # print('suma,can,prom',suma,ct,promedio)

    encima_promedio = 0

    for key in dic_importes:
        print("la operacion y su promedio ", key, dic_importes[key])
        if dic_importes[key] >= promedio:
            encima_promedio += 1
    print('la cantidad de op mayor al promedio : ', encima_promedio)
    print('promedio op: ', promedio)


def porcentaje(ventas: dict, detalles: dict, marcas: dict):
    for nro_operacion in ventas:
        contador = 0
        fecha = ventas[nro_operacion]['AAAAMMDD']
        anio = fecha[0:4:]

    for no in detalles:
        no_det = detalles[no]
        print(no_det)


def main():
    marcas: dict = {}
    ventas: dict = {}
    detalles: dict = {}

    ventas = lectura_ventas('ventas.csv')
    detalles = leer_detalles('detalles.csv')
    marcas = leer_marcas('marcas.csv')

    galleta_mas_vendida: str = ' '
    marca_produce_mas_dinero: str = ' '

    opciones: list = ["Galleta mas vendida", "Determinar la marca que mayor $ vendió ",
                      "Reporte de cantidades de artículos (artículo y cantidad) vendidos por año, ordenado por año "
                      "ascendente y por cantidad descendente.",
                      "Importe $ promedio por operación y cuantas operaciones estuvieron por encima de dicho promedio ",
                      "Para un determinado año y marca indicar en qué % del total de operaciones participacion de "
                      "dicha marca ",
                      "Salir"]
    opcion: str = ''

    while opcion != '6':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            galleta_mas_vendida = determinar_galleta_mas_vendida(detalles, marcas)

            print('La galleta mas vendida es: ', galleta_mas_vendida)

        elif opcion == '2':

            if len(ventas) != 0:

                marca_produce_mas_dinero = determinar_marca_millonaria(detalles, marcas)

                print('La marca millonaria es: ', marca_produce_mas_dinero)

            else:

                print('el diccionario esta vacio')

        elif opcion == '3':

            if len(ventas) != 0:

                reporte(ventas, detalles, marcas)

            else:

                print('el diccionario esta vacio')

        elif opcion == '4':

            if len(ventas) != 0:

                importe_promedio(detalles)

            else:

                print('el diccionario esta vacio')

        elif opcion == '5':

            if len(ventas) != 0:

                porcentaje(ventas, detalles, marcas)

                print('opcion 5')

            else:

                print('el diccionario esta vacio')

        elif opcion == '6':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 6")


main()
