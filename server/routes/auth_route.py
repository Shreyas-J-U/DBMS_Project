from flask import Blueprint, request, jsonify
import database.connect as db_connect
from database.setup import create_owner,login
from database.helper.employee import check_todays_attendance,employee_checkin,employee_checkout,get_employee_id
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
        #update attendance :-
        employee_id = get_employee_id(db_resources,username)
        if(employee_id == -1):
            print("Database error")
            #handle error
        elif(employee_id is None):
            print("Username not found")
            #handle missing values
        else:
            print(f"Employee ID is {employee_id}")
            if(not check_todays_attendance(db_resources,employee_id)):
                employee_checkin(db_resources,employee_id)



        return jsonify({
            "success": success
        }),200 if success else 500
    except Exception as e:
        return jsonify({
            "success" : False,
            "error" : str(e)
        }),500


@auth_bp.route('/logout-user',methods = ['POST'])
def logout_endpoint():
    try:
        data = request.get_json()
        username = data.get("username")
        

        if not all ([username]):
            return jsonify({"success" : False,"error": "Missing required fields"}),400

        db_resources=db_connect._connection,db_connect._cursor
        #update attendance :-
        employee_id = get_employee_id(db_resources,username)
        success = False
        if(employee_id == -1):
            print("Database error")
            #handle error
        elif(employee_id is None):
            print("Username not found")
            #handle missing values
        else:
            print(f"Employee ID is {employee_id}")
            if(not check_todays_attendance(db_resources,employee_id)):
               success=employee_checkout(db_resources,employee_id)



        return jsonify({
            "success": success
        }),200 if success else 500
    except Exception as e:
        return jsonify({
            "success" : False,
            "error" : str(e)
        }),500

