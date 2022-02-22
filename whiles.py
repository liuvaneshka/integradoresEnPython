    mes: str = input("Ingrese mes: ")
    while not mes.isnumeric() or not int(mes) != 0 or not int(mes) <= 12:
        mes: str = input("Ingrese mes (numero positivo): ")