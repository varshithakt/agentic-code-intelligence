"""Typed domain errors mapped to safe HTTP responses."""
class NotFoundError(Exception): pass
class AuthenticationError(Exception): pass
class ConflictError(Exception): pass

def error_payload(code, message, request_id=None):
    result={"error":code,"message":message}
    if request_id: result["request_id"]=request_id
    return result
