import pymysql

import bcrypt

def hash_password(plain_password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.
    Returns the hashed password as a UTF-8 string.
    """
    salt = bcrypt.gensalt(rounds=12)  # 12 = good security vs. speed balance
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a stored bcrypt hash.
    Returns True if password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
