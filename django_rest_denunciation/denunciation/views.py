from rest_framework.views import APIView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from denunciation.models import Denunciation, Denunciable
from json import dumps, loads
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.urls import reverse


class DenunciationList(APIView):


    # index
    def get(self, request, format=None):

        response = Response()

        denunciations = Denunciation.objects.all()

        denunciations_dic_list = []

        for denunciation in denunciations:

            denunciable = Denunciable.objects.get(id=denunciation.denunciable.id)

            denunciation_dic = denunciation.__dict__

            url = reverse(
                'denunciation-detail',
                kwargs={'pk': denunciation.pk}
            )

            denunciation_dic.update({'denunciable_id' : denunciable.denunciable_id})
            denunciation_dic.update({'denunciable_type' : denunciable.denunciable_type})
            denunciation_dic.update({'url' : request.build_absolute_uri(url)})

            del denunciation_dic['id']
            del denunciation_dic['_state']

            denunciations_dic_list.append(denunciation_dic)

        return Response(denunciations_dic_list)


        # create
    def post(self, request, format=None):

        response = Response()
        data = loads(request.body.decode())

        try:
            if Denunciable.objects.filter(denunciable_id=data['denunciable_id']).count() == 1:

                denunciable = Denunciable.objects.get(denunciable_id=data['denunciable_id'])

            else:

                denunciable = Denunciable()
                denunciable.denunciable_id = data['denunciable_id']
                denunciable.denunciable_type = data['denunciable_type']
                denunciable.save()

            denunciation = Denunciation()
            denunciation.justification = data['justification']
            denunciation.denunciable = denunciable
            denunciation.save()

            response = Response(status=201)

        except ValidationError:

                response = Response(status=400)

        return response
