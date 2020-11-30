from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

# is_authenticated + one of role from roles
# *roles -> [UserRole, ...]
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_authenticated and current_user.role in [role.value for role in roles]:
                return f(*args, **kwargs)
            return redirect(url_for('forbidden'))
        return decorated_function
    return decorator