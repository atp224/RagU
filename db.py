import sqlite3

db_path = 'restaurants.db'

conn = sqlite3.connect(db_path)

select_sql = 'SELECT restaurant_name FROM restaurants'

with conn:
    cursor = conn.cursor()
    cursor.execute(select_sql)
    
    print("Restaurant Names:")
    for row in cursor.fetchall():
        print(row[0])  

