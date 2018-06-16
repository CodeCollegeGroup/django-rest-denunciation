from rest_framework.throttling import (
    UserRateThrottle
)


class DenouncerThrottle(UserRateThrottle):

    scope = 'denouncer'

    #TODO This class should override alow_request method to validate
    #     if request has been blocked

