from functools import wraps
from flask.ext.login import current_user
from flask import abort
from application.models.enums import Abilities


def permission(model, name):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            obj = model.query.get(kwargs[name])
            if obj and current_user.has_ability(Abilities.TYPICAL):
                if obj.owner_id == current_user.id:
                    kwargs['obj'] = obj
                    return func(*args, **kwargs)
                elif hasattr(obj, 'private') and not obj.private and func.__name__ == 'view':
                    kwargs['obj'] = obj
                    return func(*args, **kwargs)
                return abort(403)
            return abort(404)

        return inner

    return wrapper


def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorator
