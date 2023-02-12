import psycopg2
from config import connectdb, closedb
from inputValidation import validateNaturalNumber

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
        opcion = validateNaturalNumber("Introduce la opción del menú: ", len(self.menu_options))
        return opcion

    def addNewClient(self):
        try:
            print("Nuevo cliente: ")
            first_name = input("Introduce el nombre: ")
            last_name = input("Introduce el apellido: ")
            dni = input("Introduce el DNI: ")
            birthdate = input("Introduce la fecha de nacimiento (YYYY-MM-DD): ")
            phone = input("Introduce el teléfono: ")
            query = "INSERT INTO clients (name, last_name, birthdate, phone) VALUES (%s, %s, %s, %s, %s)"
            self.cur.execute(query, (first_name, last_name, dni, birthdate, phone))
            self.conx.commit()
            print(f"El cliente {first_name} {last_name} con DNI {dni} ha sido agregado.")
        except Exception as e:
            self.conx.rollback()
            print(f"Error al agregar el cliente: {str(e)}")

    def deleteClient(self):
        try:
            client_dni = input("Introduce el DNI del cliente a eliminar: ")
            query = "DELETE FROM clients WHERE dni = %s"
            self.cur.execute(query, (client_dni,))
            self.conx.commit()
            print(f"El cliente con ID {client_dni} ha sido eliminado.")
        except Exception as e:
            self.conx.rollback()
            print(f"Error al eliminar el cliente: {str(e)}")

    def showClient(self):
        try:
            client_dni = input("Introduce el DNI del cliente (dejar en blanco para ver todos los clientes): ")
            if client_dni:
                query = "SELECT * FROM clients WHERE id = %s"
                self.cur.execute(query, (client_dni,))
                result = self.cur.fetchone()
                if result:
                    print("Datos del cliente:")
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
            client_dni = input("Introduce el DNI del cliente: ")
            sport = input("Introduce el deporte en el que quieres matricular al cliente: ")
            
            if not client_dni.strip() or not sport.strip():
                raise ValueError("El DNI del cliente y el deporte son obligatorios.")
            
            self.cur.execute(f"SELECT * FROM clientes WHERE dni = {client_dni}")
            client = self.cur.fetchone()
            if not client:
                raise ValueError(f"No existe un cliente con el DNI {client_dni}.")
            
            self.cur.execute(f"SELECT * FROM matriculas WHERE cliente_id = {client_dni} AND deporte = '{sport}'")
            enrollment = self.cur.fetchone()
            if enrollment:
                raise ValueError(f"El cliente con el ID {client_dni} ya está matriculado en {sport}.")
            
            self.cur.execute(f"INSERT INTO matriculas (cliente_id, deporte) VALUES ({client_dni}, '{sport}')")
            self.conx.commit()
            print(f"El cliente con el DNI {client_dni} ha sido matriculado en {sport}.")
    	except Exception as e:
            print(f"Error: {e}")

    def disenrollClient(self):
        try:
            print("Desmatricular cliente")

            client_dni = input("Introduce el DNI del cliente: ")

            sport_nom = input("Introduce el nombre del deporte: ")

            self.cur.execute("DELETE FROM matriculas WHERE client_dni = %s AND sport_nom = %s", (client_dni, sport_nom))

            self.conx.commit()
            print(f"El cliente ha sido desmatriculado de {sport_nom}.")
        except Exception as e:
            print("Ha ocurrido un error al desmatricular el cliente:", e)
            self.conx.rollback()

    def showSports(self):
        try:
            print("Deportes de un cliente")

            client_dni = input("Introduce el DNI del cliente: ")

			#TODO: Seleccionar los deportes de un cliente
            self.cur.execute("SELECT s.sport_nom FROM sports s JOIN enrollment e ON s.sport_id = e.sport_id WHERE e.client_id = %s", (client_dni,))

            sports = self.cur.fetchall()
            print("El cliente está matriculado en los siguientes deportes:")
            for sport in sports:
                print("Nombre:", sport[0])
        except Exception as e:
            print("Ha ocurrido un error al obtener los deportes del cliente:", e)
            self.conx.rollback()
        pass

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

    def run(self):
        self.conx = connectdb()
        self.cur = self.conx.cursor()
        self.checkTable("clients", "dni VARCHAR(9) PRIMARY KEY, name VARCHAR(50), surname VARCHAR(50), birthdate DATE, phone VARCHAR(9)")
        self.checkTable("sports", "sport_id SERIAL PRIMARY KEY, sport_name VARCHAR(50), sport_price NUMERIC(5,2)")
        self.checkTable("enrollment", "enrollment_id SERIAL PRIMARY KEY, client_id VARCHAR(9), sport_id INTEGER, FOREIGN KEY (client_id) REFERENCES clients(dni), FOREIGN KEY (sport_id) REFERENCES sports(sport_id)")
        
        while True:
            opcion = self.menu()
            print("Opción elegida:", opcion)
            self.methods = [self.addNewClient, self.deleteClient, self.showClient, self.enrollClient, self.disenrollClient, self.showSports, self.closseProgram]
            self.methods[opcion-1]()
            if opcion == 7:
                break
        closedb(self.conx)

if __name__ == '__main__':
    cms = ClientManagementSystem()
    cms.run()