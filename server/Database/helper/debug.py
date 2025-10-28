import pymysql
from database.helper.authentication import *
import os
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
        
    
def run_sql_console(db_resources):
    connection, cursor = db_resources
    os.system("cls")
    print("Interactive SQL console. Type 'exit' to quit.")

    while True:
        try:
            input_str = input("--> ").strip()
            if input_str.lower() == "exit":
                print("Exiting SQL console.")
                break
            if input_str.lower() == "cls":
                os.system("cls")
                print("Interactive SQL console. Type 'exit' to quit.")
                continue
            
            if not input_str:
                continue  # skip empty input

            cursor.execute(input_str)

            # Try fetching results (works for SELECT and some other queries)
            try:
                result = cursor.fetchall()
                if result:
                    print("\n--- Query Results ---")
                    for row in result:
                        print(row)
                else:
                    print("No rows returned.")
            except Exception:
                # For queries that don't return data (INSERT/UPDATE/etc.)
                connection.commit()
                print("Query executed successfully (no result set).")

        except Exception as e:
            print(f"Error: {e}")


