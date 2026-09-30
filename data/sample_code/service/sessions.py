"""In-memory session lifecycle and timeout handling."""
import time

def create_session(user_id, ttl=3600):
    return {"user_id": user_id, "created_at": time.time(), "expires_at": time.time()+ttl}

def session_is_valid(session, now=None):
    now = now or time.time()
    return bool(session and session.get("user_id") and session.get("expires_at", 0) > now)

def refresh_session(session, ttl=3600):
    if not session_is_valid(session):
        raise ValueError("Cannot refresh an expired session")
    session["expires_at"] = time.time()+ttl
    return session

def revoke_session(session):
    if session is not None:
        session.clear()

def session_remaining_seconds(session, now=None):
    if not session_is_valid(session, now):
        return 0
    return max(0, int(session["expires_at"]-(now or time.time())))
