"""User registration and password handling."""
import hashlib
from service.database import find_user_by_email

def hash_password(password, salt="prototype-salt"):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 120000).hex()

def register_user(connection, email, password, display_name):
    email = email.strip().lower()
    display_name = " ".join(display_name.split())
    if "@" not in email or len(password) < 10 or not display_name:
        raise ValueError("Email, a 10-character password, and display name are required")
    if find_user_by_email(connection, email):
        raise ValueError("An account with this email already exists")
    cursor = connection.execute("INSERT INTO users(email,password_hash,display_name) VALUES(?,?,?)",(email,hash_password(password),display_name))
    connection.commit()
    return cursor.lastrowid
