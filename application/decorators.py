from functools import wraps
from flask.ext.login import current_user
from flask import abort


def permission(model, name):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            obj = model.query.get(kwargs[name])
            if obj:
                print func.__name__
                if obj.owner_id == current_user.id:
                    kwargs['obj'] = obj
                    return func(*args, **kwargs)
                elif hasattr(obj, 'private') and not obj.private and func.__name__=='view':
                    kwargs['obj'] = obj
                    return func(*args, **kwargs)
                return abort(403)
            return abort(404)

        return inner

    return wrapper
