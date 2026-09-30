"""Minimal route handlers illustrating authentication and input validation."""
from service.auth import require_user
from service.input_cleaning import clean_display_name, normalize_email, parse_page_number
from service.registration import register_user

def get_profile(headers, connection):
    user_id=require_user(headers.get("authorization"))
    if not user_id:
        return {"status":401,"body":{"error":"authentication_required"}}
    return {"status":200,"body":{"user_id":user_id}}

def post_register(payload, connection):
    email=normalize_email(payload.get("email"))
    name=clean_display_name(payload.get("display_name"))
    try:
        user_id=register_user(connection,email,payload.get("password", ""),name)
        return {"status":201,"body":{"user_id":user_id}}
    except ValueError as exc:
        return {"status":400,"body":{"error":str(exc)}}

def list_events(query, connection):
    page=parse_page_number(query.get("page"),default=1)
    return connection.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT ? OFFSET ?",(20,(page-1)*20)).fetchall()
