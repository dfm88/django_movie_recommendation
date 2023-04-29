from django.db import IntegrityError
from rest_framework import status
from rest_framework.views import Response, exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # than custom handlers are defined

    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError) and not response:
        response = Response({'message': str(exc)}, status=status.HTTP_409_CONFLICT)
        return response

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
