import mysql.connector

cnx = mysql.connector.connect(
  user="", password="", host="", 
database="")
print("connected ok")
cnx.close()