    fecha_alta: str = input("Ingrese fecha de alta")
    format = "%d/%m/%Y"

    try:
        datetime.datetime.strptime(fecha_alta, format)
        print("Formato valido.")
    except ValueError:
        print("Formato invalido debe ser dd/mm/aaaa")