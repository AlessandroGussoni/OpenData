from functools import update_wrapper, wraps
from types import MethodType


class _AvailableIfDescriptor:

    def __init__(self, fn, check, attribute_name):
        self.fn = fn
        self.check = check
        self.attribute_name = attribute_name

        # update the docstring of the descriptor
        update_wrapper(self, fn)

    def __get__(self, obj, owner=None):

        attr_err = AttributeError(
            f"This {repr(owner.__name__)} has no attribute {repr(self.attribute_name)}"
        )

        if obj is not None:

            if not self.check(obj):
                raise attr_err
            out = MethodType(self.fn, obj)

        else:

            @wraps(self.fn)
            def out(*args, **kwargs):
                if not self.check(args[0]):
                    raise attr_err
                return self.fn(*args, **kwargs)

        return out


def available_if(check):

    return lambda fn: _AvailableIfDescriptor(fn, check, attribute_name=fn.__name__)