"""Validation helpers for user submitted fields."""
import re

def is_valid_email(value):
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+",(value or "").strip()))

def validate_password_strength(value):
    value=value or ""
    return len(value)>=10 and any(c.isdigit() for c in value) and any(c.isalpha() for c in value)

def validate_registration(payload):
    errors={}
    if not is_valid_email(payload.get("email")): errors["email"]="Enter a valid email address"
    if not validate_password_strength(payload.get("password")): errors["password"]="Use 10 characters with letters and digits"
    if not (payload.get("display_name") or "").strip(): errors["display_name"]="Display name is required"
    return errors

def require_valid_registration(payload):
    errors=validate_registration(payload)
    if errors: raise ValueError(errors)

def mask_email(value):
    local,sep,domain=(value or "").partition("@")
    return (local[:1]+"***"+sep+domain) if sep else "***"
