import csv
import datetime
import operator


def leer_clientes(archivo: str) -> dict:
    datos = list()
    clientes: dict = {}

    # abre el archivo, al no tener datos cargados hace una exepcion para crear el clientes
    try:
        clientes_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay datos cargados')

    else:
        lector = csv.reader(clientes_csv, delimiter=',')

        for row in lector:
            datos.append(row)

        for dato in datos:
            if dato[0] not in clientes:
                clientes[int(dato[0])] = {'Razon Social': dato[1], 'Categoria': dato[2]}
                # CUIT, Razón Social, Categoría de Cliente
        clientes_csv.close()

    return clientes


def leer_comprobantes(archivo: str) -> list:
    datos = list()
    comprobantes: list = []

    # abre el archivo, al no tener datos hace una excepcion para crear una comprobantes
    try:
        comprobantes_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay datos cargados')

    else:
        lector = csv.reader(comprobantes_csv, delimiter=',')

        for row in lector:
            datos.append(row)

        for dato in datos:
            # CUIT, Fecha en formato AAAAMMDD, Tipo de Comprobante (Factura o Cobranza), Monto
            segu = [int(dato[0]), dato[1], dato[2], int(dato[3])]
            comprobantes.append(segu)

        comprobantes_csv.close()

    return comprobantes


def validar_fecha(fecha: str) -> bool:
    formato = "%Y%m%d"
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


def validar_numero(numero: str) -> bool:
    numero_validado: bool = False

    # intento que el numero sea entero, (positivo o negativo)
    try:
        numero = int(numero)

    except ValueError:

        numero_validado = True

    return numero_validado


def entrada_movimientos(comprobantes: list, clientes: dict) -> list:
    # comprobante: list = []
    tipo: str = ''

    # CUIT, Fecha en formato AAAAMMDD, Tipo de Comprobante (Factura o Cobranza), Monto
    #  [int(dato[0]), dato[1], dato[2], int(dato[3])]
    cuit: str = input('Ingrese cuit: ')
    while int(cuit) not in clientes:
        print('Cuits validos, existentes')
        for i in clientes:
            print(i)
        cuit: str = input('Ingrese cuit: ')

    fecha: str = input('Ingrese fecha yyyymmdd: ')
    while not validar_fecha(fecha):
        fecha: str = input("Ingrese yyyymmdd: ")
    monto: str = input('Ingrese monto: ')
    while validar_numero(monto):
        print("no ingresaste un numero entero ositvo o negativo: ")
        monto = input("Ingrese otro monto: ")
    if int(monto) < 0:
        tipo = 'Cobranza'
    elif int(monto) >= 0:
        tipo = 'Factura'

    with open("comprobantes.csv", "a") as archivo:

        archivo.write(
            cuit + ',' + fecha + ',' + tipo + ',' + monto + '\n')

    comprobante = [cuit, fecha, tipo, monto]
    comprobantes.append(comprobante)

    print(comprobante)

    return comprobantes


def validar_fecha_posterior(fecha_inicial: str, fecha_final: str) -> bool:
    anterior = datetime.datetime.strptime(fecha_inicial, "%Y%m%d")
    posterior = datetime.datetime.strptime(fecha_final, "%Y%m%d")
    # fecha_valida = None

    if anterior.date() < posterior.date():
        fecha_valida = True

    else:
        fecha_valida = False
        print("Fecha posterior menor a la fecha inicial")

    return fecha_valida


def imprimir_deuda(comprobantes: list, clientes: dict) -> None:

    deuda: int = 0
    saldo_facturado: int = 0

    cuit: str = input('Ingrese cuit: ')
    while int(cuit) not in clientes:
        print('Cuits validos, existentes')
        for i in clientes:
            print(i)
        cuit: str = input('Ingrese cuit: ')

    fecha: str = input('Ingrese fecha yyyymmdd: ')
    while not validar_fecha(fecha):
        fecha: str = input("Ingrese yyyymmdd: ")

    for linea in comprobantes:
        fecha_anterior = linea[1]
        monto = linea[3]
        validada = validar_fecha_posterior(fecha_anterior, fecha)

        if int(cuit) == linea[0] and validada is True:
            if linea[2] == 'Cobranza':
                deuda += monto
            elif linea[2] == 'Factura':
                saldo_facturado += monto
    print('deuda', deuda)
    print('saldo facturado', saldo_facturado)
    deuda_total = deuda + saldo_facturado

    if deuda_total < 0:
        print('deuda total: ', deuda_total)
    else:
        print('no presenta deudas')


def imprimir_clientes_saldo_a_favor(comprobantes: list) -> None:

    saldos: dict = {}
    monto_cobranza: int = 0
    monto_facturacion: int = 0

    for linea in comprobantes:
        cuit = linea[0]
        tipo = linea[2]
        monto = linea[3]

        if cuit not in saldos:

            if tipo == 'Factura':

                monto_facturacion = monto

            elif tipo == 'Cobranza':

                monto_cobranza = monto

        elif cuit in saldos:

            if tipo == 'Factura':
                fac = saldos[cuit]['Factura']
                monto_facturacion = monto + fac

            elif tipo == 'Cobranza':
                cob = saldos[cuit]['Cobranza']
                monto_cobranza = monto + cob

        saldos[cuit] = {'Cobranza': monto_cobranza, 'Factura': monto_facturacion}

    for cliente in saldos:
        c = saldos[cliente]['Cobranza']
        f = saldos[cliente]['Factura']
        # print(cliente, f+c)
        c = c * -1

        if c < f:
            saldo_favor = f - c
            print('cuit: ', cliente, 'saldo: ', saldo_favor)


def imprimir_facturacion_periodo(comprobantes: list) -> None:

    facturacion_periodo: dict = {}
    monto_facturado: int = 0

    for comprobante in comprobantes:
        tipo = comprobante[2]
        monto = comprobante[3]
        fecha = comprobante[1]
        f = datetime.datetime.strptime(fecha, "%Y%m%d")
        mes = f.month
        anio = f.year
        if mes < 10:
            periodo = str(anio)+'0'+str(mes)
        else:
            periodo = str(anio)+str(mes)

        if tipo == 'Factura':

            if periodo in facturacion_periodo:
                monto_anterior = facturacion_periodo[periodo]
                monto_facturado = monto_anterior + monto

            elif periodo not in facturacion_periodo:

                monto_facturado = monto

            facturacion_periodo[periodo] = monto_facturado

    ordenada = sorted(facturacion_periodo.items(), key=operator.itemgetter(1), reverse=True)

    for linea in ordenada:
        p = linea[0]
        monto = linea[1]
        print('periodo: ', p, 'monto: ', monto)


def imprimir_promedio_categorias(comprobantes: list, clientes: dict) -> None:

    cliente: dict = {}
    monto_total: int = 0
    categorias: dict = {}

    for lista in comprobantes:
        cuit = lista[0]
        tipo = lista[2]
        monto = lista[3]

        if tipo == 'Factura':

            if cuit in cliente:
                monto_anterior = cliente[cuit]
                monto_total = monto_anterior + monto

            elif cuit not in cliente:
                monto_total = monto

            cliente[cuit] = monto_total

    for i in cliente:
        monto = cliente[i]
        cantidad: int = 1

        if i in clientes:
            cat = clientes[i]['Categoria']
            if cat in categorias:
                cantidad += 1
                monto_anterior = categorias[cat]['monto total']
                monto_total = monto_anterior + monto

            else:
                monto_total = monto

            categorias[cat] = {'monto total': monto_total, 'cantidad': cantidad}

    for i in categorias:
        suma = categorias[i]['monto total']
        veces = categorias[i]['cantidad']
        promedio = suma/veces
        print('categoria: ', i, 'promedio: ', promedio)


def main():
    clientes = leer_clientes('clientes.csv')
    comprobantes = leer_comprobantes('comprobantes.csv')
    print('clientes')
    print(clientes)
    print('comprobantes')
    print(comprobantes)

    opciones: list = ["Permitir el ingreso de nuevos movimientos para los clientes existentes",
                      "Imprimir la deuda a una fecha para un determinado cliente. El usuario debe indicar el CUIL"
                      " sobre el cual quiere hacer el análisis ",
                      "Imprimir el listado de clientes con saldo a favor. Se debe indicar CUIL, Descripción y Monto",
                      "Imprimir el reporte de Facturacion total por período ordenada por monto descendente. Se debe"
                      "indicar: Período (en formato AAAAMM) y monto ",
                      "Imprimir el reporte de Promedio de monto facturado según categoría de cliente. "
                      "Se debe indicar: Categoría y monto promedio",
                      "Salir"]
    opcion: str = ''

    while opcion != '6':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            comprobantes = entrada_movimientos(comprobantes, clientes)

        elif opcion == '2':

            if len(clientes) != 0:

                imprimir_deuda(comprobantes, clientes)

            else:

                print('el clientes esta vacio')

        elif opcion == '3':

            if len(clientes) != 0:

                imprimir_clientes_saldo_a_favor(comprobantes)

            else:

                print('el clientes esta vacio')

        elif opcion == '4':

            if len(clientes) != 0:

                imprimir_facturacion_periodo(comprobantes)

            else:

                print('el clientes esta vacio')

        elif opcion == '5':

            if len(clientes) != 0:

                imprimir_promedio_categorias(comprobantes, clientes)

            else:

                print('el clientes esta vacio')

        elif opcion == '6':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 6")


main()
