"""Application audit trail and structured event logging."""
import logging
logger = logging.getLogger("sample.audit")

def record_event(connection, user_id, action):
    if not action or len(action) > 100:
        raise ValueError("Invalid audit action")
    connection.execute("INSERT INTO audit_log(user_id, action) VALUES(?, ?)",(user_id,action))
    connection.commit()
    logger.info("audit action=%s user_id=%s", action, user_id)

def log_failed_login(email, remote_address):
    logger.warning("failed login email=%s remote=%s", email, remote_address)
