import csv
from datetime import datetime


def leer_operaciones(archivo: str) -> list:
    datos = list()
    operaciones: list = []
    # El manejo de excepcion lo aplique al verificar que el archivo tenga ya datos cargados
    try:
        operaciones_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay datos cargados')

    else:
        lector = csv.reader(operaciones_csv, delimiter=',')
        for row in lector:
            datos.append(row)

        for dato in datos:
            segu = [dato[0], dato[1], int(dato[2]), int(dato[3]), int(dato[4]), int(dato[5]), dato[6], int(dato[7])]
            operaciones.append(segu)

        operaciones_csv.close()

    return operaciones


def validar_anio(anio: str) -> bool:
    formato = "%Y"
    # fecha_valida = None
    try:
        datetime.strptime(anio, formato)
        anio_valido = True
    except ValueError:
        anio_valido = False
        print("Formato invalido debe ser aaaa")

    return anio_valido


def validar_numero(numero: str) -> bool:
    numero_validado: bool = False

    if not numero.isnumeric():
        numero_validado = True

    return numero_validado


def entrada_operacion(operaciones: list) -> list:
    # operacion: list = []

    patente: str = input('Ingrese patente: ')
    marca: str = input('Ingrese marca: ')
    anio: str = input('Ingrese anio auto: ')
    while not validar_anio(anio):
        anio: str = input("Ingrese anio yyyyy: ")
    precio_compra: str = input('Ingrese precio de compra: ')
    while validar_numero(precio_compra):
        print("no ingresaste un numero entero positivo: ")
        precio_compra = input("Ingrese otro precio_compra: ")
    costo_arreglo: str = input('Ingrese costo de arreglo: ')
    while validar_numero(costo_arreglo):
        print("no ingresaste un numero entero positivo: ")
        costo_arreglo = input("Ingrese costo de arreglo: ")
    precio_venta: str = input('Ingrese precio de venta: ')
    while validar_numero(precio_venta):
        print("no ingresaste un numero entero positivo: ")
        precio_venta = input("Ingrese precio de venta: ")
    empleado: str = input('Ingrese empleado: ')
    anio_operacion: str = input('Ingrese anio operacion: ')
    while not validar_anio(anio_operacion):
        anio_operacion: str = input("Ingrese anio operacion: ")

    with open("operaciones.csv", "a") as archivo:

        archivo.write(
            patente + ',' + marca + ',' + anio + ',' + str(precio_compra) + ',' + str(costo_arreglo) + ',' +
            str(precio_venta) + ',' + empleado + ',' + anio_operacion + '\n')

        operacion = [patente, marca, anio, precio_compra, costo_arreglo, precio_venta, empleado, anio_operacion]

        operaciones.append(operacion)

    print(operacion)

    return operaciones


def anio_ganancias(operaciones: list):
    diccionario: dict = {}
    # ganancia: int = 0
    # incidencia: float = 0.0
    cantidad_operaciones = len(operaciones)

    print(cantidad_operaciones)

    for operacion in operaciones:
        anio = operacion[7]
        # precio_compra = operacion[3]
        precio_venta = operacion[5]
        costo_arreglo = operacion[4]
        op: int = 1

        ganancia = int(precio_venta) - int(costo_arreglo)
        incidencia = (op * 100) / cantidad_operaciones
        
        if anio in diccionario:
            gan = diccionario[anio]['ganancia']
            op = diccionario[anio]['operaciones']
            op += 1
            ganancia = ganancia + gan
            incidencia = (op * 100) / cantidad_operaciones
            diccionario[anio] = {'ganancia': ganancia, 'incidencia': incidencia, 'operaciones': op}
            # print(anio, diccionario[anio])

        elif anio not in diccionario:

            diccionario[anio] = {'ganancia': ganancia, 'incidencia': incidencia, 'operaciones': op}

    lista_anio: list = []

    for anio in diccionario:
        dic = diccionario[anio]
        dic['anio'] = anio
        lista_anio.append(dic)

    lista_anio.sort(key=lambda p: p['ganancia'], reverse=True)

    top = lista_anio[0:1]

    for linea in top:
        if linea['ganancia'] > 0:
            print('Anio con mayor ganacias: ', linea['anio'])
            print('Incidencia: ', linea['incidencia'])
            print('Ganancia: ', linea['ganancia'])

        else:
            print('no hay operaciones')


def reporte_antiguedad(operaciones: list):

    antiguedades: dict = {}
    anio_actual: str = datetime.today().strftime('%Y')
    nro_operacion: int = 0

    for operacion in operaciones:
        # patente = operacion[0] iba a usarlo pero es antiguedad por operacion no por auto
        marca = operacion[1]
        anio = operacion[2]
        nro_operacion += 1
        cantidad_autos: int = 1

        antiguedad = int(anio_actual) - int(anio)

        if marca in antiguedades:
            cantidad = antiguedades[a]['autos']
            antiguedad_anterior = antiguedades[a]['antiguedad']
            cantidad_autos = cantidad + 1
            antiguedad = antiguedad_anterior + antiguedad
            antiguedades[marca] = {'antiguedad': antiguedad, 'autos': cantidad_autos}

        elif marca not in antiguedades:
            antiguedades[marca] = {'antiguedad': antiguedad, 'autos': cantidad_autos}

    for m in antiguedades:
        promedio = antiguedades[m]['antiguedad']/antiguedades[m]['autos']

        print('marca: ', m, '\t Promedio: ', promedio)


def reporte_comisiones(operaciones: list):

    comisiones: dict = {}
    penalizacion: int = 1000

    for op in operaciones:
        cantidad_operaciones = 1
        precio_compra = int(op[3])
        costo_arreglo = int(op[4])
        precio_venta = int(op[5])
        empleado = op[6]
        comision = 0

        ganancia = (precio_venta - precio_compra - costo_arreglo)

        if ganancia < 0:

            perdida = ganancia * 0.05
            comision = perdida - penalizacion

        elif ganancia >= 0:

            comision = ganancia * 0.1

        if empleado in comisiones:
            monto_anterior = comisiones[empleado]['Monto']
            cantidad_anterior = comisiones[empleado]['Cantidad de operaciones']
            comision = comision + monto_anterior
            cantidad_operaciones = cantidad_anterior + 1

            comisiones[empleado] = {'Monto': comision, 'Cantidad de operaciones': cantidad_operaciones}

        elif empleado not in comisiones:

            comisiones[empleado] = {'Monto': comision, 'Cantidad de operaciones': cantidad_operaciones}

    s = open("comisiones.csv", "a")
    s.truncate(0)

    for com in comisiones:

        monto_c = str(comisiones[com]['Monto'])
        cantidad_c = str(comisiones[com]['Cantidad de operaciones'])

        with open("comisiones.csv", "a") as archivo:

            archivo.write(com + ',' + monto_c + ',' + cantidad_c + '\n')

        print(com, comisiones[com])


def main():
    operaciones = leer_operaciones('operaciones.csv')

    opciones: list = ["Permitir el ingreso de nuevas operaciones. ",
                      "Imprimir por pantalla cual fue el año en el cual se generaron mayores ganancias a la"
                      "empresa, indicando Año y Monto de la ganancia, y a su vez se debe indicar cual fue la"
                      "incidencia porcentual de ese año",
                      "Imprimir por pantalla un reporte de antigüedad de los automóviles operados, indicando"
                      "Marca y promedio de antigüedad.",
                      "Exportar al archivo comisiones.csv el total de comisiones por empleado, indicando:"
                      "Empleado, Monto, Cantidad de operaciones",
                      "Salir"]
    opcion: str = ''

    while opcion != '5':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            operaciones = entrada_operacion(operaciones)
            for linea in operaciones:
                print(linea)

        elif opcion == '2':

            if len(operaciones) != 0:

                anio_ganancias(operaciones)

            else:

                print('el operaciones esta vacio')

        elif opcion == '3':

            if len(operaciones) != 0:

                reporte_antiguedad(operaciones)

            else:

                print('el operaciones esta vacio')

        elif opcion == '4':

            if len(operaciones) != 0:

                reporte_comisiones(operaciones)

            else:

                print('el operaciones esta vacio')

        elif opcion == '5':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 5")


main()
