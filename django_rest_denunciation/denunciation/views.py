from json import dumps, loads
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from domain.models import Domain
from django_rest_denunciation.views_utils import (
    add_denouncer,
    get_main_urls,
    get_categories_urls,
    get_dict_denunciation,
    verify_domain_key,
    evaluate_denunciation,
    get_request_cond,
    verify_denunciable,
    verify_denouncer,
    verify_categories
)
from .models import (
    Denunciation,
    Denunciable,
    Denouncer,
    DenunciationCategory,
    DenunciationState,
    WaitingState
)
from .serializers import (
    DenunciableSerializer,
    DenunciationCategorySerializer,
    DenunciationQueueSerializer,
    DenunciationStateSerializer,
    DenouncerSerializer
)


@api_view(['GET', 'PATCH'])
def change_denunciation_state(request, pk, state):
    denunciation = get_object_or_404(Denunciation, pk=pk)

    verify_domain_key(pk, request)

    if request.method == 'GET' and state in ('null', 'evaluating', 'waiting'):
        denunciation = get_request_cond(state, denunciation)
        denunciation.save()
    elif request.method == 'PATCH':
        data = loads(request.body.decode())

        if state == 'done':
            evaluate_denunciation(data, denunciation)

    return Response({'ok': 'State was changed'}, status.HTTP_200_OK)


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
    def make_denunciation_dict(denunciation, request):
        url, url_denunciable = get_main_urls(denunciation)
        urls_category = get_categories_urls(denunciation, request)
        urls_list = (url, url_denunciable, urls_category)

        denunciation_dict = get_dict_denunciation(
            denunciation, urls_list, request
        )

        if denunciation.denouncer is not None:
            denunciation_dict = add_denouncer(
                denunciation.denouncer, denunciation_dict, request
            )

        return denunciation_dict

    def get(self, request, format=None):  # pylint: disable=redefined-builtin
        def set_evaluation_states(denunciation):
            denunciation_dict = self.make_denunciation_dict(denunciation,
                                                            request)
            if denunciation.current_state.name == 'donestate':
                denunciation_dict['evaluation'] = denunciation.evaluation

        domain = get_object_or_404(Domain, key=request.META['HTTP_KEY'])
        denunciations = Denunciation.objects.filter(domain_id=domain.id)

        denunciations_dict_list = [set_evaluation_states(denunciation) for
                                   denunciation in denunciations]

        return Response(denunciations_dict_list, status.HTTP_200_OK)

    @staticmethod
    def save_denunciation(data, denunciable, denouncer):
        denunciation = Denunciation(
            current_state=WaitingState.objects.create(),
            justification=data['denunciation']['justification'],
            domain=Domain.objects.get(key=data['key']),
            denunciable=denunciable,
        )

        if 'denouncer' in data['denunciation']:
            denunciation.denouncer = denouncer
        denunciation.save()

        return denunciation

    def post(self, request, format=None):  # pylint: disable=redefined-builtin
        data = loads(request.body.decode())
        get_object_or_404(Domain, key=data['key'])

        denunciable, denouncer = verify_denunciable(data), None
        if 'denouncer' in data.get('denunciation'):
            denouncer = verify_denouncer(data)

        denunciation = self.save_denunciation(data, denunciable, denouncer)
        verify_categories(data, denunciation)

        return Response(status=status.HTTP_201_CREATED)


class DenunciationDetails(APIView):

    def get(self, request, pk, format=None):
        # pylint: disable=redefined-builtin,no-self-use

        verify_domain_key(pk, request)

        denunciation = get_object_or_404(Denunciation, pk=pk)
        denunciation_dict = DenunciationList.make_denunciation_dict(
            denunciation, request
        )

        return Response(denunciation_dict, status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        # pylint: disable=redefined-builtin,no-self-use

        verify_domain_key(pk, request)
        denunciation = get_object_or_404(Denunciation, pk=pk)
        denunciation.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


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
            end_data, context={'request': request}
        )

        return Response(dumps(serialized_queryset.data), status.HTTP_200_OK)

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
                created_at__gte=start, created_at__lte=end
            )
        return queryset

    @classmethod
    def _apply_queries(cls, queryset, queries_list):
        def map_query_name(query):
            return cls.queries_map[query]

        queries_list = map(map_query_name, queries_list)
        queryset = queryset.order_by(*queries_list)

        return queryset
