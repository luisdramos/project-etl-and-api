from libs.NaturalNumber import NaturalNumber

nn = NaturalNumber()

# Ejemplo de menú con bucle while
while True:
    print("\n--- Menú de Opciones ---")
    print("1. Mostrar los que quedan")
    print("2. Sacar Numero")
    print("3. Mostrar encontrados")
    print("4. Ultimo Faltante")
    print("5. Salir")

    opcion = input("Selecciona una opción (1-5): ")

    if opcion == "1":
        print("Estos son todos los que quedan en la lista")
        print(nn.mostrar())
        # Aquí iría la lógica para la Opción A
    elif opcion == "2":
        sacar = int(input("Ingresar Numero a sacar: "))
        try:
            nn.remover_numero(numero = sacar)
        except Exception as e:
            print(e)
            continue
    elif opcion == "3":
        print(nn.mostrar_encontrados())
    elif opcion == "4":
        print(nn.calcular_faltantes())
    elif opcion == "5":
        print("Fin")
        break  
    else:
        print("Opción inválida.")

