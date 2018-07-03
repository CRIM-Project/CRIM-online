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
        # Construct a query from the url parameters, which are pairs
        # of keys and value-lists. We want to join things in similar
        # categories (which have little or no chance of occurring
        # simultaneously) with OR, while connecting the categories
        # with AND.
        if self.parsed_request:
            def add_values(the_key, value_list, list_to_add_to):
                query_values = ' OR '.join(['"{0}"'.format(s) for s in value_list if s])
                if query_values:
                    query = '{0}:({1})'.format(the_key, query_values)
                    list_to_add_to.append(query)
            # These are the different categories whose search
            # parameters will be joined with AND. Those within each
            # category will be joined with OR.
            q = []
            observer = []
            model_composer = []
            derivative_composer = []
            model_genre = []
            derivative_genre = []
            rt = []
            model_mt = []
            derivative_mt = []
            for k, v in self.parsed_request.items():
                if not v:
                    continue
                if k == 'observer_s':
                    add_values(k, v, observer)
                elif k == 'model_composer_s':
                    add_values(k, v, model_composer)
                elif k == 'derivative_composer_s':
                    add_values(k, v, derivative_composer)
                elif k == 'model_genre_s':
                    add_values(k, v, model_genre)
                elif k == 'derivative_genre_s':
                    print('derivative genre!')
                    add_values(k, v, derivative_genre)
                elif k.startswith('rt_'):
                    add_values(k, v, rt)
                elif k.startswith('model_mt_'):
                    add_values(k, v, model_mt)
                elif k.startswith('derivative_mt_'):
                    add_values(k, v, derivative_mt)
                else:
                    query_values = ' OR '.join(['"{0}"'.format(s) for s in v if s])
                    if query_values:
                        query = '({1})'.format(k, query_values)
                        q.append(query)

            # Create list of each category's query, with parentheses around
            # each group to maintain proper order of operations.
            all_params = [
                '({0})'.format(' AND '.join(q)),
                '({0})'.format(' OR '.join(model_composer)),
                '({0})'.format(' OR '.join(derivative_composer)),
                '({0})'.format(' OR '.join(model_genre)),
                '({0})'.format(' OR '.join(derivative_genre)),
                '({0})'.format(' OR '.join(observer)),
                '({0})'.format(' OR '.join(rt)),
                '({0})'.format(' OR '.join(model_mt)),
                '({0})'.format(' OR '.join(derivative_mt)),
            ]
            # We only add queries with len > 2 because we don't want queries
            # of the form: (composer:"josquin") AND () AND () ...
            self.prepared_query = ' AND '.join([p for p in all_params if len(p) > 2])
            print(self.prepared_query)
        else:
            self.prepared_query = '*:*'
