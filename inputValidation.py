import re

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
   
def validateDni(str, blank):
    patern = '^[0-9]{8,8}[A-Za-z]$'
    goodinput = False
    while not goodinput:
        try:
            dni = input(str)
            result = re.match(pattern, dni)
            if result or (blank and dni == ""):
                goodinput = True
                return dni
            else:
                print("El DNI introducido no es válido.")
        except ValueError:
            print("Errror")
            
def validatePhoneNumber(str):
	pattern = '(\+34|0034|34)?[ -]*(6|7)[ -]*([0-9][ -]*){8}'
	goodinput = False
	while not goodinput:
		try:
			phone = input(str)
			result = re.match(pattern, phone)
			if result:
				goodinput = True
				return phone
			else:
				print("El número de teléfono introducido no es válido.")
		except ValueError:
			print("Error")
   
def validateIsDigit(str):
	goodinput = False
	while not goodinput:
		try:
			number = int(input(str))
			if number > 0:
				goodinput = True
				return number
			else:
				print("El valor introducido no es un número.")
		except ValueError:
			print("El valor introducido no es un número.")
    
