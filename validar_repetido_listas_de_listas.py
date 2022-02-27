def validar_no_repetido(cadena: str, listas: list) -> bool:

    cadena_validada: bool = False

    for linea in listas:
        if cadena == linea[0]:
            cadena_validada = True
        
    return cadena_validada   

def main():
    
    clientes = [['1abc','maria'],['3abc','marco'],['2abc','gabriela'],['4abc','aquiles']]
    
    cuit: str = input('cuit: ')
    while validar_no_repetido(cuit, clientes):
        cuit: str = input('cuit: ')
    nombre: str = input('nombre: ')
    
main()