from copy import copy
from functools import wraps


def wrap_exceptions(excs: dict, *, base_exception=Exception):
    """
    Decorate a function to raise a user-defined exception,
    corresponding to library-defined

    >>> class SpecificError(Exception): pass

    >>> def failing_func():
    ...     raise RuntimeError()

    >>> @wrap_exceptions({RuntimeError: SpecificError})
    ... def wrapped_failing_func():
    ...    raise RuntimeError()

    >>> failing_func()
    Traceback (most recent call last):
        ...
    RuntimeError

    >>> wrapped_failing_func()
    Traceback (most recent call last):
        ...
    RuntimeError

    The above exception was the direct cause of the following exception:

    Traceback (most recent call last):
        ...
    SpecificError
    """
    def inner_wrapper(func):

        @wraps(func)
        def new_f(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except base_exception as e:
                exc = excs.get(e.__class__)
                if exc is None:
                    raise
                elif isinstance(exc, type) and issubclass(exc, base_exception):
                    raise exc() from e
                elif isinstance(exc, base_exception):
                    raise copy(exc) from e
        return new_f

    return inner_wrapper
