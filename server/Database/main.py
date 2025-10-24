from connect import connect
from setup import *

# debug code
from helper.debug import * 

connection = None
try:

  connection = connect()
  cursor = connection.cursor()
  use_database(cursor)


finally:
  show_tables(cursor)
  connection.close()