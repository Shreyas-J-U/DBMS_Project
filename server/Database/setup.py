import pymysql
from pymysql import Error
from helper.tables import *
from helper.employee import *
from helper.authentication import *



def setup_database(db_resources):

    connection,cursor = db_resources
    try:
        cursor.execute("CREATE DATABASE store")
        cursor.execute("USE store")
    
    #table creations
        create_employee_table(cursor)
        create_store_table(cursor)
        create_customer_table(cursor)
        create_product_category(cursor)
        create_supplier_table(cursor)
        create_order_table(cursor)
        create_product_table(cursor)
        create_inventory_transactions(cursor)
        create_payment_table(cursor)
        create_order_item_table(cursor)
        create_passwords_table(cursor)
        
    #commit changes    
        connection.commit()
        return True
    except Error as e:
        print(e)
        connection.rollback()
        return False
    




def use_database(db_resources):

    connection,cursor = db_resources
    #Creates database if doesnt Exist and uses the database
    try:

        cursor.execute("USE store")
        connection.commit()
        return True

    except pymysql.err.OperationalError as e:
        
        if(setup_database(db_resources)):
            return True
        

    return False

def create_owner(db_resources,owner_cred,user_name,password):

    
    # owner_cred = (id,fname,lname,role,email,phone)

    connection,cursor = db_resources
    result = insert_employee_cred(db_resources,owner_cred) 
    if(not result[0]):
        print("insertion failed")
        return False
    if(not store_hashed_passwords(db_resources,user_name,result[1],password)):
        print("hashing failed")
        return False
    return True

def login(db_resources,user_name,password):

    connection,cursor = db_resources
    query = """
        SELECT hash_pass FROM passwords 
        WHERE user_name = %s ;
        """
    cursor.execute(query,(user_name,))
    results = cursor.fetchone()
    if(not results):
        return False

    hashed_password = results['hash_pass']
    

    return verify_password(password,hashed_password)




