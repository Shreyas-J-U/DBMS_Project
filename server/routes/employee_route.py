from flask import Blueprint, request, jsonify
from datetime import datetime
import database.connect as db_connect
from database.setup import insert_employee
from database.helper.employee import get_all_unassigned_managers,remove_employee_cred
from database.helper.employee import check_todays_attendance,employee_checkin,get_employee_id,get_total_hours,get_attendance_report
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

        #checkin for that day
        employee_id = get_employee_id(db_resources,user_name)
        if(employee_id == -1):
            print("Database error")
            #handle error
        elif(employee_id is None):
            print("Username not found")
            #handle missing values
        else:
            print(f"Employee ID is {employee_id}")
            employee_checkin(db_resources,employee_id)
            print("called employee checkin")


        return jsonify({
            "success": success
        }), 200 if success else 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    


@employee_bp.route('/remove-employee', methods=['POST'])
def remove_employee_endpoint():
    
    try:
        data = request.get_json()

        employee_id = data.get("employee_id")

        if(not employee_id):
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        db_resources = db_connect._connection,db_connect._cursor
        
        # add insert function here
        success =remove_employee_cred(db_resources,employee_id)
        
        return jsonify({
            "success": success
        }), 200 if success else 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500










@employee_bp.route('/unassigned-manager', methods=['GET'])
def get_unassigned_manager_endpoint():
    db_resources = db_connect._connection, db_connect._cursor
    success, result = get_all_unassigned_managers(db_resources)
    return jsonify({
        "success": success,
        "managers": result
    }), 200 if success else 500


@employee_bp.route('/get-total-hours',methods = ['GET'])
def get_total_hours_endpoint():
    
    data = request.get_json()
    
    employee_id = data.get("employee_id")
    work_date = data.get("date")

    if not all([employee_id,work_date]):
        return jsonify({"success": False, "error": "Missing required fields"}), 400
    
    try:
        work_date_obj = datetime.strptime(work_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"success": False, "error": "Invalid date format, expected YYYY-MM-DD"}), 400

    db_resources = db_connect._connection,db_connect._cursor
    success,result = get_total_hours(db_resources,employee_id,work_date_obj)

    return jsonify({
        "success": success,
        "result": result
    }), 200 if success else 500

@employee_bp.route('/get-attendance-report',methods = ['GET'])
def get_attendance_report_endpoint():
    
    data = request.get_json()
    
    store_id = data.get("store_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")


    if not all([store_id,start_date,end_date]):
        return jsonify({"success": False, "error": "Missing required fields"}), 400
    
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()

    except ValueError:
        return jsonify({"success": False, "error": "Invalid date format, expected YYYY-MM-DD"}), 400

    db_resources = db_connect._connection,db_connect._cursor
    success,result = get_attendance_report(db_resources,store_id,start_date,end_date)

    return jsonify({
        "success": success,
        "result": result
    }), 200 if success else 500