import sqlite3 as db 

con = db.connect("data.db")
cursor = con.cursor()


sql_query = """
    SELECT * FROM
    ( 
        SELECT
            c.name AS name,
            'payment' AS type,
            p.note AS description,
            p.amount AS amount, 
            p.created AS created
        FROM 
            customers_payments p 
        JOIN
            customers c 
        ON 
            p.customer_id = c.id 
        WHERE 
            c.id != 1
        
        UNION ALL 

        SELECT
            c.name AS name,
            'service' AS type,
            s.description AS description,
            s.paid_price AS amount,
            s.created AS created
        FROM 
            customers c
        JOIN 
            services s 
        ON 
            c.id = s.customer_id
        WHERE
            c.id != 1
        
        UNION ALL
        SELECT
            c.name AS name,
            'sale' AS type,
            si.invoice_number AS description,
            si.deposit AS amount,
            si.created_at AS created
        FROM
            customers c
        JOIN
            sale_invoices si
        ON
            c.id = si.customer_id
        WHERE 
            c.id != 1
            
    ) AS compined 
    WHERE 
        amount > 0 
    AND 
        created LIKE '%02'

"""
cursor.execute(sql_query)
rows = [row for row in cursor.fetchall()]
for row in rows:
    print(row)