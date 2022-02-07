def leer_temperaturas(archivo: str) -> list:
    datos = list()
    temperaturas: list = []

    with codecs.open(os.path.dirname(os.path.abspath(__file__)) + '/' + archivo, "r", encoding='utf-8',
                     errors='ignore') as f:
        lector = csv.reader(f, delimiter=';', quotechar='|')
        next(lector)
        for row in lector:
            datos.append(row)

    for dato in datos:
        temperatura = [dato[0], int(dato[1]), dato[2], int(dato[3])]
        temperaturas.append(temperatura)
        
        

    print('temperaturas: ')
    print(temperaturas)

    return temperaturas