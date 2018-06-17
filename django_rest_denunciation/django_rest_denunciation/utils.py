from functools import wraps
from smtplib import SMTPException
from rest_framework import status
from rest_framework.response import Response


def except_smpt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            returned = func(*args, **kwargs)
        except SMTPException:
            return Response(
                {'detail': 'error while sending email'},
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return returned
    return wrapper
