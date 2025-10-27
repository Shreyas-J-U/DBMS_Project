from connect import connect
from setup import *
# debug code
from helper.debug import * 





connection = None
try:

  connection = connect()
  cursor = connection.cursor()
  db_resources = (connection,cursor)
  
  # delete_database(db_resources)

  if(not use_database(db_resources)):
    print("failed database creation")

  # testing owner creation :-
  # owner_cred = (id,fname,lname,email,phone)
  owner_cred = ("Shub","Jain","owner","Shu360zbham@gmail.com",999999999)
  my_password = "pass123"
  if(create_owner(db_resources,owner_cred,"shub jain",my_password)):
    print("owner created")
  else:
    print("Owner creation failed")

  if(login(db_resources,"shub jain","pass123")):
    print("correct password")
  else:
    print("incorrect password")
  
finally:
  show_tables(cursor)

  connection.close()