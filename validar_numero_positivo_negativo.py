def validar_numero(numero: str) -> bool:
    numero_validado: bool = False

    try:
        numero = int(numero)
        # numero = float(numero)
        # print(numero_validado)
    except ValueError:
        """
        # solo validar si es negativo
        if numero.lstrip('-').isdigit():
            numero_validado = False
            print(numero_validado)
        else:
            numero_validado = True
        """
        numero_validado = True

    return numero_validado


def main():

    numero: str = input('1. Ingrese un numero: ')
    while validar_numero(numero):
        print("no ingresaste un numero entero: ")
        numero = input("Ingrese otro numero: ")
    numero_entero_positivo: str = input('2. Ingrese un numero entero positivo: ')
    while not numero_entero_positivo.isnumeric():
        print("no ingresaste un numero entero positivo: ")
        numero_entero_positivo = input("Ingrese otro numero: ")
    # print('cadena',numero)
    # print('int', int(numero))
    # print('float', float(numero))

    
main()