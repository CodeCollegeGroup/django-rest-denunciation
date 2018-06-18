from json import dumps
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
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
    DenunciationSerializer,
    DenunciableSerializer,
    DenunciationCategorySerializer,
    DenunciationQueueSerializer,
    DenunciationStateSerializer,
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
from domain.models import Domain


def fetch_domain_post(data):

    if Domain.objects.filter(key=data['key']).count() == 1:
        return True
    else:
        return False


def fetch_domain_get(req):

    if Domain.objects.filter(key=req.META['HTTP_KEY']).count() == 1:

        return Domain.objects.get(key=req.META['HTTP_KEY'])
    else:
        return None


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

        if fetch_domain_get(request):
            if name in ['null', 'evaluating', 'waiting']:
                new_state = get_request_cond(name, denunciation)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            if new_state is not None:
                denunciation.current_state = new_state
                denunciation.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':

        data = loads(request.body.decode())

        if fetch_domain_post(data):
            if name == 'done':
                return make_evaluate(data, denunciation)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
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


class DenunciationStateViewSet(viewsets.ModelViewSet):

    serializer_class = DenunciationStateSerializer
    queryset = DenunciationState.objects.all()


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

        domain = fetch_domain_get(request)

        if domain is not None:
            denunciations = Denunciation.objects.filter(domain_id=domain.id)

            denunciations_dic_list = []

            for denunciation in denunciations:

                denunciation_dic = self.dict_denunciation_maker(
                    denunciation, request
                )

                if denunciation.current_state.name == 'DoneState':
                    denunciation_dic['evaluate'] = denunciation.evaluate

                denunciations_dic_list.append(denunciation_dic)

            return Response(denunciations_dic_list)
        else:
            return Response(status=400)

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
            data['key']
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
        denouncer = self.getDenouncer(data['denunciation']['denouncer'])
        if denouncer is None:
            denouncer_serializer = DenouncerSerializer(
                data={'email': data['denunciation']['denouncer']}
            )
            if denouncer_serializer.is_valid():
                denouncer_serializer.save()
                denouncer = Denouncer.objects.get(
                    email=data['denunciation']['denouncer']
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
        denunciation.domain = Domain.objects.get(key=data['key'])
        denunciation.denunciable = denunciable
        if 'denouncer' in data['denunciation']:
            denunciation.denouncer = denouncer
        denunciation.save()

        return denunciation

    # create
    def post(self, request, format=None):

        denouncer = None
        data = loads(request.body.decode())
        self.validate_keys(data)
        if fetch_domain_post(data):
            denunciable = self.verify_denunciable(data)
            if denunciable is None:
                return Response(status=400)

            if 'denouncer' in data['denunciation']:
                denouncer = self.verify_denouncer(data)
                if denouncer is None:
                    return Response(status=400)

            try:
                denunciation = self.save_denunciation(
                    data, denunciable, denouncer
                )

                if not self.verify_categories(data, denunciation):
                    return Response(status=400)
            except ValidationError:
                return Response(status=400)

            return Response(status=201)
        else:
            return Response(status=400)


class DenunciationDetails(APIView):

    def get_object(self, pk):

        try:
            return Denunciation.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    # show
    def get(self, request, pk, format=None):

        domain = fetch_domain_get(request)

        if domain is not None:

            denunciation = self.get_object(pk)
            d_dict = DenunciationList.dict_denunciation_maker(
                denunciation, request
            )

            return Response(d_dict)
        else:
            return Response(status=400)

    # delete
    def delete(self, request, pk, format=None):

        denunciation = self.get_object(pk)
        denunciation.delete()

        return Response(status=204)


class DenunciationQueueViewList(APIView):

    filters = ('start', 'end')
    queries_map = {
        'gravity': 'gravity',
        '-gravity': '-gravity',
        'date': 'created_at',
        '-date': '-created_at',
    }

    def get(self, request, format=None):  # pylint: disable=redefined-builtin
        data = request.query_params.copy()
        queryset = self._get_initial_queryset()

        queryset = self._filter_date(queryset, data)

        queries = data.getlist('queries')

        if None not in queries:
            queryset = self._apply_queries(queryset, queries)

        end_data = {'denunciation_queue': queryset}

        serialized_queryset = DenunciationQueueSerializer(
            end_data,
            context={'request': request}
        )

        return Response(
            dumps(serialized_queryset.data),
            status.HTTP_200_OK
        )

    @staticmethod
    def _get_initial_queryset():
        return Denunciation.objects.filter(
            current_state=WaitingState.objects.last()
        )

    @staticmethod
    def _filter_date(queryset, data):
        start, end = data.get('start', None), data.get('end', None)

        if start is not None and end is not None:
            queryset = queryset.filter(
                created_at__gte=start,
                created_at__lte=end
            )
        return queryset

    @classmethod
    def _apply_queries(cls, queryset, queries_list):
        def map_query_name(query):
            return cls.queries_map[query]

        queries_list = map(map_query_name, queries_list)
        queryset = queryset.order_by(*queries_list)

        return queryset
