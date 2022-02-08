import csv
from datetime import datetime


# from operator import itemgetter


def leer_pedidos(archivo: str):
    datos = list()
    pedidos: dict = {}

    try:
        pedidos_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay pedidos cargados')
        with open(archivo, 'a') as pedidos_csv:
            pedidos_csv.write('id_pedido, descripción_del_pedido, costo_del_pedido, cantidad de items, '
                              'categoría_del_pedido, mes, año\n')

    else:
        lector = csv.reader(pedidos_csv, delimiter=',')
        next(lector)
        for row in lector:
            datos.append(row)

        for dato in datos:

            if int(dato[0]) not in pedidos:
                pedidos[int(dato[0])] = {'Descripcion': dato[1], 'Costo': int(dato[2]), 'Cantidad': int(dato[3]),
                                         'Categoria': dato[4], 'Mes': int(dato[5]), 'Año': int(dato[6])}

        pedidos_csv.close()

    return pedidos


def validar_numero(numero: str) -> bool:
    numero_validado: bool = False

    if not numero.isnumeric():
        numero_validado = True

    return numero_validado


def ingresar_pedidos(pedidos: dict) -> dict:
    numeros = list(map(int, pedidos.keys()))
    if len(numeros) > 0:
        numeros.sort()
        numero_pedido: int = int(numeros[-1]) + 1
    else:
        numero_pedido = 1

    descripcion: str = input('Ingrese descripcion: ')
    costo: str = input('Ingrese costo: ')
    while validar_numero(costo):
        print("no ingresaste un numero entero positivo: ")
        costo = input("Ingrese otro costo: ")
    cantidad: str = input('Ingrese cantidad: ')
    while validar_numero(cantidad):
        print("no ingresaste un numero entero positivo: ")
        cantidad = input("Ingrese otra cantidad: ")
    categoria: str = input('Ingrese categoria: ')
    categoria = categoria[0:2:]
    categoria = categoria.upper()
    mes: str = datetime.today().strftime('%#m')
    anio: str = datetime.today().strftime('%Y')

    print(mes, anio)

    with open("pedidos.csv", "a") as archivo:

        archivo.write(
            str(numero_pedido) + ', ' + descripcion + ', ' + costo + ', ' + cantidad + ', ' + categoria + ', ' + str(
                mes) + ', ' + str(anio) + '\n')

    pedidos[numero_pedido] = {'Descripcion': descripcion, 'Cantidad': cantidad, 'Categoria': categoria, 'Mes': mes,
                              'Año': anio}

    return pedidos


def mostrar_por_annio_mes(pedidos: dict) -> None:
    suma: int = 0
    cantidad_pedidos: int = 0
    lista_m: list = []
    anio: str = input('Ingrese anio: ')
    while validar_numero(anio):
        print("no ingresaste un numero entero positivo: ")
        anio = input("Ingrese otro costo: ")
    for i in pedidos:

        annio = pedidos[i]['Año']

        if annio == int(anio):
            mes = pedidos[i]['Mes']

            lista_m.append(mes)

    print(lista_m)

    if len(lista_m) > 0:

        mes: int = int(input('Ingrese mes valido: '))

        while mes not in lista_m:
            print('noingresaste u mes valido')
            mes: int = int(input('Ingrese mes valido: '))

        for d in pedidos:
            m = int(pedidos[d]['Mes'])
            a = int(pedidos[d]['Año'])
            c = int(pedidos[d]['Costo'])
            if (m == int(mes)) and (a == int(anio)):
                print(pedidos[d])
                cantidad_pedidos += 1
                suma += c

        print('cqantidad de pedidos: ', cantidad_pedidos)
        print('costo toal: ', suma)

    else:

        print('no hay pedidos con ese annio')


def imprimir_pedidos_ordenados_anio_mes(pedidos: dict):
    # Año

    lista_pedidos: list = []

    for i in pedidos:
        pedido = pedidos[i]
        lista_pedidos.append(pedido)

    lista_pedidos.sort(key=lambda p: p['Año'], reverse=False)

    lista_pedidos.sort(key=lambda p: p['Mes'], reverse=False)

    for linea in lista_pedidos:
        print(linea)


def organizar_categoria(pedidos: dict):
    categorias: dict = {}
    lista_categorias: list = []

    for i in pedidos:
        categoria = pedidos[i]['Categoria']
        costo = pedidos[i]['Costo']
        cantidad = pedidos[i]['Cantidad']

        costo_promedio = costo / cantidad

        categorias[i] = {'Categoria': categoria, 'Costo promedio POR ITEM': costo_promedio}

    for i in categorias:
        lista_categorias.append(categorias[i])

        lista_categorias.sort(key=lambda p: p['Categoria'], reverse=False)

    for linea in lista_categorias:
        print(linea)


def main():
    pedidos = leer_pedidos('pedidos.csv')
    # print(pedidos)

    opciones: list = ["Poder agregar pedidos en el sistema y que queden almacenados",
                      "Mostrar en pantalla la cantidad de pedidos y el costo total de un mes y año en particular ",
                      "Imprimir en pantalla todos los pedidos ordenados de forma ascendente por año y mes, indicando "
                      "Id, "
                      "descripcion del pedido, costo total y costo promedio por item. ",
                      "Mostrar las categorías ordenadas descendentemente por costo promedio por item indicando "
                      "categoría "
                      "y costo promedio por item ",
                      "Salir"]
    opcion: str = ''

    while opcion != '5':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            pedidos = ingresar_pedidos(pedidos)

        elif opcion == '2':

            if len(pedidos) != 0:

                mostrar_por_annio_mes(pedidos)

            else:

                print('pedidos esta vacio')

        elif opcion == '3':

            if len(pedidos) != 0:

                imprimir_pedidos_ordenados_anio_mes(pedidos)

            else:

                print('pedidos esta vacio')

        elif opcion == '4':

            if len(pedidos) != 0:

                organizar_categoria(pedidos)

            else:

                print('pedidos esta vacio')

        elif opcion == '5':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 7")


main()
