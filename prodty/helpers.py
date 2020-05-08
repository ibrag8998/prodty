from functools import wraps

from flask import render_template
from flask import request
from flask import g


def templated(template=None):
    def decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            template_name = template
            if template is None:
                template_name = request.endpoint.replace(
                    '.', '/') + '.html'

            ctx = func(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx

            return render_template(template_name, **ctx)
        return wrapper
    return decor


def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.signin'))
        return view(*args, **kwargs)
    return wrapper

