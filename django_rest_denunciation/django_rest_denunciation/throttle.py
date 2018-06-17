from rest_framework.throttling import (
    UserRateThrottle
)
from denunciation.models import Denunciation
from datetime import (
    datetime,
    date,
    time
)
import json


class DenouncerRateThrottle(UserRateThrottle):

    scope = 'denouncer'

    def allow_request(self, request, view):

        self.key = self.get_cache_key(request, view)
        self.history = self.cache.get(self.key, [])
        self.now = self.timer()

        data = json.loads(request.body.decode('utf-8'))

        if 'denouncer' in data and 'email' in data['denouncer']:
            denouncer = data['denouncer']['email']
            domain = data['denunciation']['domain']

            if domain[-1] == '/':
                domain = domain[:-1]
            domain = domain.rsplit('/')[-1]

            start_day = datetime.combine(date.today(), time.min)
            end_day = datetime.combine(date.today(), time.max)

            denunciations = Denunciation.objects.filter(
                domain=domain,
                denouncer__email=denouncer,
                denunciable__denunciable_datetime__range=(start_day, end_day)
            )

            if denunciations.count() < self.num_requests:
                return True
            else:
                return False
        else:
            return False
