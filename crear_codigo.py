def crear_codigo(pedidos: dict) -> int:
    numeros = list(map(int, pedidos.keys()))
    if len(numeros) > 0:
        numeros.sort()
        numero_pedido: int = int(numeros[-1]) + 1
    else:
        numero_pedido = 1

    return numero_pedido