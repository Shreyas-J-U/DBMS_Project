import pymysql
from pymysql import Error
from database.helper.authentication import *


def insert_employee_cred(db_resources,owner_cred):

    connection,cursor= db_resources
    

    try:

        if(len(owner_cred) == 5):

            query = """
                INSERT INTO employee (first_name, last_name, role, email, phone)
                VALUES (%s, %s, %s, %s, %s)
            """
        else:
            query = """
                INSERT INTO employee (first_name, last_name, role, email, phone,store_id)
                VALUES (%s, %s, %s, %s, %s, %s)
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
    

def get_all_unassigned_managers(db_resources):

    connection,cursor = db_resources
    try:
        query = """
            SELECT e.employee_id, e.first_name, e.last_name
            FROM employee e
            WHERE e.role = 'manager'
            AND e.employee_id NOT IN (
            SELECT s.manager_id FROM store s WHERE s.manager_id IS NOT NULL
            );
            """
        cursor.execute(query)
        result = cursor.fetchall()
        return (True,result)
    
    except Exception as e:
        print(e)
        return (False,None)
