"""Role based access checks for service operations."""
ROLE_PERMISSIONS={"viewer":{"profile:read"},"editor":{"profile:read","profile:write"},"admin":{"profile:read","profile:write","users:manage"}}

def permissions_for(role):
    return ROLE_PERMISSIONS.get((role or "").strip().lower(),set())

def can_perform(role, action):
    return action in permissions_for(role)

def require_permission(role, action):
    if not can_perform(role,action):
        raise PermissionError(f"Role {role!r} cannot perform {action!r}")

def visible_user_fields(role):
    fields={"id","display_name"}
    if can_perform(role,"users:manage"):
        fields.add("email")
    return fields

def filter_user_record(record, role):
    allowed=visible_user_fields(role)
    return {key:value for key,value in record.items() if key in allowed}
