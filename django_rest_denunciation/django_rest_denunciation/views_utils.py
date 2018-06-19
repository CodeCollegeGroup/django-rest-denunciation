from django.urls import reverse
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, ParseError
from denunciation.serializers import DenunciableSerializer, DenouncerSerializer
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


def add_denouncer(denouncer, denunciation_dict, request):
    denouncer = Denouncer.objects.get(id=denouncer.id)
    url_denouncer = reverse('denouncer-detail', kwargs={'pk': denouncer.pk})

    denunciation_dict.update(
        {'denouncer': request.build_absolute_uri(url_denouncer)}
    )

    return denunciation_dict


def get_main_urls(denunciation):

    denunciable = Denunciable.objects.get(id=denunciation.denunciable.id)

    url = reverse('denunciation-detail', kwargs={'pk': denunciation.pk})
    url_denunciable = reverse('denunciable-detail',
                              kwargs={'pk': denunciable.pk})

    return url, url_denunciable


def get_categories_urls(denunciation, request):

    urls_category = []
    for category in denunciation.categories.all():
        url_c = reverse('denunciationcategory-detail',
                        kwargs={'pk': category.pk})

        urls_category.append(request.build_absolute_uri(url_c))

    return urls_category


def get_dict_denunciation(denunciation, url_list, request):
    url, url_denunciable, urls_category = url_list

    d_dict = {'url': request.build_absolute_uri(url)}
    d_dict['justification'] = denunciation.justification

    d_dict.update({'current_state': denunciation.current_state.name})

    if not urls_category:
        d_dict.update({'categories': urls_category})

    d_dict['denunciable'] = request.build_absolute_uri(url_denunciable)
    return d_dict


def verify_domain_key(pk, request):
    key = request.META['HTTP_KEY']
    denunciation = get_object_or_404(Denunciation, pk=pk)

    if key != denunciation.domain.key:
        raise ParseError('Wrong domain key!')


def evaluate_denunciation(data, denunciation):
    if denunciation.current_state.name == 'evaluatingstate':
        denunciation.evaluation = data.get('evaluation')
        denunciation.fake = data.get('fake')

        denunciation.current_state = DoneState.objects.create()
        denunciation.save()

        if denunciation.fake and denunciation.denouncer is not None:
            denunciation.denouncer.fake_denunciation += 1
    else:
        raise ValidationError("Invalid state transition")


def evaluate_states(denunciation, states):
    if states == ('evaluating', 'waitingstate'):
        denunciation.current_state = EvaluatingState.objects.create()
    elif states == ('waiting', 'nullstate'):
        denunciation.current_state = WaitingState.objects.create()
    else:
        raise ValidationError("Invalid state transition")

    return denunciation


def get_request_cond(state, denunciation):
    denunciation_state = denunciation.current_state.name
    states = (state, denunciation_state)

    if state == 'null':
        denunciation.current_state = NullState.objects.create()
    else:
        denunciation = evaluate_states(denunciation, states)

    return denunciation


def verify_denunciable(data):
    denunciable_id = data['denunciable']['denunciable_id']
    denunciable_type = data['denunciable']['denunciable_type']

    if not Denunciable.objects.filter(
        denunciable_id=denunciable_id,
        denunciable_type=denunciable_type
    ).exists():
        data_denunciable = data['denunciable']
        denunciable_serializer = DenunciableSerializer(
            data=data_denunciable
        )
        denunciable_serializer.is_valid()
        denunciable_serializer.save()

    return Denunciable.objects.get(
        denunciable_id=data['denunciable']['denunciable_id'],
        denunciable_type=data['denunciable']['denunciable_type']
    )


def verify_denouncer(data):
    email = data['denunciation']['denouncer']
    if not Denouncer.objects.filter(email=email).exists():
        denouncer_serializer = DenouncerSerializer(
            data={'email': data['denunciation']['denouncer']}
        )
        denouncer_serializer.is_valid()
        denouncer_serializer.save()

    return Denouncer.objects.get(email=data['denunciation']['denouncer'])


def save_categories(denunciation, categories):
    if list(categories):
        for category in categories:
            denunciation.categories.add(category)
            denunciation.save()
    else:
        denunciation.delete()
        raise ValidationError('Categories failed on validation')


def verify_categories(data, denunciation):
    def get_category(name):
        return DenunciationCategory.objects.filter(name=name).first()

    if 'categories' in data['denunciation']:
        categories_names = data['denunciation']['categories']

        categories = filter(
            lambda category: category is not None,
            [get_category(name) for name in categories_names]
        )

        save_categories(denunciation, categories)
