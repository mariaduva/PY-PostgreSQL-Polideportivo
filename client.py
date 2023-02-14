class Client:
    def __init__(self, dni, name, surname, birthdate, phone):
        self.dni = dni
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.phone = phone

    def data(self):
        return str(self)

    def __str__(self):
        return (
            "Nombre: " + self.name + self.surname +  "\n" +
            "DNI: " + self.dni + "\n" +
            "Fecha de nacimiento: " + self.birthdate + "\n" +
            "Teléfono: " + self.phone
        )


if __name__ == "__main__":
    print("Hello World")

    c = Client("12345678A", "Miguel", "Arroyo", "1998-01-01", "666666666")
    print(c)
    print(c.data())