from django.shortcuts import render
import json

from django.http import HttpResponse
from django.conf import settings
from django.core.paginator import EmptyPage, InvalidPage
from crim.helpers.solrsearch import CRIMSolrSearch


class JsonResponse(HttpResponse):
    def __init__(self, content, content_type='application/json', status=None):
        super(JsonResponse, self).__init__(
            content=json.dumps(content),
            status=status,
            content_type=content_type
        )


def result_callback(request, restype):
    if restype == 'piece':
        return _fetch_piece_results(request)
    elif restype == 'relationship':
        return _fetch_relationship_results(request)
    elif restype == 'facet':
        return _fetch_facet_results(request)


def _fetch_piece_results(request):
    s = CRIMSolrSearch(request)
    piece_res = s.group_search(['title'], fq=['type:(crim_relationship OR crim_piece)'])

    if piece_res.count == 0:
        return render(request, 'search/no_results.html')

    try:
        piece_page = int(request.GET.get('piece_page', '1'))
    except ValueError:
        piece_page = 1

    try:
        piece_results = piece_res.page(piece_page)
    except (EmptyPage, InvalidPage):
        piece_results = piece_res.page(piece_res.num_pages)
    piece_results.pager_id = 'pieces'

    data = {
        'piece_results': piece_results,
    }
    return render(request, 'search/piece_result_list.html', data)


def _fetch_relationship_results(request):
    s = CRIMSolrSearch(request)
    rel_res = s.search(
        fq=['type:crim_relationship'],
        sort=[
            'model_piece_id_s asc',
            'derivative_piece_id_s asc',
            'model_ema_t asc',
            'derivative_ema_t asc',
        ]
    )

    if rel_res.count == 0:
        return render(request, 'search/no_results.html')

    try:
        relationship_page = int(request.GET.get('relationship_page', '1'))
    except ValueError:
        relationship_page = 1

    try:
        relationship_results = rel_res.page(relationship_page)
    except (EmptyPage, InvalidPage):
        relationship_results = rel_res.page(rel_res.num_pages)
    relationship_results.pager_id = 'relationships'

    data = {
        'relationship_results': relationship_results
    }
    return render(request, 'search/relationship_result_list.html', data)


def _fetch_facet_results(request):
    s = CRIMSolrSearch(request)
    facet_params = {
        'facet_mincount': 1,
    }
    facet_res = s.facets(fq=['type:crim_relationship'], **facet_params)
    facets = facet_res.facet_counts['facet_fields']
    # filtered_facets = dict([(k, v) for k, v in facets.iteritems() if k in settings.DISPLAY_FACETS])

    filtered_facets = []
    for k, v in facets.iteritems():
        this_facet = []
        if k not in settings.DISPLAY_FACETS.keys():
            continue
        for facet_value, num in v.iteritems():
            this_facet.append([facet_value, settings.DISPLAY_FACETS[k][0]])

        this_facet.sort()
        filtered_facets.append([settings.DISPLAY_FACETS[k][1], this_facet])

    filtered_facets.sort()

    data = {
        'facet_results': filtered_facets
    }
    return render(request, 'search/facets.html', data)
