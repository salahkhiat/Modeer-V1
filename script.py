import sqlite3 as db 

con = db.connect("shop_data.db")
cursor = con.cursor()


sql_query = """
ALTER TABLE expenses_categories
ADD COLUMN is_deleted BOOLEAN DEFAULT 0;
    
"""
cursor.execute(sql_query)
# rows = [row for row in cursor.fetchall()]
# for row in rows:
#     print(row)


a = ["a"]
print(a+["k"])