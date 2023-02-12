def validateNaturalNumber(str, max):
	goodinput = False
	while not goodinput:
		try:
			number = int(input(str))
			if number > 0 and number <= max:
				goodinput = True
				return number
			else:
				print("Opción no válida")
		except ValueError:
			print("El valor introducido no es un número.")
