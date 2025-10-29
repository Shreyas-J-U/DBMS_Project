from flask import Blueprint, request, jsonify
import database.connect as db_connect
from database.setup import insert_employee
import pymysql

employee_bp = Blueprint('employee_bp', __name__)


@employee_bp.route('/insert-employee', methods=['POST'])
def insert_employee_endpoint():
    #used for adding new employees or manager
    try:
        data = request.get_json()

        fname = data.get("fname")
        lname = data.get("lname")
        email = data.get("email")
        phone = data.get("phone")
        role = data.get("role")
        user_name = data.get("user_name")
        password = data.get("password")
        store_id = data.get("store_id")

        if not all([fname, lname, email, phone ,role,store_id, user_name, password]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        
        if(role not in ("employee","manager") ):
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        employee_cred = (fname, lname, role, email, phone,store_id)
        db_resources = db_connect._connection,db_connect._cursor
        
        # add insert function here
        success = insert_employee(db_resources,employee_cred,user_name,password)
        


        return jsonify({
            "success": success
        }), 200 if success else 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    
