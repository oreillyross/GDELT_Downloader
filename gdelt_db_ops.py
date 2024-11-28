import sqlite3

conn = sqlite3.connect("gdelt_events.db")
cursor = conn.cursor()

cursor.execute('''
  create table if not exists keywords (
    name text not null,
    date_created text not null,
    criticality_score integer check(criticality_score >= 1 and criticality_score <= 5)
  )
  
''')

cursor.execute('''
  insert into keywords (name, date_created, criticality_score)
  values (?,?,?)
''', ("example_keyword", "2024-10-21", 4))

conn.commit()

cursor.execute("select * from keywords")

rows = cursor.fetchall()
for row in rows:
  print(row)

conn.close()