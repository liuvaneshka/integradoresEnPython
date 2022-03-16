import csv
import operator


def leer_articulos(archivo: str) -> list:
    datos = list()
    lista: list = []

    # abre el archivo, al no tener datos hace una excepcion para crear una lista
    try:
        lista_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay datos cargados')

    else:
        lector = csv.reader(lista_csv, delimiter=',')

        for row in lector:
            datos.append(row)

        for dato in datos:
            segu = [dato[0], dato[1], dato[2], dato[3]]
            lista.append(segu)

        lista_csv.close()

    return lista


def leer_canjes(archivo: str) -> dict:
    datos = list()
    canjes: dict = {}

    # abre el archivo, al no tener datos hace una excepcion para crear una lista
    try:
        canjes_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay datos cargados')

    else:
        lector = csv.reader(canjes_csv, delimiter=',')

        for row in lector:
            datos.append(row)

        for dato in datos:

            if int(dato[0]) not in canjes:
                canjes[int(dato[0])] = {'puntos': dato[1], 'articulos': {dato[2]: {'cantidad': int(dato[3]),
                                                                                   'categoria': dato[4]}}}
            elif dato[2] in canjes[int(dato[0])]['articulos']:
                canjes[dato[0]]['articulos'][dato[2]] = {'cantidad': int(dato[3]), 'categoria': dato[4]}
            else:
                canjes[int(dato[0])]['articulos'][dato[2]] = {'cantidad': int(dato[3]), 'categoria': dato[4]}

            canjes_csv.close()

    return canjes


def carga_articulos(lista: list, puntos: int) -> tuple:
    nombres: list = []

    for li in lista:
        nombre = li[0]
        nombres.append(nombre)

    respuesta: str = 'si'
    articulos: dict = {}

    while respuesta == 'si':
        nombre: str = input('Ingrese el nombre: ')
        while nombre not in nombres:
            nombre: str = input('Ingrese el nombre valido: ')
            print(nombres)

        articulos[nombre] = {}
        cantidad: str = input('ingrese cantidad')
        cantidad_max: int = 0
        precio: int = 0
        for i in lista:
            if nombre == i[0]:
                cantidad_max = i[3]
                precio = i[2]
        costo = int(precio) * int(cantidad)
        while costo > puntos or cantidad > cantidad_max:
            print('INGRESO INVÁLIDO')
            if costo > puntos:
                print('no te alcanzan los puntos')
                print(puntos)
            if cantidad > cantidad_max:
                print('no hay tantos en existencia')
            cantidad: str = input('Ingrese la cantidad: ')

        categoria: str = ''
        for i in lista:
            if nombre == i[0]:
                categoria = i[1]

        puntos = puntos - int(costo)

        articulos[nombre] = {'cantidad': int(cantidad), 'categoria': categoria}
        print('Quiere agregar otro articilo?Si agrega un código que ya ingresó el nuevoingreso sobreescribirá el viejo')
        respuesta = input("Responda 'si' ó 'no': ")
        while respuesta != 'si' and respuesta != 'no':
            print('INGRESO INVÁLIDO')
            respuesta = input("Quiere agregar otro art? Responda 'si' ó 'no': ")

    return articulos, puntos


def entrada_canjes(canjes: dict, articulos: list) -> dict:
    dni: str = input('dni: ')
    puntos: int = 60000
    car: tuple = carga_articulos(articulos, puntos)
    art = car[0]
    punt = car[1]

    with open("canjes.csv", "a") as archivo:
        for nombre in art:
            cantidad: str = str(art[nombre]['cantidad'])
            categoria: str = str(art[nombre]['categoria'])
            archivo.write(
                str(dni) + ',' + str(punt) + ',' + nombre + ',' + str(cantidad) + ',' + categoria + ',' + '\n')

    canjes[dni] = {'puntos': punt, 'articulos': art}
    print("dentro de la funcion")
    for c in canjes:
        print(c, canjes[c])
    return canjes


def imprimir_canje(canjes: dict):
    dni: str = input('ingrese dni del empleado: ')
    for i in canjes:

        if int(dni) == i:
            ar = canjes[i]['articulos']
            lista_canjes = []
            for clave in ar:
                contenido = ar[clave]
                contenido['articulo'] = clave
                lista_canjes.append(contenido)

            lista_canjes.sort(key=lambda p: p['articulo'], reverse=False)
            lista_canjes.sort(key=lambda p: p['cantidad'], reverse=False)

            for linea in lista_canjes:
                print(linea)


def imprimir_stock(canjes: dict, articulos: list):
    stock: dict = {}
    stock_original: int = 0
    for i in canjes:
        ars = canjes[i]['articulos']
        for ar in ars:
            cantidad = ars[ar]['cantidad']
            cantidad = int(cantidad)
            for j in articulos:
                if ar == j[0]:
                    s = j[3]
                    s = int(s)
                    stock_original = s

            if ar not in stock:
                cantidad = stock_original - cantidad
                stock[ar] = cantidad

            elif ar in stock:
                anterior = stock[ar]
                cantidad = anterior - cantidad
                stock[ar] = cantidad

    ordenada = sorted(stock.items(), key=operator.itemgetter(1), reverse=True)
    for linea in ordenada:
        print(linea)


def crear_categorias(canjes: dict):

    categorias: dict = {}

    for i in canjes:
        print(i)
        arti = canjes[i]['articulos']

        for j in arti:
            categoria = arti[j]['categoria']
            can = arti[j]['cantidad']

            if categoria not in categorias:
                categorias[categoria] = can

            elif categoria in categorias:
                anterior = categorias[categoria]
                can = anterior + can
                categorias[categoria] = can
    print(categorias)

    s = open("categorias.csv", "a")
    s.truncate(0)

    for st in categorias:
        cate = str(st)
        canti = str(categorias[st])

        with open("categorias.csv", "a") as archivo:
            archivo.write(cate + ',' + canti + '\n')


def main():
    canjes = leer_canjes('canjes.csv')
    articulos = leer_articulos('articulos.csv')

    opciones: list = ["Permitir el ingreso de nuevos canjes.",
                      "Imprimir por pantalla el reporte de stock actual de artículos que ya fueron canjeados"
                      "ordenados por cantidad en stock descendente",
                      "Exportar al archivo categorías.csv un reporte que indique la cantidad de unidades"
                      "pedidas por categoría indicando Categoría y cantidad de artículos canjeados.",
                      "Diseñar e imprimir por pantalla un combo de artículos en base a un cierto crédito"
                      "en puntos basándose en la cantidad en que han sido canjeados los artículos "
                      "(se deben contemplar los artículos mas pedidos para sugerir el combo).",
                      "Salir"]
    opcion: str = ''

    while opcion != '5':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            canjes = entrada_canjes(canjes, articulos)
            print('canje por empleado:')
            imprimir_canje(canjes)
            print("dentro del main")
            for canje in canjes:
                print(canje, canjes[canje])

        elif opcion == '2':

            if len(canjes) != 0:

                print('stock')
                imprimir_stock(canjes, articulos)

            else:

                print('el diccionario esta vacio')

        elif opcion == '3':

            if len(canjes) != 0:

                crear_categorias(canjes)

            else:

                print('el diccionario esta vacio')

        elif opcion == '4':

            if len(canjes) != 0:

                print('opcion 4')

            else:

                print('el diccionario esta vacio')

        elif opcion == '5':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 5")


main()
