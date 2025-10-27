from flask import Flask, jsonify, request
import pymysql
from Database.setup import *


app = Flask(__name__)

# --- init ---
db_resources = init_database()
if(db_resources == None):
    pass
connection,cursor= db_resources


# --- create a REST endpoint ---
@app.route('/create-owner', methods=['POST'])
def create_owner_endpoint():
    try:
        data = request.get_json()

        fname = data.get("fname")
        lname = data.get("lname")
        email = data.get("email")
        phone = data.get("phone")
        user_name = data.get("user_name")
        password = data.get("password")

        if not all([fname, lname, email, phone, user_name, password]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        owner_cred = (fname, lname, "owner", email, phone)

        success = create_owner(db_resources,owner_cred,user_name,password)

        return jsonify({
            "success": success
        }), 200 if success else 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/login-user',methods = ['POST'])
def login_endpoint():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not all ([username,password]):
            return jsonify({"success" : False,"error": "Missing required fields"}),400

        success = login(db_resources,username,password)

        return jsonify({
            "success": success
        }),200 if success else 500
    except Exception as e:
        return jsonify({
            "success" : False,
            "error" : str(e)
        }),500


# --- run the app ---
if __name__ == '__main__':
    app.run(debug=True)
