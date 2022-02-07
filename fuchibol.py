import csv


def leer_preguntas(archivo: str) -> dict:
    datos = list()
    preguntas: dict = {}

    try:
        preguntas_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay preguntas cargados')

    else:
        lector = csv.reader(preguntas_csv, delimiter=',')
        # saltar encabezado
        # next(lector)
        for row in lector:
            datos.append(row)

        for dato in datos:
            if dato[0] not in preguntas:
                preguntas[int(dato[0])] = {'Pregunta': dato[1], 'Dificultad': dato[2]}

        preguntas_csv.close()

    return preguntas


def leer_respuestas(archivo: str) -> dict:
    datos = list()
    respuestas: dict = {}

    try:
        respuestas_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay preguntas cargados')

    else:
        lector = csv.reader(respuestas_csv, delimiter=',')

        for row in lector:
            datos.append(row)

        for dato in datos:

            if dato[0] not in respuestas:
                respuestas[int(dato[0])] = {'1': dato[1], '2': dato[2], '3': dato[3], '4': dato[4]}

        respuestas_csv.close()

    return respuestas


def leer_score(archivo: str) -> dict:
    datos = list()
    scores: dict = {}

    try:
        scores_csv = open(archivo, newline='', encoding="UTF-8")
    except IOError:
        print('No hay preguntas cargados')

    else:
        lector = csv.reader(scores_csv, delimiter=',')

        for row in lector:
            datos.append(row)

        for dato in datos:

            if dato[0] not in scores:
                scores[int(dato[0])] = {'Nombre': dato[1], 'Dificultad': dato[2], 'Puntaje': int(dato[3])}

        scores_csv.close()

    return scores


def partida(preguntas: dict, respuestas: dict, dificultad: str) -> int:
    porcentaje = 0.0
    puntaje = 0
    correcta: str = ' '
    numeros: list = ['1', '2', '3', '4']
    contador: int = 0

    for i in preguntas:
        dif = preguntas[i]['Dificultad']

        if dif == dificultad:

            pregunta = preguntas[i]['Pregunta']
            print(pregunta)
            print(respuestas[i])
            respuesta = respuestas[i]
            respuesta_ingresada: str = input('Ingrese respuesta: ')

            if respuesta_ingresada in numeros:
                print('entro')
                respuesta_ingresada = respuesta[respuesta_ingresada]
                print(respuesta_ingresada)

            for c in respuesta:

                r = respuesta[c]
                c = r[0:2]

                if c == ' *':
                    correcta = r

            if respuesta_ingresada == correcta:
                puntaje += 1

            print(correcta)
            contador += 1
            porcentaje = (puntaje * 100) / contador

    print('% respuestas correctas: ', porcentaje)

    return puntaje


def ingresar_jugador(preguntas: dict, respuestas: dict, scores: dict) -> dict:
    dificultad: str = ' '
    d: str = ''
    numeros = list(map(int, scores.keys()))

    if len(numeros) > 0:
        numeros.sort()
        numero_partida: int = int(numeros[-1]) + 1
    else:
        numero_partida = 1

    nombre: str = input('Ingrese Nombre del jugador: ')
    dificulatades: list = ["Alta", "Baja"]

    while d != '1' and d != '2':
        print("Dificultades: ")
        for indice in range(len(dificulatades)):
            print(indice + 1, ".", dificulatades[indice])
        d = input(" ")
        if d == '1':
            dificultad = ' alta'
        elif d == '2':
            dificultad = ' baja'
        else:
            print("Las opciones deben ser entre 1 y 7")

    puntaje = partida(preguntas, respuestas, dificultad)

    with open("scores.txt", "a") as archivo:

        archivo.write(str(numero_partida) + ',' + nombre + ',' + dificultad + ',' + str(puntaje) + '\n')

    scores[numero_partida] = {'Nombre': nombre, 'Dificultad': dificultad, 'Puntaje': puntaje}

    print(scores)

    return scores


def mostrar_score(scores: dict) -> None:
    for i in scores:
        print(scores[i])


def main():
    preguntas = leer_preguntas('preguntas.txt')
    respuestas = leer_respuestas('respuestas.txt')
    scores = leer_score('score.txt')
    print(scores)
    # print(respuestas)

    opciones: list = ["Comenzar Partida",
                      "Mostrar Score Historico",
                      "Salir"]
    opcion: str = ''

    while opcion != '3':

        print("Menu: ")
        for indice in range(len(opciones)):
            print(indice + 1, ".", opciones[indice])

        opcion = input(" ")

        if opcion == '1':

            scores = ingresar_jugador(preguntas, respuestas, scores)

            print('opcion 1')

        elif opcion == '2':

            if len(preguntas) != 0:

                mostrar_score(scores)

            else:

                print('el preguntas esta vacio')

        elif opcion == '3':

            print("Cordial Despedida")

        else:

            print("Las opciones deben ser entre 1 y 7")


main()
