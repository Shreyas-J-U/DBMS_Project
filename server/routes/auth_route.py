from flask import Blueprint, request, jsonify
import database.connect as db_connect
from database.setup import create_owner,login
import pymysql

auth_bp = Blueprint('auth_bp', __name__)



@auth_bp.route('/create-owner', methods=['POST'])
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
        db_resources = db_connect._connection,db_connect._cursor
        success = create_owner(db_resources,owner_cred,user_name,password)

        return jsonify({
            "success": success
        }), 200 if success else 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    

@auth_bp.route('/login-user',methods = ['POST'])
def login_endpoint():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not all ([username,password]):
            return jsonify({"success" : False,"error": "Missing required fields"}),400

        db_resources=db_connect._connection,db_connect._cursor
        success = login(db_resources,username,password)

        return jsonify({
            "success": success
        }),200 if success else 500
    except Exception as e:
        return jsonify({
            "success" : False,
            "error" : str(e)
        }),500
