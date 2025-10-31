import pymysql
from dotenv import load_dotenv
import os

_connection =None
_cursor = None
    
def get_connection_details():
    
    load_dotenv()

    mode = os.getenv("MODE")

    if(mode == "LOCAL"):
        print("Connecting to Local MySQL...")
        config={
            "host" : os.getenv("LOCAL_HOST", "127.0.0.1"),
            "port" : int(os.getenv("LOCAL_PORT", 3306)),
            "user" : os.getenv("LOCAL_USER", "root"),
            "password" : os.getenv("LOCAL_PASSWORD", ""),
            "db" : os.getenv("TRIAL"),
        }
    else:
        print("conecting to AIVEN database")
        config = {
            "charset": os.getenv("AIVEN_CHARSET", "utf8mb4"),
            "connect_timeout": int(os.getenv("AIVEN_CONNECT_TIMEOUT")),
            "cursorclass": pymysql.cursors.DictCursor, 
            "db": os.getenv("AIVEN_DB"),
            "host": os.getenv("AIVEN_HOST"),
            "password": os.getenv("AIVEN_PASSWORD"),
            "read_timeout": int(os.getenv("AIVEN_READ_TIMEOUT")),
            "port": int(os.getenv("AIVEN_PORT")),
            "user": os.getenv("AIVEN_USER"),
            "write_timeout": int(os.getenv("AIVEN_WRITE_TIMEOUT")),
            "autocommit" : False
        }
    if(mode == "AIVEN"):
        ca_path = os.getenv("AIVEN_CA_CERT_PATH")
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


