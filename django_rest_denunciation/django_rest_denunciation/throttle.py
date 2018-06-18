from datetime import (
    datetime,
    date,
    time
)
import json
from rest_framework.throttling import (
    UserRateThrottle
)
from denunciation.models import Denunciation


class DenouncerRateThrottle(UserRateThrottle):

    scope = 'denouncer'

    def allow_request(self, request, view):

        self.key = self.get_cache_key(request, view)  # pylint: disable=W0201
        self.history = self.cache.get(self.key, [])  # pylint: disable=W0201

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

            return denunciations.count() < self.num_requests
        else:
            return False
