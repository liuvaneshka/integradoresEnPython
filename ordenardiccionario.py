    lista_pedidos: list = []

    for i in pedidos:
        pedido = pedidos[i]
        pedido['ID pedido'] = i
        lista_pedidos.append(pedido)

    lista_pedidos.sort(key=lambda p: p['Año'], reverse=False)

    lista_pedidos.sort(key=lambda p: p['Mes'], reverse=False)

    for linea in lista_pedidos:
        print(linea)