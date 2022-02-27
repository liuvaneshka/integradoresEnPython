# ordenar diccionario que contiene diccionarios
    lista: list = []

    for clave in diccionario:
        #tomo el subdiccionario
        contenido = diccionario[clave]
        #le introduzo a ese subdiccionario la clave del diccionario
        contenido['clave'] = clave
        # creo una lista con todos los subdiccionarios
        lista_pedidos.append(contenido)
        
    # ordeno 
    lista.sort(key=lambda p: p['clave'], reverse=False)

    lista.sort(key=lambda p: p['otra clave'], reverse=False)

    for linea in lista:
        print(linea)
        
"""
    #ordenar diccionario con solo valores
    import operator
    ordenada = sorted(facturacion_periodo.items(), key=operator.itemgetter(1), reverse=True)

    for linea in ordenada:
        print(linea)
"""
