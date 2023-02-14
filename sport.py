class Sport:
    def __init__(self, name, precio_hora):
        self.name = name
        self.price = precio_hora

    def mostrar_nombre(self):
        return (
                    "Nombre del deporte: " + self.name + "\n" +
                    "Precio: " + self.price +  "\n" 
            )