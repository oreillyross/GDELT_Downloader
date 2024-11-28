import re
import sqlite3

conn = sqlite3.connect('gdelt.db')
cursor = conn.cursor()

create_table_query = """
  CREATE TABLE IF NOT EXISTS countries(
      code TEXT PRIMARY KEY,
      name TEXT NOT NULL
  )
"""

cursor.execute(create_table_query)

with open("utils/CAMEO.country.txt", 'r') as file:
    content = file.read()

countries = re.findall(r'(\w{3})\s(.+?)(?=\s\w{3}\s|$)', content)

insert_query = "INSERT OR REPLACE INTO countries (code, name) VALUES (?, ?)"
    
cursor.executemany(insert_query, countries)

conn.commit()
conn.close()

print("Countries added successfully")



