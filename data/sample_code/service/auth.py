"""Authentication and bearer-token validation."""
import hashlib
import hmac
import time

SECRET = "local-demo-secret"

def issue_token(user_id, ttl=3600):
    expires = int(time.time()) + ttl
    body = f"{user_id}:{expires}"
    signature = hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
    return f"{body}:{signature}"

def validate_token(token):
    """Validate expiry and HMAC signature for an incoming access token."""
    try:
        user_id, expires, signature = token.split(":", 2)
        body = f"{user_id}:{expires}"
        expected = hmac.new(SECRET.encode(), body.encode(), hashlib.sha256).hexdigest()
        if int(expires) < int(time.time()):
            return None
        if not hmac.compare_digest(signature, expected):
            return None
        return user_id
    except (ValueError, TypeError):
        return None

def require_user(authorization):
    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    return validate_token(authorization[7:].strip())
