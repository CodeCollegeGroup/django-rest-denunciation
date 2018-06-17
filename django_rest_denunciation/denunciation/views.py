from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from json import loads
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import (
    DenunciableSerializer,
    DenunciationCategorySerializer,
    DenouncerSerializer
)
from denunciation.models import (
    Denunciation,
    Denunciable,
    Denouncer,
    DenunciationCategory,
    WaitingState,
    NullState,
    EvaluatingState,
    DoneState
)
from denunciation.auxiliary_methods import (
    add_denouncer,
    get_main_urls,
    get_categories_urls,
    get_dict_denunciation
)


def make_nullstate():
    return NullState.objects.create()


def make_evaluatingstate(denunciation):

    if denunciation.current_state.name == 'WaitingState':
        return EvaluatingState.objects.create()
    else:
        return None


def make_waitingstate(denunciation):

    if denunciation.current_state.name == 'NullState':
        return WaitingState.objects.create()
    else:
        return None


def make_evaluate(data, denunciation):
    try:
        if denunciation.current_state.name == 'EvaluatingState':
            denunciation.evaluation = data['evaluation']
            denunciation.fake = data['fake']
            denunciation.current_state = DoneState.objects.create()
            denunciation.save()
            if denunciation.fake and denunciation.denouncer is not None:
                denouncer = denunciation.denouncer
                denouncer.fake_denunciation += 1
        else:
            return Response(status=400)
    except KeyError:
        return Response(status=400)
    return Response(status=200)


def get_request_cond(name, denunciation):
    new_state = None

    if name == 'null':
        new_state = make_nullstate()
    elif name == 'evaluating':
        new_state = make_evaluatingstate(denunciation)
    elif name == 'waiting':
        new_state = make_waitingstate(denunciation)
    return new_state


@api_view(['GET', 'PATCH'])
def change_denunciation_state(request, pk, name):

    try:
        denunciation = Denunciation.objects.get(pk=pk)
    except Denunciation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        if name in ['null', 'evaluating', 'waiting']:
            new_state = get_request_cond(name, denunciation)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if new_state is not None:
            denunciation.current_state = new_state
            denunciation.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        if name == 'done':
            data = loads(request.body.decode())
            return make_evaluate(data, denunciation)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


class DenunciableViewSet(viewsets.ModelViewSet):

    serializer_class = DenunciableSerializer
    queryset = Denunciable.objects.all()


class DenunciationCategoryViewSet(viewsets.ModelViewSet):

    serializer_class = DenunciationCategorySerializer
    queryset = DenunciationCategory.objects.all()


class DenouncerViewSet(viewsets.ModelViewSet):

    serializer_class = DenouncerSerializer
    queryset = Denouncer.objects.all()


class DenunciationList(APIView):

    @staticmethod
    def dict_denunciation_maker(denunciation, request):

        url, url_denunciable = get_main_urls(denunciation)

        urls_category = get_categories_urls(denunciation, request)

        url_list = [url, url_denunciable, urls_category]
        denunciation_dict = get_dict_denunciation(
            denunciation, url_list, request
        )

        if denunciation.denouncer is not None:
            denunciation_dict = add_denouncer(
                denunciation.denouncer, denunciation_dict, request
            )

        return denunciation_dict

    # index
    def get(self, request, format=None):

        denunciations = Denunciation.objects.all()

        denunciations_dic_list = []

        for denunciation in denunciations:

            denunciation_dic = self.dict_denunciation_maker(
                denunciation, request
            )

            if denunciation.current_state.name == 'DoneState':
                denunciation_dic['evaluate'] = denunciation.evaluate

            denunciations_dic_list.append(denunciation_dic)

        return Response(denunciations_dic_list)

    @staticmethod
    def getDenunciable(d_id, d_type):

        denunciable_count = Denunciable.objects.filter(
            denunciable_id=d_id,
            denunciable_type=d_type
        ).count()
        if denunciable_count == 1:
            return Denunciable.objects.get(
                denunciable_id=d_id, denunciable_type=d_type
            )
        else:
            return None

    @staticmethod
    def getDenouncer(email):

        if Denouncer.objects.filter(email=email).count() == 1:
            return Denouncer.objects.get(email=email)
        else:
            return None

    @staticmethod
    def getCategories(names):

        list_categories = []

        for _name in names:
            if DenunciationCategory.objects.filter(name=_name).count() == 1:
                list_categories.append(
                    DenunciationCategory.objects.get(name=_name)
                )
            else:
                return None

        return list_categories

    @staticmethod
    def validate_keys(data):

        try:
            data['denunciable']
            data['denunciable']['denunciable_id']
            data['denunciable']['denunciable_type']

            data['denunciation']
        except KeyError:
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST)

    def verify_denunciable(self, data):
        denunciable = self.getDenunciable(
            data['denunciable']['denunciable_id'],
            data['denunciable']['denunciable_type']
        )

        if not denunciable:
            data_denunciable = data['denunciable']
            denunciable_serializer = DenunciableSerializer(
                data=data_denunciable
            )
            if denunciable_serializer.is_valid():
                denunciable_serializer.save()
                denunciable = Denunciable.objects.get(
                    denunciable_id=data['denunciable']['denunciable_id'],
                    denunciable_type=data['denunciable']['denunciable_type']
                )
            else:
                return None

        return denunciable

    def verify_denouncer(self, data):
        denouncer = self.getDenouncer(data['denunciation']['email'])
        if denouncer is None:
            denouncer_serializer = DenouncerSerializer(
                data={'email': data['denunciation']['email']}
            )
            if denouncer_serializer.is_valid():
                denouncer_serializer.save()
                denouncer = Denouncer.objects.get(
                    email=data['denunciation']['email']
                )
            else:
                return None

        return denouncer

    def verify_categories(self, data, denunciation):
        if 'categories' in data['denunciation']:
            categories = self.getCategories(
                data['denunciation']['categories']
            )

            if categories is not None:
                for category in categories:
                    denunciation.categories.add(category)
                    denunciation.save()
            else:
                denunciation.delete()
                return False

        return True

    def save_denunciation(self, data, denunciable, denouncer):
        denunciation = Denunciation()
        denunciation.current_state = WaitingState.objects.create()
        denunciation.justification = data['denunciation']['justification']
        denunciation.denunciable = denunciable
        if 'email' in data['denunciation']:
            denunciation.denouncer = denouncer
        denunciation.save()

        return denunciation

    # create
    def post(self, request, format=None):

        denouncer = None
        data = loads(request.body.decode())
        self.validate_keys(data)
        denunciable = self.verify_denunciable(data)
        if denunciable is None:
            return Response(status=400)

        if 'email' in data['denunciation']:
            denouncer = self.verify_denouncer(data)
            if denouncer is None:
                return Response(status=400)

        try:
            denunciation = self.save_denunciation(data, denunciable, denouncer)

            if not self.verify_categories(data, denunciation):
                return Response(status=400)
        except ValidationError:
            return Response(status=400)

        return Response(status=201)


class DenunciationDetails(APIView):

    def get_object(self, pk):

        try:
            return Denunciation.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    # show
    def get(self, request, pk, format=None):

        denunciation = self.get_object(pk)

        denunciation_dic = denunciation.__dict__

        denunciable = Denunciable.objects.get(id=denunciation.denunciable.id)

        url = reverse(
            'denunciation-detail',
            kwargs={'pk': denunciation.pk}
        )

        denunciation_dic.update(
            {'denunciable_id': denunciable.denunciable_id}
        )
        denunciation_dic.update(
            {'denunciable_type': denunciable.denunciable_type}
        )
        denunciation_dic.update(
            {'url': request.build_absolute_uri(url)}
        )

        del denunciation_dic['id']
        del denunciation_dic['_state']

        return Response(denunciation_dic)

    # update
    def put(self, request, pk, format=None):

        denunciation = self.get_object(pk)
        denunciable = Denunciable.objects.get(id=denunciation.denunciable.id)
        response = Response()
        data = loads(request.body.decode())

        try:

            denunciation.justification = data['justification']
            denunciation.save()

            denunciable.denunciable_id = data['denunciable_id']
            denunciable.denunciable_type = data['denunciable_type']
            denunciable.save()

            response = Response(status=200)

        except ValidationError:

                response = Response(status=400)

        return response

    # delete
    def delete(self, request, pk, format=None):

        denunciation = self.get_object(pk)
        denunciation.delete()

        return Response(status=204)
