from functools import wraps

from flask import session, redirect, url_for


def role_required(role):

    def wrapper(func):

        @wraps(func)
        def decorated(*args, **kwargs):

            if "role" not in session:
                return redirect(url_for("auth.login"))

            if session["role"] != role:
                return "Access Denied", 403

            return func(*args, **kwargs)

        return decorated

    return wrapper