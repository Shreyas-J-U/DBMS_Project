import pymysql
from database.helper.authentication import *
def show_tables(cursor):

    cursor.execute("Show tables")
    cursor.execute(
        """

            select * from passwords;
        """
        )
    results = cursor.fetchall()
    for row in results:
        print(row)

def delete_database(db_resources):
    connection,cursor = db_resources

    cursor.execute("Drop database store")
    connection.commit()

def check_database_owner_cred(db_resources):

    connection,cursor = db_resources

    cursor.execute(
        """

            select * from passwords;
        """
        )
    results = cursor.fetchall()
    print(results)
    hashed_password = results[0]['hash_pass']

    print(verify_password("pass123",hashed_password))
        
    