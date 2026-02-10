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

    def search_by(self, table: str, column: str, keyword: str, target: str) -> Any:
        """
        Search for a single value in the database table based on a condition.
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






    """

    
    """
    
    def get_item_info(self, table: str, columns: tuple, keyword: str, target) -> dict | None:
        """
        Fetch a single row from a database table where a specific column matches a target value.

        Args:
            table (str): Name of the table (e.g. "products")
            columns (tuple): Columns to retrieve (e.g. ("barcode", "sale_price", "quantity"))
            keyword (str): The column used in the WHERE condition (e.g. "barcode" or "id")
            target: The value to match in the keyword column (e.g. 3434)

        Returns:
            dict | None: A dictionary representing one row, or None if not found.

            Examples:
                >>> table = "products"
                >>> columns = ("barcode", "sale_price", "quantity", "name")
                >>> keyword = "barcode"
                >>> target = 3434
                >>> item = obj.get_item_info(table, columns, keyword, target)
        """
        connection = None
        try:
            # connect to database
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()

            # dynamically construct query
            cols_str = ", ".join(columns)
            query = f"SELECT {cols_str} FROM {table} WHERE {keyword} = ? LIMIT 1"

            cursor.execute(query, (target,))
            row = cursor.fetchone()

            if row:
                # return a dictionary {column_name: value}
                return {col: val for col, val in zip(columns, row)}
            else:
                return None

        except db.Error as err:
            print(f"Database error: {err}")
            return None

        finally:
            if connection:
                connection.close()


    def search_by_similar(self, table: str, column: str, keyword: str, target: List[str]) -> List[Dict[str, Any]]:
        """
        Search for rows in a table where a column starts with a given keyword.
        Returns a list of dictionaries with the specified target columns.

        :param table: Name of the table to search
        :param column: Column to perform the LIKE search on
        :param keyword: The prefix keyword to search for
        :param target: List of columns to retrieve in the result
        :return: List of dictionaries with the requested columns
        """
        # if not keyword.strip():  # prevent empty or whitespace-only searches
        #     return []
        connection = None
        try:
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()

            # Build the SELECT part dynamically from target list
            target_columns = ', '.join(target)
            # Query with parameterized LIKE for prefix search
            query = f"SELECT {target_columns} FROM {table} WHERE {column} LIKE ? "
            cursor.execute(query, (f"%{keyword}%",))
            rows = cursor.fetchall()

            # Convert result rows to list of dicts
            results = []
            for row in rows:
                row_dict = dict(zip(target, row))
                results.append(row_dict)

            return results

        except db.Error as err:
            print(f"Database error: {err}")
            return []
        finally:
            if connection:
                connection.close()

    def is_db_table_empty(self, table: str) -> bool:
        """
        Check if a database table is empty.

        :param table: Name of the database table to check.
        :type table: str
        :return: True if the table is empty, False otherwise.
        :rtype: bool
        """
        connection = None
        try:
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()

            query = f"SELECT 1 FROM {table} LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return False  # Table has at least one row
            else:
                return True   # Table is empty

        except db.Error as err:
            print(f"Database error: {err}")
            return False  # Default to False if there's an error (fail-safe)
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

    def get_table_cols_list(self, table:str, columns:List[str], where_clause:str=None, parms: tuple=()) -> List:
   
        con = None
        try:
            con = db.connect(self.get_database_ref())
            cursor = con.cursor()
            query = f"SELECT {','.join(columns)} FROM {table}" 
            if  where_clause:
                query += f" WHERE {where_clause}"
            
            return cursor.execute(query, parms).fetchall()
        
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

    def get_sales_income(self,s_date:str="today") -> float:
        """
        Calculate total sales income based on conditional rules.

        Rules:
        - If customer_id == 1:
            - If deposit == 0 → use total
            - If deposit > 0 → use deposit
        - If customer_id != 1:
            - Always use deposit

        :return: Calculated sales income.
        :rtype: float
        """
        connection = None
        try:
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            created = self.current_date() # 1447-06-01
            if s_date == "month":
                created = self.current_date()[:7] # 1447-06

            query = """
                SELECT SUM(
                    CASE
                        WHEN customer_id = 1 AND deposit = 0 THEN total
                        WHEN customer_id = 1 AND deposit > 0 THEN deposit
                        ELSE deposit
                    END
                )
                FROM sale_invoices
                WHERE created_at LIKE ?

            """
            cursor.execute(query,(f"{created}%",))
            result = cursor.fetchone()

            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()


    def get_services_income(self,s_date:str="today") -> float:
        """
        Calculate total services income based on conditional rules.

        """
        connection = None
        try: 
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            created = self.current_date() # 1447-06-01
            if s_date == "month":
                created = self.current_date()[:7] # 1447-06

            query = """
                SELECT SUM(
                    CASE
                        WHEN customer_id = 1  THEN default_price
                        ELSE paid_price
                    END
                )
                FROM services
                WHERE created LIKE ? 
            """
            cursor.execute(query,(f"{created}%",))
            result = cursor.fetchone()

            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()

    def get_sales_capital(self,s_date:str="today") -> float:
        """
        Calculate total sales capital (sum of invoice capitals) for the current month.
        """
        connection = None
        try:
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()

            created = self.current_date() # 1447-06-01
            if s_date == "month":
                created = self.current_date()[:7] # 1447-06

            query = """
                SELECT SUM(sh.purchase_price * sh.quantity)
                FROM sales_history sh
                JOIN sale_invoices si ON si.id = sh.invoice_id
                WHERE si.created_at LIKE ?
            """
            cursor.execute(query, (f"{created}%",))
            result = cursor.fetchone()

            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0

        finally:
            if connection:
                connection.close()

    def get_expenses(self,s_date:str="today") -> float:
        """
        Calculate total expenses  based on conditional rules.

        """
        connection = None
        try: 
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            created = self.current_date() # 1447-06-01
            if s_date == "month":
                created = self.current_date()[:7] # 1447-06

            query = """
                SELECT SUM(amount)
                FROM expenses
                WHERE created LIKE ? 
            """
            cursor.execute(query,(f"{created}%",))
            result = cursor.fetchone()

            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()

    def get_suppliers_deposits(self,s_date:str="today") -> float:
        """
        Calculate deposits to suppliers  based on conditional rules.

        """
        connection = None
        try: 
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            created = self.current_date() # 1447-06-01
            if s_date == "month":
                created = self.current_date()[:7] # 1447-06

            query = """
                SELECT SUM(
                    CASE
                          WHEN type = 'deposit' THEN amount
                    END
                )
                FROM suppliers_transactions
                WHERE created LIKE ? 
            """
            cursor.execute(query,(f"{created}%",))
            result = cursor.fetchone()

            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()
                
    def get_suppliers_debts(self,s_date:str="today") -> float:
        """
        Calculate deposits to suppliers  based on conditional rules.

        """
        connection = None
        try: 
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            created = self.current_date() # 1447-06-01
            if s_date == "month":
                created = self.current_date()[:7] # 1447-06

            query = """
                SELECT SUM(
                    CASE
                          WHEN type = 'debt' THEN amount
                    END
                )
                FROM suppliers_transactions
                WHERE created LIKE ? 
            """
            cursor.execute(query,(f"{created}%",))
            result = cursor.fetchone()

            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()

    def get_purchases_deposits(self,s_date:str="today") -> float:
        """
        Calculate deposits to suppliers  based on purchase_invoices and conditional rules.

        """
        connection = None
        try: 
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            created = self.current_date() # 1447-06-01
            if s_date == "month":
                created = self.current_date()[:7] # 1447-06

            query = """
                SELECT SUM(deposit)
                FROM purchase_invoices
                WHERE created_at LIKE ? 
            """
            cursor.execute(query,(f"{created}%",))
            result = cursor.fetchone()

            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()

    def get_customers_payments(self,s_date:str="today") -> float:
        """
        Calculate total customer_payments  based on conditional rules.

        """
        connection = None
        try: 
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            created = self.current_date() # 1447-06-01
            if s_date == "month":
                created = self.current_date()[:7] # 1447-06
            

            query = """
                SELECT SUM(amount)
                FROM customers_payments
                WHERE created LIKE ?
            """
            cursor.execute(query,(f"{created}%",))
            result = cursor.fetchone()

            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()

    def get_employees_withdrawals(self,s_date:str="today") -> float:
        """
        Calculate total employees_withdrawals  based on conditional rules.

        """
        connection = None
        try: 
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            created = self.current_date() # 1447-06-01
            if s_date == "month":
                created = self.current_date()[:7] # 1447-06
            

            query = """
                SELECT SUM(amount)
                FROM employees_withdrawals
                WHERE created LIKE ?
            """
            cursor.execute(query,(f"{created}%",))
            result = cursor.fetchone()

            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()
    
    def get_supplier_transactions_sum(self, tran_type: str, user_id: int) -> float:
        connection = None
        try: 
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            query = """
                SELECT SUM(amount)
                FROM suppliers_transactions
                WHERE type = ?
                AND supplier_id = ? 
            """
            cursor.execute(query,(tran_type, user_id))
            result = cursor.fetchone()
            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()

    def get_supplier_purchase_sum(self, col_name: str, user_id: int) -> float:
        connection = None
        try: 
            connection = db.connect(self.get_database_ref())
            cursor = connection.cursor()
            query = f"""
                SELECT SUM({col_name})
                FROM purchase_invoices
                WHERE supplier_id = ? 
            """
            cursor.execute(query,(user_id,))
            result = cursor.fetchone()
            
            return result[0] if result and result[0] is not None else 0.0

        except db.Error as err:
            print(f"Database error: {err}")
            return 0.0  # Fail-safe default

        finally:
            if connection:
                connection.close()

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
                tel TEXT,
                is_deleted BOOLEAN DEFAULT 0
            );
            """,

            # Customers
            """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tel TEXT,
                is_deleted BOOLEAN DEFAULT 0
            );
            """,

            # Employees
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                tel TEXT,
                is_deleted BOOLEAN DEFAULT 0
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
            CREATE TABLE IF NOT EXISTS sale_invoices (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                invoice_number TEXT,           -- Optional: unique invoice code
                total TEXT,
                deposit TEXT,
                created_at TEXT ,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
            );
            """,

            # Sales History
            """
            CREATE TABLE IF NOT EXISTS sales_history (
                id INTEGER PRIMARY KEY,
                invoice_id INTEGER NOT NULL,
                product_id INTEGER,                 -- FK to products, nullable if you allow free-text items
                product_name TEXT NOT NULL,        -- Snapshot of name
                barcode TEXT,                      -- Optional snapshot of barcode
                quantity INTEGER NOT NULL,
                purchase_price REAL NOT NULL,      -- Snapshot of price at sale time
                sale_price REAL,                   -- Optional: expected sale price
                total REAL GENERATED ALWAYS AS (quantity * sale_price) STORED,  -- Auto-calculated
                FOREIGN KEY (invoice_id) REFERENCES sale_invoices(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
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
                customer_id INTEGER,
                amount REAL,
                note TEXT,
                created TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(id)
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
                name TEXT NOT NULL,
                created TEXT
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
    