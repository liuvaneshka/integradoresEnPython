import codecs
import csv
import os

def leer_diccionario(archivo: str) -> list:
    datos = list()
    diccionario: list = []

    try:
        diccionario_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay diccionario cargados')
        """
        #encabezado
        with open(archivo, 'a') as pedidos_csv:
            pedidos_csv.write('Nro. Pedidio, Fecha, Cliente\n')
        """

    else:
        lector = csv.reader(diccionario_csv, delimiter=';')
        #saltar encabezado
        #next(lector)
        for row in lector:
            datos.append(row)

        for dato in datos:
            segu = [int(dato[0]), dato[1]]
            diccionario.append(segu)
            #guardar en diciconario
            #if dato[0] not in ventas:
                #ventas[int(dato[0])] = {'Cliente': dato[1], 'AAAAMMDD': dato[2]}

        diccionario_csv.close()

    return diccionario


def main():

    diccionario = leer_diccionario('diccionario.csv')

    opciones: list = [" ",
                      " ",
                      " ",
                      " ",
                      " ",
                      " ",
                      "Salir"]
    opcion: str = ''

    while opcion != '7':

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

            if len(diccionario) != 0:

                print('opcion 5')

            else:

                print('el diccionario esta vacio')

        elif opcion == '6':

            if len(diccionario) != 0:

                print('opcion 6')

            else:

                print('el diccionario esta vacio')

        elif opcion == '7':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 7")


main()
