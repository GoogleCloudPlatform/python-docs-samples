import traceback
import json
from . dtos import Step

class QBValidationError(Exception):
    """Exception for query builder validation errors"""
    def __init__(self, errors):
        super().__init__()
        self.errors = errors


class QBNotFoundError(Exception):
    """Exception for query builder validation errors"""
    def __init__(self, errors):
        super().__init__()
        self.errors = errors


class RunStepError(Exception):
    """Exception for step call on scc"""
    def __init__(self, step_order, cause):
        super().__init__()
        error_content = cause.__dict__['content'].decode()
        error_content = json.loads(error_content)
        error_message = error_content['error']['message']
        self.error = {
            '{}{}'.format(Step.key_for_exception(), step_order) : {
                'message' : error_message,
                'stackTrace' : traceback.format_exception(
                    etype=None, value=cause, tb=cause.__traceback__)
            }
        }


class MissingSecurityHeadersError(Exception):
    """Access denied error for Missing Security Headers"""
    def __init__(self, errors):
        super().__init__()
        self.errors = errors
