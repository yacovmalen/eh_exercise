
"""
Errors Definitions
"""


class ErrorDefinitions(object):
    errors = {
        'EntityAlreadyExistsError': {
            'message': "A entity with that ID already exists.",
            'status': 409
        },
        'EntityNotFound': {
            'message': "A resource with that ID does not exist.",
            'status': 404
        },
        'UnauthorizedError': {
            'message': 'Access denied - current user is not authorized to access this data',
            'status': 401
        },
        'BadRequestError': {
            'message': 'Bad Request Error',
            'status': 400
        },
        'DatabaseError': {
            'message': 'Internal Error',
            'status': 500
        },
        'NotImplementedError': {
            'message': 'Api Method is Not Implemented',
            'status': 501
        }
    }


class EntityAlreadyExistsError(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)


class EntityNotFound(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)


class BadRequestError(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)


class DatabaseError(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)


class UnauthorizedError(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)