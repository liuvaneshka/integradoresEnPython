import csv
import datetime


def leer_clientes(archivo: str) -> dict:
    datos = list()
    clientes: dict = {}
    # El manejo de excepcion lo aplique al verificar que el archivo tenga ya datos cargados
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
                clientes[int(dato[0])] = {'Nombre': dato[1], 'Alta': dato[2], 'Baja': dato[3], 'Plan': dato[4]}

        clientes_csv.close()

    return clientes


def validar_fecha(fecha: str) -> bool:
    formato = "%d/%m/%Y"
    # fecha_valida = None
    try:
        datetime.datetime.strptime(fecha, formato)
        fecha_valida = True
    except ValueError:
        fecha_valida = False
        print("Formato invalido debe ser dd/mm/aaaa")

    return fecha_valida


def validar_fecha_posterior(fecha_inicial: str, fecha_final: str) -> bool:
    anterior = datetime.datetime.strptime(fecha_inicial, "%d/%m/%Y")
    posterior = datetime.datetime.strptime(fecha_final, "%d/%m/%Y")
    # fecha_valida = None

    if anterior.date() < posterior.date():
        fecha_valida = True

    else:
        fecha_valida = False
        print("Fecha posterior menor a la fecha inicial")

    return fecha_valida


def ingreso_cliente(clientes: dict, planes: dict) -> dict:
    agregar: str = 'si'

    while agregar == 'si':

        numeros = list(map(int, clientes.keys()))
        if len(numeros) > 0:
            numeros.sort()
            numero_cliente: int = int(numeros[-1]) + 1
        else:
            numero_cliente = 1

        nombre: str = input('Ingrese el nombre del cliente: ')
        fecha_alta: str = input("Ingrese fecha de alta (dd/mm/yyyyy): ")
        while not validar_fecha(fecha_alta):
            fecha_alta: str = input("Ingrese fecha de alta (dd/mm/yyyyy): ")

        baja_dada: str = input("presione enter si no se dio baja, cualquier otra tecla para ingresar baja")
        if baja_dada == '':
            fecha_baja = '00/00/0000'
        else:
            fecha_baja: str = input("Ingrese fecha de baja (dd/mm/yyyyy): ")
            while not validar_fecha_posterior(fecha_alta, fecha_baja):
                fecha_baja: str = input("Ingrese fecha de baja (dd/mm/yyyyy): ")
        for p in planes:
            print(p)
        plan: str = input('Ingrese el plan: ')
        while plan not in planes:
            plan: str = input("Ingrese plan): ")

        with open("clientes.csv", "a") as archivo:

            archivo.write(str(numero_cliente) + ', ' + nombre + ', ' + fecha_alta + ', ' + fecha_baja + ', ' + plan +
                          '\n')

        clientes[int(numero_cliente)] = {'Nombre': nombre, 'Alta': fecha_alta, 'Baja': fecha_baja, 'Plan': plan}

        agregar = input("Quiere agregar otro cliente? Responda 'si' ó 'no': ")

    return clientes


def imprimir_cantidad_altas(clientes: dict):
    cantidad_altas: int = 0
    anio_ingresado: str = input("Ingrese anio: ")
    while anio_ingresado == '%Y':
        anio_ingresado: str = input("Ingrese anio (numero positivo): ")
    mes_ingresado: str = input("Ingrese mes: ")
    while mes_ingresado == '%m':
        mes_ingresado: str = input("Ingrese mes (numero positivo): ")
    if int(mes_ingresado) < 10:
        mes_ingresado = mes_ingresado.zfill(2)

    for i in clientes:
        fecha = clientes[i]['Alta']
        mes = fecha[4:6:]
        anio = fecha[7:11]

        if mes == mes_ingresado and anio == anio_ingresado:
            print(mes, anio)
            cantidad_altas += 1

    print(cantidad_altas)


def imprimir_ingresos_por_mes_anio(clientes: dict, planes: dict):
    anio_ingresado: str = input("Ingrese anio: ")
    monto_total: float = 0.0
    descuento: float = 0.0
    monto_final: float = 0.0
    montos: list = [monto_total, descuento, monto_final]
    while anio_ingresado == '%Y':
        anio_ingresado: str = input("Ingrese anio (numero positivo): ")
    dic_mes: dict = {1: montos, 2: montos, 3: montos, 4: montos, 5: montos, 6: montos, 7: montos, 8: montos, 9: montos,
                     10: montos, 11: montos, 12: montos}
    for i in range(1, 13):
        for c in clientes:
            fecha_baja = clientes[c]['Baja']
            fecha_alta = clientes[c]['Alta']
            mes_alta = fecha_alta[4:6:]
            anio_alta = fecha_alta[7:11]
            anio_baja = fecha_baja[7:11]
            mes_baja = fecha_baja[4:6:]
            plan = clientes[c]['Plan']
            plan = plan[1:]
            costo = planes[plan]

            # verificar en que mes de ese anio comenzo a facturarse en ese anio pedido
            if anio_alta == anio_ingresado:
                # para verificar si ese mismo anio se les dio la baja y contar solo hasta el mes q se facturo
                if (mes_baja == '00' and i >= int(mes_alta)) or (int(mes_alta) <= i <= int(mes_baja)):
                    # para el anio de las promos
                    if anio_alta == '2021':
                        # si el mes de alta es enero o febrero y estan dentro de los meses validos de promo
                        if (mes_alta == '01' and i <= 6) or (mes_alta == '02' and i <= 7):
                            if plan == '100MB':
                                descuento = costo * 0.15
                                monto_total = costo
                            elif plan == '1GB':
                                descuento = costo * 0.20
                                monto_total = costo
                            # para los planes q no tienen promo
                            else:
                                monto_total = costo
                                descuento = 0.0
                                # print(clientes[c])
                        # cuando se acaba la promo para los planes que tienen promo
                        elif (mes_alta == '01' and i <= 12) or (mes_alta == '02' and i <= 12):
                            monto_total = costo
                            descuento = 0.0
                            # print('se acabo el descuentico vale ')
                            # print(clientes[c])
                        # para el resto de los meses que no hay promo en ese anio
                        else:
                            monto_total = costo
                            descuento = 0.0
                            print(clientes[c])
                    # para cualquier anio
                    else:
                        monto_total = costo
                        descuento = 0.0
                        # print(clientes[c])
                    dic_mes[i] = [dic_mes[i][0] + monto_total, dic_mes[i][1] + descuento,
                                  dic_mes[i][2] + (monto_total - descuento)]

                elif (int(anio_baja) > int(anio_alta)) and (
                        int(mes_alta) <= i) and mes_alta != '01' and mes_alta != '02':
                    monto_total = costo
                    descuento = 0.0
                    print(clientes[c])
                    dic_mes[i] = [dic_mes[i][0] + monto_total, dic_mes[i][1] + descuento,
                                  dic_mes[i][2] + (monto_total - descuento)]
            # para verificar que se cobra el plan dentro del anio pedido
            elif int(anio_alta) <= int(anio_ingresado) and (
                    (int(anio_baja) >= int(anio_ingresado)) or (anio_baja == '0000')):
                print(clientes[c])
                monto_total = costo
                descuento = 0.0
                dic_mes[i] = [dic_mes[i][0] + monto_total, dic_mes[i][1] + descuento,
                              dic_mes[i][2] + (monto_total - descuento)]
    for linea in dic_mes:
        print(linea, dic_mes[linea])


def cantidad_meses_entre_fechas(anio_posterior: str, mes_posterior: str, dia_posterior: str, anio_anterior: str,
                                mes_anterior: str, dia_anterior: str) -> int:

    fecha_final = datetime.datetime(int(anio_posterior), int(mes_posterior), int(dia_posterior))
    fecha_inicial = datetime.datetime(int(anio_anterior), int(mes_anterior), int(dia_anterior))

    cantidad_meses: int = (fecha_final.year - fecha_inicial.year) * 12 + (fecha_final.month - fecha_inicial.month)

    return cantidad_meses


def imprimir_top_tres(clientes: dict, planes: dict):
    fecha_ingresada: str = input("Ingrese fecha (dd/mm/aaaa): ")
    while fecha_ingresada == '%d/%m/%Y':
        fecha_ingresada: str = input("Ingrese fecha dd/mm/aaaa ")

    dia_ingresado = fecha_ingresada[0:2]
    mes_ingresado = fecha_ingresada[3:5]
    anio_ingresado = fecha_ingresada[6:]

    for i in clientes:
        fecha_baja = clientes[i]['Baja']
        fecha_alta = clientes[i]['Alta']
        dia_alta = fecha_alta[1:3:]
        mes_alta = fecha_alta[4:6:]
        anio_alta = fecha_alta[7:11]
        dia_baja = fecha_baja[1:3:]
        mes_baja = fecha_baja[4:6:]
        anio_baja = fecha_baja[7:11]
        plan = clientes[i]['Plan']
        plan = plan[1:]
        costo = planes[plan]
        aporte = 0

        if anio_baja == '0000' and int(anio_alta) <= int(anio_ingresado):
            anio_baja = anio_ingresado
            mes_baja = mes_ingresado
            dia_baja = dia_ingresado

        if int(anio_ingresado) < int(anio_alta):
            aporte = 0

        elif int(anio_ingresado) > int(anio_alta):

            meses = cantidad_meses_entre_fechas(anio_baja, mes_baja, dia_baja, anio_alta, mes_alta, dia_alta)
            meses = meses + 1
            aporte = meses * costo

            if anio_alta == '2021':

                if(mes_alta == '01' or mes_alta == '02') and plan == '100MB':
                    descuento = (costo * 0.85) * 6
                    meses = meses - 6
                    aporte = (meses * costo) + descuento
                    print('hacer, descuentos 1', aporte)

                elif (mes_alta == '01' or mes_alta == '02') and plan == '1GB':
                    descuento = (costo * 0.85) * 6
                    meses = meses - 6
                    aporte = (meses * costo) + descuento
                    print('hacer, descuentos 1', aporte)


        elif int(anio_ingresado) == int(anio_alta):

            if int(anio_baja) > int(anio_ingresado):
                mes_baja = mes_ingresado
                meses = cantidad_meses_entre_fechas(anio_ingresado, mes_ingresado, dia_ingresado, anio_alta, mes_alta,
                                                    dia_alta)
                meses = meses + 1
                aporte = meses*costo

            if int(mes_alta) <= int(mes_ingresado) <= int(mes_baja):

                meses = cantidad_meses_entre_fechas(anio_ingresado, mes_ingresado, dia_ingresado, anio_alta, mes_alta,
                                                    dia_alta)
                meses = meses + 1
                aporte = meses*costo

            elif int(mes_alta) <= int(mes_ingresado):
                meses = cantidad_meses_entre_fechas(anio_baja, mes_baja, dia_baja, anio_alta, mes_alta,
                                                    dia_alta)
                meses = meses + 1
                aporte = meses*costo

            elif int(mes_alta) >= int(mes_ingresado):
                aporte = 0

        clientes[i]['APORTES'] = aporte

    lista_clientes: list = []

    for id_cliente in clientes:

        cliente = clientes[id_cliente]
        cliente['ID'] = id_cliente
        lista_clientes.append(cliente)

    lista_clientes.sort(key=lambda p: p['APORTES'], reverse=True)

    top_tres = lista_clientes[0:3]

    for linea in top_tres:
        if linea['APORTES'] > 0:
            print(linea)
        else:
            print('no hay clientes para la fecha')


def main():
    planes: dict = {'50MB': 1450, '100MB': 2100, '1GB': 4500}
    clientes = leer_clientes('clientes.csv')

    opciones: list = ["Permitir el ingreso de nuevos datos de clientes, ya sean actuales o históricos ",
                      "Imprimir en pantalla la cantidad de clientes dados de alta en un mes y año en particular"
                      "ingresado por el usuario",
                      "Imprimir en pantalla el ingreso total $ de cada mes de un año ingresado por el usuario,"
                      "discriminando el monto aplicado en descuentos. Se debe indicar mes, monto total,"
                      "monto de descuento, monto final.",
                      "Imprimir la información del top 3 de los clientes que más dinero han aportado a la"
                      "empresa desde su ingreso y hasta una fecha de corte indicada por el usuario. Se debe"
                      "indicar Id, Nombre y Apellido, Fecha de Alta, Fecha de Baja, Plan y Monto final ",
                      "Salir"]
    opcion: str = ''

    while opcion != '5':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            clientes = ingreso_cliente(clientes, planes)

        elif opcion == '2':

            if len(clientes) != 0:

                imprimir_cantidad_altas(clientes)

            else:

                print('el clientes esta vacio')

        elif opcion == '3':

            if len(clientes) != 0:

                imprimir_ingresos_por_mes_anio(clientes, planes)

            else:

                print('el clientes esta vacio')

        elif opcion == '4':

            if len(clientes) != 0:

                imprimir_top_tres(clientes, planes)

            else:

                print('el clientes esta vacio')

        elif opcion == '5':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 5")


main()
