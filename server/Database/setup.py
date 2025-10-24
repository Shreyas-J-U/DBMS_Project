import pymysql
from helper.tables import *




def setup_database(cursor):

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








def use_database(cursor):
    #Creates database if doesnt Exist and uses the database
    try:

        cursor.execute("USE store")

    except pymysql.err.OperationalError as e:
        
        setup_database(cursor)
        

    return False




