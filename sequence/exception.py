from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        data = response.data
        response.data = {}
        errors = []
        if isinstance(data, dict):
            for value in data.values():
                error = {}
                error["code"] = value.code
                error["title"] = value
                errors.append(error)
        elif isinstance(data, list):
            for value in data:
                error = {}
                error["code"] = value.code
                error["title"] = value
                errors.append(error)

        response.data['errors'] = errors
    return response
