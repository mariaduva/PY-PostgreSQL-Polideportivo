class Client:
    def __init__(self, dni, name, surname, birthdate, phone):
        self.dni = dni
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.phone = phone

        def data(self):
            return (
                    "Nombre: " + self.name + self.surname +  "\n" +
                    "DNI: " + self.dni + "\n" +
                    "Fecha de nacimiento: " + self.fecha_nacimiento + "\n" +
                    "Teléfono: " + self.telefono
            )
