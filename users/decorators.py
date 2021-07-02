from functools import wraps

from django.shortcuts import redirect


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("users:login")
        return view_func(request, *args, **kwargs)

    return wrapper


def admin_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect("users:access-denied")
        return view_func(request, *args, **kwargs)

    return wrapper
