

class ExceptionMixin:
    def __init__(self, detail=None, code=None, reason=None):
        """
        Builds a detail dictionary for the error to give more information to API
        users.
        """
        detail_dict = {'detail': self.default_detail, 'code': self.default_code}

        if isinstance(detail, dict):
            detail_dict.update(detail)
        elif detail is not None:
            detail_dict['detail'] = detail

        if code is not None:
            detail_dict['code'] = code

        if reason is not None:
            detail_dict['reason'] = reason

        if self.default_reason is not None:
            detail_dict['reason'] = self.default_reason
