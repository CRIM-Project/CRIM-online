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
            'rt_q_b desc',
            'rt_tm_b desc',
            'rt_tnm_b desc',
            'rt_nm_b desc',
            'rt_om_b desc',
            'model_mt_cf_b desc',
            'model_mt_sog_b desc',
            'model_mt_csog_b desc',
            'model_mt_cd_b desc',
            'model_mt_fg_b desc',
            'model_mt_pe_b desc',
            'model_mt_id_b desc',
            'model_mt_nid_b desc',
            'model_mt_hr_b desc',
            'model_mt_cad_b desc',
            'model_mt_int_b desc',
            'model_mt_fp_b desc',
            'derivative_mt_cf_b desc',
            'derivative_mt_sog_b desc',
            'derivative_mt_csog_b desc',
            'derivative_mt_cd_b desc',
            'derivative_mt_fg_b desc',
            'derivative_mt_pe_b desc',
            'derivative_mt_id_b desc',
            'derivative_mt_nid_b desc',
            'derivative_mt_hr_b desc',
            'derivative_mt_cad_b desc',
            'derivative_mt_int_b desc',
            'derivative_mt_fp_b desc',
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

    filtered_facets_observer = []
    filtered_facets_model = []
    filtered_facets_derivative = []
    filtered_facets_rt_mt = []

    for k, v in facets.items():
        this_facet = []
        if k in settings.DISPLAY_FACETS_OBSERVER.keys():
            for facet_value, num in v.items():
                this_facet.append([facet_value, settings.DISPLAY_FACETS_OBSERVER[k][0], num])
            filtered_facets_observer.append([settings.DISPLAY_FACETS_OBSERVER[k][1], this_facet])
        elif k in settings.DISPLAY_FACETS_MODEL.keys():
            for facet_value, num in v.items():
                this_facet.append([facet_value, settings.DISPLAY_FACETS_MODEL[k][0], num])
            filtered_facets_model.append([settings.DISPLAY_FACETS_MODEL[k][1], this_facet])
        elif k in settings.DISPLAY_FACETS_DERIVATIVE.keys():
            for facet_value, num in v.items():
                this_facet.append([facet_value, settings.DISPLAY_FACETS_DERIVATIVE[k][0], num])
            filtered_facets_derivative.append([settings.DISPLAY_FACETS_DERIVATIVE[k][1], this_facet])
        else:
            pass

    data = {
        'facet_results_observer': filtered_facets_observer,
        'facet_results_model': filtered_facets_model,
        'facet_results_derivative': filtered_facets_derivative,
        'type_facets': {k: facets.get(k) for k in settings.TYPE_FACETS},
    }
    return render(request, 'search/facets.html', data)
