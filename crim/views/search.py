from django.shortcuts import render
from crim.helpers.solrsearch import CRIMSolrSearch


def search(request):
    if 'q' not in request.GET:
        return _empty_search(request)
    else:
        return render(request, 'search/results.html')


def _empty_search(request):
    s = CRIMSolrSearch(request)
    ret = s.facets(fq=['crim_relationship'], rows=0)
    facets = ret.facet_counts['facet_fields']

    data = {
        'observer': facets['observer_s'],
        'model_title': facets['model_title_s'],
        'model_mass': facets['model_mass_s'],
        'model_composer': facets['model_composer_s'],
        'model_genre': facets['model_genre_s'],
        'derivative_title': facets['derivative_title_s'],
        'derivative_mass': facets['derivative_mass_s'],
        'derivative_composer': facets['derivative_composer_s'],
        'derivative_genre': facets['derivative_genre_s'],
        'rt_q': facets['rt_q_b'],
        'rt_q_x': facets['rt_q_x_b'],
        'rt_q_monnayage': facets['rt_q_monnayage_b'],
        'rt_tm': facets['rt_tm_b'],
        'rt_tm_snd': facets['rt_tm_snd_b'],
        'rt_tm_minv': facets['rt_tm_minv_b'],
        'rt_tm_retrograde': facets['rt_tm_retrograde_b'],
        'rt_tm_ms': facets['rt_tm_ms_b'],
        'rt_tm_transposed': facets['rt_tm_transposed_b'],
        'rt_tm_invertible': facets['rt_tm_invertible_b'],
        'rt_tnm': facets['rt_tnm_b'],
        'rt_tnm_embellished': facets['rt_tnm_embellished_b'],
        'rt_tnm_reduced': facets['rt_tnm_reduced_b'],
        'rt_tnm_amplified': facets['rt_tnm_amplified_b'],
        'rt_tnm_truncated': facets['rt_tnm_truncated_b'],
        'rt_tnm_ncs': facets['rt_tnm_ncs_b'],
        'rt_tnm_ocs': facets['rt_tnm_ocs_b'],
        'rt_tnm_ocst': facets['rt_tnm_ocst_b'],
        'rt_tnm_nc': facets['rt_tnm_nc_b'],
        'rt_nm': facets['rt_nm_b'],
        'rt_om': facets['rt_om_b'],
    }
    return render(request, 'search/search.html', data)
