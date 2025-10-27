import pymysql
from dotenv import load_dotenv
import os

    
def get_connection_details():
    
    load_dotenv()
    return {
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


def connect():
    # connects to AIVEN datbase and returns the connection variable
    
    config = get_connection_details()
    connection = pymysql.connect(**config)
    return connection


