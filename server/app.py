from flask import Flask, jsonify, request
import pymysql
from database.setup import *
from routes.auth_route import auth_bp
import sys

# --- init ---

app = Flask(__name__)
db_resources = init_database()
if(db_resources is None):
    print("Database connection failed")
    sys.exit(1)
connection,cursor= db_resources


# --- create a REST endpoint ---
app.register_blueprint(auth_bp)




# --- run the app ---
if __name__ == '__main__':
    app.run(debug=True)
