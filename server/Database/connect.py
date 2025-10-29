import pymysql
from dotenv import load_dotenv
import os

_connection =None
_cursor = None
    
def get_connection_details():
    
    load_dotenv()

    config = {
        "charset": os.getenv("CHARSET", "utf8mb4"),
        "connect_timeout": int(os.getenv("CONNECT_TIMEOUT")),
        "cursorclass": pymysql.cursors.DictCursor, 
        "db": os.getenv("DB"),
        "host": os.getenv("HOST"),
        "password": os.getenv("PASSWORD"),
        "read_timeout": int(os.getenv("READ_TIMEOUT")),
        "port": int(os.getenv("PORT")),
        "user": os.getenv("USER"),
        "write_timeout": int(os.getenv("WRITE_TIMEOUT")),
        "autocommit" : False
    }
    ca_path = os.getenv("CA_CERT_PATH")
    print(ca_path)
    if ca_path and os.path.exists(ca_path):
        config["ssl"] = {"ca": ca_path}
    else:
        print("not found")
        print("Warning: CA certificate not found or not specified. SSL verification may fail.")
    
    return config    


def connect():
    # connects to AIVEN datbase and returns the connection variable
    global _connection,_cursor
    config = get_connection_details()
    _connection = pymysql.connect(**config)    
    _cursor = _connection.cursor()


    return _connection,_cursor


