from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.db import connection, transaction
from rest_framework.response import Response
from rest_framework import exceptions, status

def set_rollback():
    atomic_requests = connection.settings_dict.get('ATOMIC_REQUESTS', False)
    if atomic_requests and connection.in_atomic_block:
        transaction.set_rollback(True)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if hasattr(exc, 'get_full_details'):
            data = exc.get_full_details()
        else:
            data = exc.detail

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
