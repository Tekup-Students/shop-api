from rest_framework import exceptions, status

from apps.core.mixins import ExceptionMixin


class WrongPasswordException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Wrong Password'
    default_reason = 'Password don\'t match'
    default_code = 1200

