import pymysql
from pymysql import Error
from database.helper.authentication import *


def insert_employee_cred(db_resources,owner_cred):

    connection,cursor= db_resources

    try:
        query = """
            INSERT INTO employee (first_name, last_name, role, email, phone)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, owner_cred)
        connection.commit()
        new_id = cursor.lastrowid
        return (True,new_id)

    except Error as e:
        print(e)
        connection.rollback()
        return (False,-1)

def store_hashed_passwords(db_resources,user,id,raw_password) -> bool:

    connection,cursor=db_resources
    hash_pass = hash_password(raw_password)
    query = """
        insert into passwords(user_name,employee_id,hash_pass) values(
            %s,
            %s,
            %s
            );
        """
    try : 
        cursor.execute(query,(user,id,hash_pass))
        connection.commit()
        return True
    except Error as e:
        print(e)
    
        connection.rollback()
        return False