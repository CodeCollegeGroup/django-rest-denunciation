from django.urls import reverse
from denunciation.models import (
    Denunciable,
    Denouncer
)


def add_denouncer(denouncer, denunciation_dict, request):
    denouncer = Denouncer.objects.get(id=denouncer.id)

    url_denouncer = reverse(
        'denouncer-detail',
        kwargs={'pk': denouncer.pk}
    )

    denunciation_dict.update(
        {'denouncer': request.build_absolute_uri(url_denouncer)}
    )

    return denunciation_dict


def get_main_urls(denunciation):

    denunciable = Denunciable.objects.get(
        id=denunciation.denunciable.id
    )

    url = reverse(
        'denunciation-detail',
        kwargs={'pk': denunciation.pk}
    )

    url_denunciable = reverse(
        'denunciable-detail',
        kwargs={'pk': denunciable.pk}
    )

    return [url, url_denunciable]


def get_categories_urls(denunciation, request):

    urls_category = []

    for category in denunciation.categories.all():

        url_c = reverse(
            'denunciationcategory-detail',
            kwargs={'pk': category.pk}
        )

        urls_category.append(request.build_absolute_uri(url_c))

    return urls_category


def get_dict_denunciation(denunciation, url_list, request):

    url, url_denunciable, urls_category = url_list

    d_dict = {'url': request.build_absolute_uri(url)}
    d_dict['justification'] = denunciation.justification

    d_dict.update(
        {'current_state': denunciation.current_state.name}
    )

    if urls_category != []:
        d_dict.update({'categories': urls_category})

    d_dict['denunciable'] = request.build_absolute_uri(url_denunciable)

    return d_dict
