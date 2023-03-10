import psycopg2
import psycopg2.extras
from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connectdb():
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)  
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 
    return conn
        
def closedb(conn):
	if conn is not None:
		conn.close()
		print('Database connection closed.')