import csv
import datetime


def leer_pedidos(archivo: str) -> dict:
    datos = list()
    diccionario: dict = {}

    # abre el archivo, al no tener datos cargados hace una exepcion para crear el diccionario
    try:
        diccionario_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay datos cargados')
        with open(archivo, 'a') as diccionario_csv:
            diccionario_csv.write('id_pedido, descripción_del_pedido, costo_del_pedido, cantidad de items, '
                                  'categoría_del_pedido, mes, año \n')

    else:
        lector = csv.reader(diccionario_csv, delimiter=',')
        next(lector)
        for row in lector:
            datos.append(row)

        for dato in datos:
            if dato[0] not in diccionario:
                diccionario[int(dato[0])] = {'descripcion': dato[1], 'costo': int(dato[2]), 'cantidad': int(dato[3]),
                                             'categoria': dato[4], 'mes': dato[5], 'anio': dato[6]}

        diccionario_csv.close()

    return diccionario


def validar_fecha(fecha: str) -> bool:
    formato = "%Y"
    # fecha_valida = None
    # intento con formato valido para retornar verdadero, sino se cumple
    # hace una excepcion para retornar falso y arrojar un aviso
    try:
        datetime.datetime.strptime(fecha, formato)
        fecha_valida = True
    except ValueError:
        fecha_valida = False
        print("Formato invalido debe ser dd/mm/aaaa")

    return fecha_valida


def crear_codigo(pedidos: dict) -> int:
    numeros = list(map(int, pedidos.keys()))
    if len(numeros) > 0:
        numeros.sort()
        numero_pedido: int = int(numeros[-1]) + 1
    else:
        numero_pedido = 1

    return numero_pedido


def entrada_operaciones(pedidos: dict) -> dict:
    categorias: list = ['AL', 'ME', 'FE']
    idp: int = crear_codigo(pedidos)

    descripcion: str = input('Descripcion: ')
    costo: str = input('Ingrese costo: ')
    while not costo.isnumeric():
        print("no ingresaste un numero entero: ")
        costo = input("Ingrese nuevamente costo: ")
    cantidad: str = input('Ingrese cantidad de items: ')
    while not cantidad.isnumeric():
        print("no ingresaste un numero entero: ")
        cantidad = input("Ingrese nuevamente cantidad: ")
    print("categorias: \n")
    for i in categorias:
        print(i)
    categoria: str = input('Categoria: ')
    categoria = categoria.upper()
    while categoria not in categorias:
        categoria: str = input('Categoria: ')
        categoria = categoria.upper()
    mes: str = input('Ingrese mes: ')
    while 0 >= int(mes) > 12:
        mes: str = input("Ingrese mes valido : ")
    anio: str = input('Ingrese anio: ')
    while not validar_fecha(anio):
        anio: str = input("yyyy: ")

    with open("pedidos.csv", "a") as archivo:
        archivo.write(str(idp) + ', ' + descripcion + ', ' + str(costo) + ', ' + str(cantidad) + ', ' + categoria +
                      ', ' + mes + ', ' + anio + '\n')

    pedidos[int(idp)] = {'descripcion': descripcion, 'costo': int(costo), 'cantidad': int(cantidad),
                         'categoria': categoria, 'mes': mes, 'anio': anio}
    print(pedidos)

    return pedidos


def mostrar_cantidad_costo_pedidos_mes_anio(pedidos: dict) -> None:

    # pedidos_mes: dict = {}
    cantidad_pedidos: int = 0
    costo_total: int = 0

    mes_ingresado: str = input('Ingrese mes: ')
    while 0 >= int(mes_ingresado) > 12:
        mes_ingresado: str = input("Ingrese mes valido : ")
    anio_ingresado: str = input('Ingrese anio: ')
    while not validar_fecha(anio_ingresado):
        anio_ingresado: str = input("yyyy: ")

    for pedido in pedidos:

        mes = pedidos[pedido]['mes']
        mes = mes[1:]
        anio = pedidos[pedido]['anio']
        anio = anio[1:]
        costo = pedidos[pedido]['costo']

        if mes_ingresado == mes and anio_ingresado == anio:

            cantidad_pedidos += 1
            costo_total += costo

    print(anio_ingresado, mes_ingresado, cantidad_pedidos, costo_total)


def ordenar_pedidos(pedidos: dict) -> None:

    lista: list = []
    # promedio: float = 0.0

    for clave in pedidos:
        contenido = pedidos[clave]
        cantidad = pedidos[clave]['cantidad']
        costo = pedidos[clave]['costo']
        promedio = costo / cantidad
        contenido['clave'] = clave
        contenido['promedio'] = promedio
        lista.append(contenido)

    lista.sort(key=lambda p: p['mes'], reverse=False)

    lista.sort(key=lambda p: p['anio'], reverse=False)

    for linea in lista:
        print(linea)


def mostrar_categorias_ordenadas(pedidos: dict) -> None:

    categorias: dict = {}

    for clave in pedidos:

        categoria = pedidos[clave]['categoria']
        cantidad = pedidos[clave]['cantidad']
        costo = pedidos[clave]['costo']
        promedio = costo / cantidad

        if categoria not in categorias:
            categorias[categoria] = promedio
        elif categoria in categorias:
            promedio_anterior = categorias[categoria]
            promedio = promedio + promedio_anterior
            categorias[categoria] = promedio
        # print(categorias)

    categorias_items = categorias.items()

    items_ordenados = sorted(categorias_items)

    # print(items_ordenados)
    print("categorida:   suma de promedios:")

    for i in items_ordenados:
        print(i)


def main():
    pedidos = leer_pedidos('pedidos.csv')
    print(pedidos)

    opciones: list = ["Poder agregar pedidos en el sistema y que queden almacenados ",
                      "Mostrar en pantalla la cantidad de pedidos y el costo total de un mes y año en particular ",
                      "Imprimir en pantalla todos los pedidos ordenados de forma ascendente por año y mes, indicando"
                      "ID, descripcion del pedido, costo total y costo promedio por item",
                      "Mostrar las categorías ordenadas descendentemente por costo promedio por item indicando"
                      " categoría y costo promedio por item.",
                      "Salir"]
    opcion: str = ''

    while opcion != '5':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            pedidos = entrada_operaciones(pedidos)

        elif opcion == '2':

            if len(pedidos) != 0:

                mostrar_cantidad_costo_pedidos_mes_anio(pedidos)

            else:

                print('el diccionario esta vacio')

        elif opcion == '3':

            if len(pedidos) != 0:

                ordenar_pedidos(pedidos)

            else:

                print('el diccionario esta vacio')

        elif opcion == '4':

            if len(pedidos) != 0:

                mostrar_categorias_ordenadas(pedidos)

            else:

                print('el diccionario esta vacio')

        elif opcion == '5':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 5")


main()
