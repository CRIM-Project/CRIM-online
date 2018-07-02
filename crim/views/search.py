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
        'observer': sorted(facets['observer']),
        'model_composer': sorted(facets['model_composer']),
        'model_genre': sorted(facets['model_genre']),
        'derivative_composer': sorted(facets['derivative_composer']),
        'derivative_genre': sorted(facets['derivative_genre']),
    }
    return render(request, 'search/search.html', data)
def _empty_search(request):
    s = CRIMSolrSearch(request)
    ret = s.facets(fq=['crim_relationship'], rows=0)
    facets = ret.facet_counts['facet_fields']
    print(sorted(facets['observer']))

    data = {
        'observer': facets['observer'],
        'model_composer': facets['model_composer'],
        'model_genre': facets['model_genre'],
        'derivative_composer': facets['derivative_composer'],
        'derivative_genre': facets['derivative_genre'],
    }
    return render(request, 'search/search.html', data)
