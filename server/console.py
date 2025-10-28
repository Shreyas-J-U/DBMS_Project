import database.connect as db_connect
from database.setup import *
# debug code
from database.helper.debug import * 
import sys

'''
this script is used to connect to aiven database and run sql query in console
this is meant for testing and debugging and should not be included in final product
'''


try:

  db_resources = init_database()
  
  if(db_resources is None):
    print("Database connection failed")
    sys.exit(1)
  connection,cursor= db_resources
  

  

  run_sql_console(db_resources)
finally:
  print("closing connection")

  connection.close()