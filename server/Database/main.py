from connect import connect
from setup import *
# debug code
from helper.debug import * 





connection = None
try:

  connection = connect()
  cursor = connection.cursor()
  db_resources = (connection,cursor)
  

  if(not use_database(db_resources)):
    print("failed database creation")

  
finally:
  show_tables(cursor)

  connection.close()