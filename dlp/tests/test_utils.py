import os
import decorator
import pdb

from google.api_core import exceptions

SHOULD_PASS = os.getenv('SHOULD_PASS').lower()

def is_rejected_by_vpc(call):
    try:
        print("INSIDE WRAPPER")
        response = call()
    except exceptions.PermissionDenied as e:
        return "Request is prohibited by organization's policy." in e.message
    except exceptions.Forbidden as e:
        return "Request violates VPC Service Controls." in e.message
    except:
        return False

def vpc_check(fn):
    def wrapped(fn, *args, **kwargs):
        if SHOULD_PASS == "true":
            return fn(*args, **kwargs)
        else:
            call = lambda: fn(*args, **kwargs)
            return is_rejected_by_vpc(call)
    return decorator.decorator(wrapped, fn)


def vpc_dec(fn):
    def new_gen(fn, *args, **kwargs):
        g = fn(*args, **kwargs)
        try:
            value = next(g)
            for v in g:
                yield value
                value = v
        except exceptions.PermissionDenied as e:
            pass
        except exceptions.Forbidden as e:
            pass
    return decorator.decorator(new_gen, fn)
