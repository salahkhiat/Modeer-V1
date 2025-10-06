import sqlite3 as db
from typing import List, Dict , Any
import os 

from .shared_functions import SharedFunctions

class DatabaseManager(SharedFunctions):
        
    def get_database_ref(self) -> str:
        """
        Return a full database reference.
        
        :return: A database path.
        :rtype: str

        :example:
            >>> obj.get_database_ref()
            "./database_path/database.db"
        """
        settings = self.get_settings()
        return os.path.join(settings["database_path"], settings["database_name"])
    
    def store(self, table_name:str, columns: list[str], data: tuple, last_row_id:bool=False )-> Any:
        """
        Insert data into a database table, return last_row_id if True.

        :param table_name: The name of the database table.
        :type table_name: str
        :param columns: A list of columns names.
        :type columns: list[str]
        :param data: A tuple of values.
        :type data: tuple
        :return: True or False If data inserted successfully or not, last_row_id if It was added as an Arg.
        :rtype: Any

        """
        connection = None 
        try:
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            
            # Prepare the SQL query
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

            cursor.execute(query,data)
            connection.commit()
            if last_row_id:
                return cursor.lastrowid
            else:
                return True
            
        except db.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            if connection:
                connection.close()

    def update_info(self, table_name: str, columns: list[str], data: tuple, where_clause: str, where_args: tuple = ()) -> bool:
        """
        Update data in a database table.

        :param table_name: The name of the database table.
        :type table_name: str
        :param columns: A list of column names to update.
        :type columns: list[str]
        :param data: A tuple of new values corresponding to the columns.
        :type data: tuple
        :param where_clause: SQL WHERE clause (e.g., "id = ?").
        :type where_clause: str
        :param where_args: Tuple of values for the WHERE clause placeholders.
        :type where_args: tuple
        :return: True if the update was successful, False otherwise.
        :rtype: bool

        Examples:
            >>># Update the 'name' and 'age' of the user where id=5
            >>>update('users', ['name', 'age'], ('Alice', 30), 'id = ?', (5,))
        """
        connection = None
        try:
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()

            # Prepare the SQL query
            set_clause = ', '.join([f"{col} = ?" for col in columns])
            query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            # Combine data for SET and WHERE
            full_data = data + where_args

            cursor.execute(query, full_data)
            connection.commit()

            return cursor.rowcount > 0  # True if any row was updated

        except db.Error as err:
            print(f"Database error: {err}")
            return False
        finally:
            if connection:
                connection.close()

    
    
    def is_in_table(self, table:str,column:str , target:str) -> bool:
        """
        Check from an item by condition if exists.
        
        Args:
            table (str): the table name.
            target (str): the item name you're looking for.
            column (str): the table column.
        Returns:
            bool : True if the item exists, and False otherwise.
        
        """
        conn = None
        try:
            conn = db.connect(self.get_database_ref())
            cursor = conn.cursor()
            query = f"SELECT 1 FROM {table} WHERE {column} = ? LIMIT 1"
            cursor.execute(query,(target,))
            result = cursor.fetchone()

            if result is not None:
                return True
            else:
                return False 

        except db.Error as err:
            print(f"database err:{err}")
        finally:
            if conn:
                conn.close()

    def search_by(self,table: str, column: str, keyword: str, target: str) -> Any:
        """
        Search for a single value in the database table based on a condition.

        :param table: Name of the database table.
        :type table: str
        :param column: Column to match against the keyword (used in WHERE).
        :type column: str
        :param keyword: The value to search for in the specified column.
        :type keyword: str
        :param target: The column whose value should be returned.
        :type target: str
        :return: The value of the target column if found, else None.
        :rtype: Any
        """
        connection = None
        try:
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()

            query = f"SELECT {target} FROM {table} WHERE {column} = ? LIMIT 1"
            cursor.execute(query, (keyword,))
            result = cursor.fetchone()

            if result:
                return result[0]
            else:
                return None

        except db.Error as err:
            print(f"Database error: {err}")
            return None
        finally:
            if connection:
                connection.close()


                     

    def create_default_column(self, table:str, column:str, name:str = "-") -> bool:
        """
        Creating a default column if not exists.

        Args:
            table (str): The table name.
            column (str): The column name.
            name (str):the default user name.
        Returns:
            bool: True if the name was created successfully, False otherwise.
        """
        is_exists = self.is_in_table(table,column,name)
        if is_exists is False:
            return self.store(table,[column],(name))
        else:
            return False
            

    
    def get_table_as_list(self, table:str, columns:List[str] ) -> List:
        """
        Returning table data as list.

        :param table: a table name.
        :type table: str
        :param columns: A list of columns names.
        :type columns: List[str]
        :return: A list rows.
        :rtype: List

        :examples:
            >>> table = "students"
            >>> columns = ["name","class","degree"]
            >>> obj.get_table_as_list(table,columns)
            ["Muhammed", "Nooh", "Adam" ]
        """
        con = None
        try:
            con = db.connect(self.get_database_ref())
            cursor = con.cursor()
            table_columns = ", ".join(columns)
            query = f"SELECT {table_columns} FROM {table}"
            data = cursor.execute(query).fetchall()
            new_data = [item[0] for item in data]
            return new_data
        
        except db.Error as err:
            print(f"database error: {err}")
            return False 
        finally:
            if con:
                con.close()
    
    def get_table_as_dict(self, table:str, column:str) -> Dict:
        """
        Returning table data as dictionary {"id":"column"}.
        
        Args:
            table (str): The table name.
            column (str): The table column.
        Returns:
            dict: Data as dictionary.
        Examples:
            >>> table = "student"
            >>> column = "name"
            >>> obj.get_table_as_dict(table,column)
            {1:"Muhammed", 2:"Ahmed"}
        """
        con = None
        try:
            con = db.connect(self.get_database_ref())
            cursor = con.cursor()
            
            query = f"SELECT id, {column} FROM {table}"
            data = cursor.execute(query).fetchall()

            new_data = {item[0]:item[1] for item in data}
            return new_data
        
        except db.Error as err:
            print(f"database error: {err}")
            return {} 
        finally:
            if con:
                con.close()
    
    def tel_exists(self,table: str, tel: str) -> bool:
        """
        Check if a telephone number exists in a specific table.

        :param table: Name of the table to search in.
        :type table: str
        :param tel: The telephone number to search for.
        :type tel: str
        :return: True if the telephone number exists, False otherwise.
        :rtype: bool

        :example:
            >>> obj.tel_exists("contacts", "1234567890")
            True
        """
        conn = None
        try:
            conn = db.connect(self.get_database_ref())
            cursor = conn.cursor()
            query = f"SELECT 1 FROM {table} WHERE tel = ? LIMIT 1"
            cursor.execute(query, (tel,))
            result = cursor.fetchone()
            return result is not None
        except db.Error as e:
            print(f"Database error: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def prepare_database(self,database_reference:str) -> bool:
        """
        Create a database and its tables if they not exists.
        
        :param database_reference: a full database path.
        :type database_reference: str
        :return: True if the database was prepared successfully.
        :rtype: bool
        
        :example:
            >>> db_ref = "./database_path/database.db"
            >>> obj.prepare_database(db_ref)
            True

        """
        
        conn = db.connect(database_reference)
        cursor = conn.cursor()

        # List of SQL commands to create each table
        create_tables_sql = [
            # Suppliers
            """
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tel TEXT
            );
            """,

            # Customers
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tel TEXT,
                type TEXT
            );
            """,

            # Employees
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tel TEXT
            );
            """,

            # Suppliers Invoices
            """
            CREATE TABLE IF NOT EXISTS purchase_invoices (
                id INTEGER PRIMARY KEY,
                supplier_id INTEGER NOT NULL,
                invoice_number TEXT,           -- Optional: unique invoice code
                total TEXT,
                deposit TEXT,
                created_at TEXT ,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
            );

            """,

            # Product
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                barcode TEXT,
                name TEXT NOT NULL,
                purchase_price REAL,
                sale_price REAL,
                quantity INTEGER,
                invoice_id INTEGER,
                is_deleted BOOLEAN DEFAULT 0,  -- Soft delete flag
                FOREIGN KEY (invoice_id) REFERENCES purchase_invoices(id)
            );

            """,

            # purchases_history
            """
            CREATE TABLE IF NOT EXISTS purchases_history (
                id INTEGER PRIMARY KEY,
                invoice_id INTEGER NOT NULL,
                product_id INTEGER,                 -- FK to products, nullable if you allow free-text items
                product_name TEXT NOT NULL,        -- Snapshot of name
                barcode TEXT,                      -- Optional snapshot of barcode
                quantity INTEGER NOT NULL,
                purchase_price REAL NOT NULL,      -- Snapshot of price at purchase time
                sale_price REAL,                   -- Optional: expected sale price
                total REAL GENERATED ALWAYS AS (quantity * purchase_price) STORED,  -- Auto-calculated
                FOREIGN KEY (invoice_id) REFERENCES purchase_invoices(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );

            """,

            # Customers Invoices
            """
            CREATE TABLE IF NOT EXISTS customers_invoices (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                sold_price REAL,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            );
            """,

            # Orders
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                invoice_id INTEGER,
                product_id INTEGER,
                product_name TEXT,
                unit_price REAL,
                sold_price REAL,
                quantity INTEGER,
                FOREIGN KEY (invoice_id) REFERENCES customers_invoices(id),
                FOREIGN KEY (product_id) REFERENCES product(id)
            );
            """,

            # Suppliers Transactions
            """
            CREATE TABLE IF NOT EXISTS suppliers_transactions (
                id INTEGER PRIMARY KEY,
                supplier_id INTEGER,
                invoice_id INTEGER,             -- ✅ NEW: optional link to a purchase invoice
                note TEXT,
                amount REAL,
                type TEXT,                      -- e.g., 'debt', 'deposit'
                created TEXT,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
                FOREIGN KEY (invoice_id) REFERENCES purchase_invoices(id)  -- ✅ new FK
            );

            """,

            # Employees Withdrawals
            """
            CREATE TABLE IF NOT EXISTS employees_withdrawals (
                id INTEGER PRIMARY KEY,
                employee_id INTEGER,
                note TEXT,
                amount REAL,
                created TEXT,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            );
            """,

            # Expenses Categories
            """
            CREATE TABLE IF NOT EXISTS expenses_categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            """,

            # Expenses
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                note TEXT,
                amount REAL,
                category_id INTEGER,
                created TEXT,
                FOREIGN KEY (category_id) REFERENCES expenses_categories(id)
            );
            """,

            # Services Categories
            """
            CREATE TABLE IF NOT EXISTS services_categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            """,

            # Services
            """
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                category_id INTEGER,
                description TEXT,
                default_price REAL,
                paid_price REAL,
                created TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (category_id) REFERENCES services_categories(id)
            );
            """,

            # Customers Payments
            """
            CREATE TABLE IF NOT EXISTS customers_payments (
                id INTEGER PRIMARY KEY,
                amount REAL,
                note TEXT,
                created TEXT
            );
            """,

            # Mobiles
            """
            CREATE TABLE IF NOT EXISTS mobiles (
                id INTEGER PRIMARY KEY,
                model TEXT,
                color TEXT,
                price REAL,
                serial TEXT,
                note TEXT,
                seller_name TEXT,
                seller_tel TEXT,
                seller_identify_id TEXT,
                document_type INTEGER,
                created TEXT,
                FOREIGN KEY (document_type) REFERENCES documents_types(id)
            );
            """,

            # Documents Types
            """
            CREATE TABLE IF NOT EXISTS documents_types (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            """,

            # Requested Products
            """
            CREATE TABLE IF NOT EXISTS requested_products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            """
        ]

        # Execute each create table statement
        for sql in create_tables_sql:
            cursor.execute(sql)

        # Commit changes and close connection
        conn.commit()
        conn.close()

        print("Database and tables created successfully.")
    