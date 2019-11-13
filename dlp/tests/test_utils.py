import os

import decorator
import pytest
from google.api_core import exceptions

SHOULD_PASS_VPCSC = os.getenv('SHOULD_PASS_VPCSC').lower() == "true"
VPC_FAILURE_MESSAGE = "Expected to fail if VPCSC is misconfigured."

# VPCSC function wrappers.
##################################################
@pytest.mark.xfail
def is_rejected_by_vpc(call):
    try:
        call()
    except exceptions.PermissionDenied as e:
        return "Request is prohibited by organization's policy." in e.message
    except exceptions.Forbidden as e:
        return "Request violates VPC Service Controls." in e.message
    except Exception:
        return False


def vpc_check(fn):
    def wrapped(fn, *args, **kwargs):
        if SHOULD_PASS_VPCSC:
            return fn(*args, **kwargs)
        else:
            def call(): return fn(*args, **kwargs)
            return is_rejected_by_vpc(call)
    return decorator.decorator(wrapped, fn)
