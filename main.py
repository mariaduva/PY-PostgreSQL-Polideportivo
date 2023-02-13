import psycopg2
from config import connectdb, closedb
from inputValidation import validateNaturalNumber, validateDni, validatePhoneNumber, validateIsDigit

class ClientManagementSystem:
    
    def __init__(self):
        self.menu_options = ["1. Dar de alta un cliente con sus datos personales", 
                             "2. Dar de baja un cliente", 
                             "3. Mostrar los datos personales de un cliente o de todos", 
                             "4. Matricular a un cliente en un deporte", 
                             "5. Desmatricular a un cliente en un deporte",
                             "6. Mostrar los deportes de un cliente",
                             "7. Salir"]
        
    def menu(self):
        print("Menú de opciones")
        [print(i) for i in self.menu_options]
        option = validateNaturalNumber("Introduce la opción del menú: ", len(self.menu_options))
        return option

    def addNewClient(self):
        print("Dar de alta un cliente con sus datos personales")
        try:
            dni = validateDni("Introduce el DNI del cliente: ", False)
            if dni:
                query = "SELECT * FROM clients WHERE dni = %s"
                self.cur.execute(query, (dni,))
                result = self.cur.fetchone()
                if result:
                    raise ValueError(f"Ya existe un cliente con el DNI {dni}.")
                else:
                    name = input("Introduce el nombre: ")
                    surname = input("Introduce el apellido: ")
                    birthdate = input("Introduce la fecha de nacimiento (YYYY-MM-DD): ")
                    phone = validatePhoneNumber("Introduce un número de telefono: ")
                    query = "INSERT INTO clients (dni, name, surname, birthdate, phone) VALUES (%s, %s, %s, %s, %s)"
                    self.cur.execute(query, (dni, name, surname, birthdate, phone))
                    self.conx.commit()
                    print(f"El cliente {name} {surname} con DNI {dni} ha sido agregado.")
            else:
                raise ValueError("El DNI es obligatorio.")
        except Exception as e:
            self.conx.rollback()
            print(f"Error al agregar el cliente: {str(e)}")

    def deleteClient(self):
        print("Dar de baja un cliente")
        try:
            dni = validateDni("Introduce el DNI del cliente a eliminar: ", False)
            if dni:
                query = "SELECT * FROM clients WHERE dni = %s"
                self.cur.execute(query, (dni,))
                result = self.cur.fetchone()
                if result:
                    query = "DELETE FROM clients WHERE dni = %s"
                    self.cur.execute(query, (dni,))
                    self.conx.commit()
                    print(f"El cliente con DNI {dni} ha sido eliminado.")
                else:
                    print("No se encontró un cliente con ese DNI.")
            else:
                raise ValueError("El DNI es obligatorio.")
        except Exception as e:
            self.conx.rollback()
            print(f"Error al eliminar el cliente: {str(e)}")

    def showClient(self):
        try:
            dni = validateDni("Introduce el DNI del cliente (dejar en blanco para ver todos los clientes): ", True)
            if dni:
                query = "SELECT * FROM clients WHERE dni = %s"
                self.cur.execute(query, (dni,))
                result = self.cur.fetchone()
                if result:
                    print("Datos del cliente:")
                    print("-" * 20)
                    print(f"DNI: {result[0]}")
                    print(f"Nombre: {result[1]}")
                    print(f"Apellido: {result[2]}")
                    print(f"Fecha de nacimiento: {result[3]}")
                    print(f"Teléfono: {result[4]}")
                else:
                    print("No se encontró un cliente con ese DNI.")
            else:
                query = "SELECT * FROM clients"
                self.cur.execute(query)
                results = self.cur.fetchall()
                if results:
                    print("Datos de los clientes:")
                    print("-" * 20)
                    for result in results:
                        print(f"DNI: {result[0]}")
                        print(f"Nombre: {result[1]}")
                        print(f"Apellido: {result[2]}")
                        print(f"Fecha de nacimiento: {result[3]}")
                        print(f"Teléfono: {result[4]}")
                        print("-" * 20)
                else:
                    print("No hay clientes registrados.")
        except Exception as e:
            print(f"Error al obtener los datos del cliente: {str(e)}")

    def enrollClient(self):
    	try:
            print("Matricular a un cliente en un deporte: ")
            client_id = validateDni("Introduce el DNI del cliente: ", False)
            sport_id = validateIsDigit("Introduce el ID del deporte en el que quieres matricular al cliente: ")
            
            query = "SELECT * FROM clients WHERE dni = %s"
            self.cur.execute(query, (client_id,))
            client = self.cur.fetchone()
            
            query = "SELECT * FROM sports WHERE sport_id = %s"
            self.cur.execute(query, (sport_id,))
            sport = self.cur.fetchone()
            
            if not client or not sport:
                raise ValueError("El cliente o el deporte no existen.")
            else:
                query = "SELECT * FROM enrollment WHERE client_id = %s AND sport_id = %s"
                self.cur.execute(query, (client_id, sport_id))
                
                enrollment = self.cur.fetchone()
                if enrollment:
                    raise ValueError(f"El cliente con el dni {client_id} ya está matriculado en {sport_id}.")
                else:
                    query = "SELECT max(enrollment_id) FROM enrollment"
                    self.cur.execute(query)
                    result = self.cur.fetchone()
                    if result and result[0]:
                        last_enrollment_id = result[0]
                    else:
                        last_enrollment_id = 0
                    
                    query = "INSERT INTO enrollment (enrollment_id, client_id, sport_id) VALUES (%s, %s, %s)"
                    self.cur.execute(query, (last_enrollment_id + 1, client_id, sport_id))
                    self.conx.commit()
                    print(f"El cliente con el DNI {client_id} ha sido matriculado en {sport_id}.")
    	except Exception as e:
            print(f"Error: {e}")

    def disenrollClient(self):
        try:
            print("Desmatricular cliente")
            client_id = validateDni("Introduce el DNI del cliente: ", False)
            sport_name = input("Introduce el nombre del deporte: ")
            
            query = "SELECT * FROM sports WHERE sport_name = %s"
            self.cur.execute(query, (sport_name,))
            result = self.cur.fetchall()
            if result:
                sport_id = result[0][0]
            else:
                print("No se ha encontrado el deporte indicado.")
                
            query = "DELETE FROM enrollment WHERE client_id = %s AND sport_id = %s"
            self.cur.execute(query, (client_id, sport_id))
            self.conx.commit()
            
            print(f"El cliente ha sido desmatriculado de {sport_name}.")
        except Exception as e:
            print("Ha ocurrido un error al desmatricular el cliente:", e)
            self.conx.rollback()

    def showSports(self):
        try:
            print("Deportes de un cliente")
            client_dni = validateDni("Introduce el DNI del cliente: ", False)
            self.cur.execute("SELECT s.sport_id, s.sport_name FROM sports s JOIN enrollment e ON s.sport_id = e.sport_id WHERE e.client_id = %s", (client_dni,))
            sports = self.cur.fetchall()
            print("El cliente está matriculado en los siguientes deportes:")
            print("|   ID   |      Nombre     |")
            for sport in sports:
                print("-" * 20)
                print(f"|   {sport[0]}   |   {sport[1]}   |")
                print("-" * 20)
        except Exception as e:
            print("Ha ocurrido un error al obtener los deportes del cliente:", e)
            self.conx.rollback()

    def closseProgram(self):
        print("Saliendo del programa...")
        
    def checkTable(self, table_name, columns):
        table_exists_query = f"SELECT to_regclass('public.{table_name}')"
        self.cur.execute(table_exists_query)
        result = self.cur.fetchone()[0]

        if not result:
            create_table_query = f"CREATE TABLE {table_name} ({columns});"
            self.cur.execute(create_table_query)
            self.conx.commit()
            print(f"Table '{table_name}' created successfully.")
        else:
            print(f"Table '{table_name}' already exists.")
            
    def addExampleData(self):
        query = "INSERT INTO sports (sport_id, sport_name, sport_price) VALUES (101, 'Futbol', 50.00), (102, 'Baloncesto', 40.00), (103, 'Tenis', 60.00)"
        self.cur.execute(query)
        self.conx.commit()
            
    def run(self):
        self.conx = connectdb()
        self.cur = self.conx.cursor()
        
        #Check if tables exist, if not, create them. Also add some example data.
        self.checkTable("clients", "dni text PRIMARY KEY, name VARCHAR(50), surname VARCHAR(50), birthdate DATE, phone VARCHAR(9)")
        self.checkTable("sports", "sport_id SERIAL PRIMARY KEY, sport_name VARCHAR(50), sport_price NUMERIC(5,2)")
        self.checkTable("enrollment", "enrollment_id SERIAL PRIMARY KEY, client_id text, sport_id INTEGER, FOREIGN KEY (client_id) REFERENCES clients(dni), FOREIGN KEY (sport_id) REFERENCES sports(sport_id)")
        #self.addExampleData()
        
        while True:
            option = self.menu()
            self.methods = [self.addNewClient, self.deleteClient, self.showClient, self.enrollClient, self.disenrollClient, self.showSports, self.closseProgram]
            self.methods[option-1]()
            if option == 7:
                break
        closedb(self.conx)

if __name__ == '__main__':
    cms = ClientManagementSystem()
    cms.run()