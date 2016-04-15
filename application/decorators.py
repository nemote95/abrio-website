from functools import wraps
from flask.ext.login import current_user
from flask import abort


def permission(model, name):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            obj = model.query.get(kwargs[name])
            if obj:
                if obj.owner_id == current_user.id or (hasattr(obj, 'private') and not obj.private):
                    kwargs['obj'] = obj
                    return func(*args, **kwargs)
                return abort(403)
            return abort(404)

        return inner

    return wrapper
