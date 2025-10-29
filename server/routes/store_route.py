from flask import Blueprint, request, jsonify
import database.connect as db_connect
from database.helper.stores import add_store
import pymysql



store_bp = Blueprint('store_bp', __name__)

@store_bp.route('/insert-store', methods=['POST'])
def insert_store_endpoint():

    try:
        data = request.get_json()

        store_name = data.get("store_name")
        store_location = data.get("location")
        manager_id = data.get("manager_id")



        if not all([store_name,store_location]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400
        

        store_data = (store_name,store_location,manager_id)
        db_resources = db_connect._connection,db_connect._cursor
        
        # add insert function here
        success = add_store(db_resources,store_data)
        


        return jsonify({
            "success": success
        }), 200 if success else 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500