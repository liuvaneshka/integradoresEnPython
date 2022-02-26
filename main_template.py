import csv
import datetime


def leer_diccionario(archivo: str) -> dict:
    datos = list()
    diccionario: dict = {}

    # abre el archivo, al no tener datos cargados hace una exepcion para crear el diccionario
    try:
        diccionario_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay datos cargados')
        """
        #encabezado
        with open(archivo, 'a') as diccionario_csv:
            diccionario_csv.write('Nro., Fecha, Cliente\n')
        """

    else:
        lector = csv.reader(diccionario_csv, delimiter=';')
        # saltar encabezado
        # next(lector)
        for row in lector:
            datos.append(row)

        for dato in datos:
            if dato[0] not in diccionario:
                diccionario[int(dato[0])] = {'Cliente': dato[1], 'AAAAMMDD': dato[2]}

        diccionario_csv.close()

    return diccionario


def leer_lista(archivo: str) -> list:
    datos = list()
    lista: list = []

    # abre el archivo, al no tener datos hace una excepcion para crear una lista
    try:
        lista_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay datos cargados')
        """
        #encabezado
        with open(archivo, 'a') as lista_csv:
            lista_csv.write('Nro., Fecha, Cliente\n')
        """

    else:
        lector = csv.reader(lista_csv, delimiter=';')
        # saltar encabezado
        # next(lector)
        for row in lector:
            datos.append(row)

        for dato in datos:
            segu = [int(dato[0]), dato[1]]
            lista.append(segu)

        lista_csv.close()

    return lista


def validar_fecha(fecha: str) -> bool:
    formato = "%d/%m/%Y"
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


def entrada_operaciones(operaciones: list) -> list:
    # operacion: list = []
    # operacion: dict = {}
    """
    cadena: str = input('cadena: ')
    fecha: str = input('Ingrese anio auto: ')
    while not validar_fecha(fecha):
        fecha: str = input("Ingrese dd/mm/yyyy: ")
    numero: str = input('Ingrese numero: ')
    while not numero.isnumeric():
        print("no ingresaste un numero entero: ")
        numero = input("Ingrese otro numero: ")

    with open("operaciones.csv", "a") as archivo:

        archivo.write(
            patente + ',' + fecha + ',' +  numero\n')

        # lista
        # operacion = [cadena, anio, numero]
        # operaciones.append(operacion)

        # diccionario
        # operaciones[cadena] = {'anio': anio, 'precio compra': precio_compra}


    print(operacion)
    """
    return operaciones


def main():
    diccionario = leer_diccionario('diccionario.csv')
    lista = leer_lista('lista.csv')
    print('diccionario')
    print(diccionario)
    print('lista')
    print(lista)

    opciones: list = [" ",
                      " ",
                      " ",
                      " ",
                      "Salir"]
    opcion: str = ''

    while opcion != '5':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            print('opcion 1')

        elif opcion == '2':

            if len(diccionario) != 0:

                print('opcion 2')

            else:

                print('el diccionario esta vacio')

        elif opcion == '3':

            if len(diccionario) != 0:

                print('opcion 3')

            else:

                print('el diccionario esta vacio')

        elif opcion == '4':

            if len(diccionario) != 0:

                print('opcion 4')

            else:

                print('el diccionario esta vacio')

        elif opcion == '5':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 5")


main()
