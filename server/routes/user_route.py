# user_route.py
from flask import Blueprint, request, jsonify, current_app
import database.connect as db_connect
from auth_helpers import auth_required, role_required, create_access_token, hash_password, send_email_smtp
import database.helper.authentication as auth_helper  # if you have it

user_bp = Blueprint('user_bp', __name__)


# Register (creates approval request, does NOT create employee record yet)
@user_bp.route('/register', methods=['POST'])
def register():
    """
    body: { fname, lname, email, phone, designation (manager|staff|supplier), username, password, store_id(optional) }
    """
    data = request.get_json()
    fname = data.get("fname"); lname = data.get("lname")
    email = data.get("email"); phone = data.get("phone")
    designation = data.get("designation")
    username = data.get("username"); password = data.get("password")
    store_id = data.get("store_id")

    if not all([fname, lname, email, phone, designation, username, password]):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    if designation not in ("manager", "staff", "supplier"):
        return jsonify({"success": False, "error": "Invalid designation"}), 400

    conn, cursor = db_connect._connection, db_connect._cursor

    # Save into an 'approval_requests' table until owner approves
    try:
        query = """
        INSERT INTO approval_requests
        (fname, lname, email, phone, designation, username, password_hash, store_id, created_at, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW(),'pending')
        """
        hashed = hash_password(password)
        cursor.execute(query,
                       (fname, lname, email, phone, designation, username, hashed, store_id))
        conn.commit()
        return jsonify({"success": True}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500


# List pending approvals (owner only)
@user_bp.route('/pending', methods=['GET'])
@auth_required
@role_required("owner")
def list_pending():
    conn, cursor = db_connect._connection, db_connect._cursor
    cursor.execute("SELECT id, fname, lname, email, phone, designation, username, store_id, created_at FROM approval_requests WHERE status='pending'")
    rows = cursor.fetchall()
    return jsonify({"success": True, "pending": rows}), 200


# Approve request (owner only)
@user_bp.route('/approve/<int:request_id>', methods=['POST'])
@auth_required
@role_required("owner")
def approve_request(request_id):
    conn, cursor = db_connect._connection, db_connect._cursor

    try:
        # fetch request
        cursor.execute("SELECT * FROM approval_requests WHERE id=%s AND status='pending'", (request_id,))
        req = cursor.fetchone()
        if not req:
            return jsonify({"success": False, "error": "Not found"}), 404

        # insert into employees / suppliers table depending on designation
        designation = req['designation']
        username = req['username']
        password_hash = req['password_hash']  # hashed already
        fname = req['fname']; lname = req['lname']; email = req['email']; phone = req['phone']; store_id = req['store_id']

        # Insert into employees table
        if designation in ("manager", "staff"):
            insert_q = """
            INSERT INTO employees (fname, lname, role, email, phone, store_id, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,NOW())
            """
            cursor.execute(insert_q, (fname, lname, designation, email, phone, store_id))
            emp_id = cursor.lastrowid

            # store hashed password in passwords table
            cursor.execute("INSERT INTO passwords (user_name, employee_id, hash_pass) VALUES (%s,%s,%s)",
                           (username, emp_id, password_hash))
        else:
            # supplier - optional separate table
            insert_q = """
            INSERT INTO suppliers (name, email, phone, created_at)
            VALUES (%s,%s,%s,NOW())
            """
            supplier_name = f"{fname} {lname}"
            cursor.execute(insert_q, (supplier_name, email, phone))
            supplier_id = cursor.lastrowid

            cursor.execute("INSERT INTO passwords (user_name, supplier_id, hash_pass) VALUES (%s,%s,%s)",
                           (username, supplier_id, password_hash))

        # mark request approved
        cursor.execute("UPDATE approval_requests SET status='approved', processed_at=NOW() WHERE id=%s", (request_id,))

        conn.commit()

        # send email to user with credentials (or a link to reset password)
        smtp_cfg = current_app.config.get("SMTP", {})
        try:
            subject = "Your account is approved"
            body = f"Hello {fname},\n\nYour account has been approved. You can log in with username: {username}\nPlease change your password after first login.\n"
            send_email_smtp(subject, body, email,
                            smtp_cfg.get("HOST"), smtp_cfg.get("PORT"),
                            smtp_cfg.get("USER"), smtp_cfg.get("PASS"),
                            smtp_cfg.get("FROM"))
        except Exception as e_mail:
            # log but do not fail approval
            current_app.logger.exception("Failed to send approval email: %s", e_mail)

        return jsonify({"success": True}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
