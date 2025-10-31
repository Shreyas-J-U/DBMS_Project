# auth_helpers.py
import os
import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app
import smtplib
from email.message import EmailMessage
import bcrypt

# config:
JWT_SECRET = os.getenv("JWT_SECRET", "change_this_secret")
JWT_ALGORITHM = "HS256"
JWT_EXP_DAYS = 7

def create_access_token(payload: dict, expires_days: int = JWT_EXP_DAYS):
    exp = datetime.datetime.utcnow() + datetime.timedelta(days=expires_days)
    payload_copy = payload.copy()
    payload_copy.update({"exp": exp})
    return jwt.encode(payload_copy, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return data
    except Exception:
        return None

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"success": False, "error": "Missing token"}), 401
        token = auth_header.split(" ", 1)[1].strip()
        data = decode_access_token(token)
        if not data:
            return jsonify({"success": False, "error": "Invalid/expired token"}), 401
        # Attach user info to request context
        request.user = data
        return fn(*args, **kwargs)
    return wrapper

def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            if not user:
                return jsonify({"success": False, "error": "Unauthorized"}), 401
            if user.get("role") not in allowed_roles:
                return jsonify({"success": False, "error": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Password helpers using bcrypt
def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False

# Simple email sender (smtplib). You can replace with Flask-Mail if you prefer.
def send_email_smtp(subject: str, body: str, to_email: str,
                    smtp_host: str, smtp_port: int, smtp_user: str, smtp_pass: str,
                    from_email: str = None):
    from_email = from_email or smtp_user
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.starttls()
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)
