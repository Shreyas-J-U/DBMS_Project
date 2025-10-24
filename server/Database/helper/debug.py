import pymysql

def show_tables(cursor):

    cursor.execute("Show tables")
    results = cursor.fetchall()
    for row in results:
        print(row)


    