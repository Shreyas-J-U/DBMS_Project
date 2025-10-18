from connect import *

connection = None
try:
  connection = connect()
  cursor = connection.cursor()
  cursor.execute("show databases")
  #cursor.execute("")
  #cursor.execute("")
  print(cursor.fetchall())
finally:
  connection.close()