from functools import wraps

from flask import render_template
from flask import request
from flask import g
from flask import redirect
from flask import url_for


def to_index():
    """ For short """
    return redirect(url_for('index'))


def templated(_func=None, *, t=None):
    """
    Specifies template for the view

    >>> @templated
    ... def view(): return {'form': form}

    will use endpoint.replace('.', '/') + '.html' template,
    in this case 'view.html', and pass dict that view returns
    to the template. You can also specify template:

    >>> @templted(t='index.html')
    ... def home(): return {}

    Please, note, template must be keyword argument.

    Of course, you don't have to return dict everywhere.
    You can return redirect(...) as well as other non-dict
    values.
    """
    def decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            template_name = t
            # no template passed, use default
            if t is None:
                template_name = request.endpoint.replace(
                    '.', '/') + '.html'

            ctx = func(*args, **kwargs)
            # None returned, make {}
            if ctx is None:
                ctx = {}
            # if non-dict value returned
            elif not isinstance(ctx, dict):
                return ctx

            # render template and pass context
            return render_template(template_name, **ctx)
        return wrapper

    # @templated(t='signin.html') was called with args,
    # means _func is None, return decorator
    if _func is None:
        return decor
    # @templated was called without parenthesis,
    # it means _func is not None, so return wrapper
    else:
        return decor(_func)

