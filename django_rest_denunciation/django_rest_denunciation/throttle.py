from rest_framework.throttling import (
    UserRateThrottle
)
import json


class DenouncerThrottle(UserRateThrottle):

    scope = 'denouncer'

    def allow_request(self, request, view):

        self.key = self.get_cache_key(request, view)
        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        data = json.loads(request.body.decode('utf-8'))

        if 'denouncer' in data:
            denouncer = data['denouncer']
            #TODO check if has many denouncements of denouncer in day
            return super(DenouncerThrottle, self).allow_request(request, view)
        else:
            return False
