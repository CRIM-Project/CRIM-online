from django.conf import settings
from crim.helpers.solrpaginate import SolrPaginator, SolrGroupedPaginator
import solr


class CRIMSolrSearch(object):
    def __init__(self, request):
        self.server = solr.Solr(settings.SOLR_SERVER)
        self.request = request
        self.parsed_request = {}
        self.prepared_query = ''
        self.solr_params = {}
        self._parse_request()
        self._prep_q()

    def search(self, **kwargs):
        self.solr_params.update(kwargs)
        res = self._do_query()
        return SolrPaginator(res)

    def facets(self, facet_fields=settings.SOLR_FACET_FIELDS, **kwargs):
        facet_params = {
            'facet': 'true',
            'facet_field': facet_fields,
        }
        self.solr_params.update(facet_params)
        self.solr_params.update(kwargs)

        ret = self._do_query()
        return ret

    def group_search(self, group_fields, **kwargs):
        group_params = {
            'group': 'true',
            'group_ngroups': 'true',
            'group_field': group_fields
        }
        self.solr_params.update(group_params)
        self.solr_params.update(kwargs)

        res = self._do_query()
        return SolrGroupedPaginator(res)

    def _do_query(self):
        return self.server.select(self.prepared_query, **self.solr_params)

    def _parse_request(self):
        qdict = self.request.GET
        for k, v in qdict.lists():
            if k not in settings.SEARCH_PARAM_MAP.keys():
                continue
            self.parsed_request[settings.SEARCH_PARAM_MAP[k]] = v

    def _prep_q(self):
        if self.parsed_request:
            arr = []
            for k, v in self.parsed_request.iteritems():
                if not v:
                    continue
                if k == 'q':
                    if v[0] != '':
                        arr.insert(0, '{0}'.format(v[0]))
                else:
                    selected_values = ' OR '.join(['"{0}"'.format(s) for s in v if s])
                    arr.append('{0}:({1})'.format(k, selected_values))
            self.prepared_query = ' AND '.join(arr)
        else:
            self.prepared_query = '*:*'
