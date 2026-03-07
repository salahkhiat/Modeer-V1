import sqlite3 
import logging
from contextlib import contextmanager 

logging.basicConfig(
    filename='file.log',
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
)

@contextmanager
def db_connection():
    con = sqlite3.connect("data.db")
    try:
        yield con 
    except sqlite3.Error as e:
        logging.exception(f"Database error:{e}")
        raise
    finally:
        con.close()
        
        
    

def connection():
    with db_connection() as con:
        cursor = con.cursor()
        query = "SELECT namef FROM customers"
        result = cursor.execute(query)
        return(result.fetchall())
    
print(connection())



