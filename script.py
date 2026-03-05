import sqlite3 as db 

con = db.connect("data.db")
cursor = con.cursor()


sql_query = """
        SELECT
            c.id,
            c.name AS category_name,
            COALESCE(SUM(s.paid_price), 0) AS total_price,
            COUNT(s)
        FROM
            services_categories c
        LEFT JOIN
            services s
        ON
            s.category_id = c.id
        GROUP BY
            c.id, c.name 
        ORDER BY
            c.name;
    
"""
# cursor.execute(sql_query)
# rows = [row for row in cursor.fetchall()]
# for row in rows:
#     print(row)


a = ["a"]
print(a+["k"])