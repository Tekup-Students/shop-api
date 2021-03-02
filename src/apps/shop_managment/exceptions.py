from rest_framework import exceptions, status

from apps.core.mixins import ExceptionMixin


class ExampleException(exceptions.APIException, ExceptionMixin):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Wrong'
    default_reason = 'Reason'
    default_code = 1300


class InvalidDateException(exceptions.APIException, ExceptionMixin):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Wrong'
    default_reason = 'Reason'
    default_code = 1301


class InvalidAppointmentTimeException(exceptions.APIException, ExceptionMixin):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Appointment Time is not valid'
    default_reason = 'Reason'
    default_code = 1302


class UnauthorizedUpdateException(exceptions.APIException, ExceptionMixin):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'You are unauthorized to update'
    default_reason = 'Reason'
    default_code = 1303


class UnauthorizedCreateFolderException(exceptions.APIException, ExceptionMixin):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'A Folder with this data already exists'
    default_reason = 'Reason'
    default_code = 1303