import sqlite3 as db 

con = db.connect("data.db")
cursor = con.cursor()
query = """ 
    SELECT name, amount, deposit
    FROM suppliers
    JOIN suppliers_transactions
        ON suppliers.id = suppliers_transactions.supplier_id
    JOIN purchase_invoices
        ON purchase_invoices.supplier_id = suppliers.id
    """

cursor.execute(query)
rows = [row for row in cursor.fetchall()]
for row in rows:
    print(row)