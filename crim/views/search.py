from haystack.forms import FacetedSearchForm as BaseFacetedSearchForm
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView


class FacetedSearchForm(BaseFacetedSearchForm):
    def no_query_found(self):
        return self.searchqueryset.auto_query('')


class FacetedSearchView(BaseFacetedSearchView):
    form_class = FacetedSearchForm
    # List of facets on relationship objects
    facet_fields = ['composer', 'genre']

    context_object_name = 'page_object'
