from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.observation import CRIMObservationSerializer
from crim.models.observation import CRIMObservation

COMPOSER = 'Composer'


class ObservationSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the observation_list.html template!
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 45


class ObservationListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['observation/observation_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class ObservationDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # - Add `composer` field to content: only look at roles with
        # the role type with name "Composer", and add all such names
        # to the list, along with the url of the composer
        composers = []
        for role in data['piece']['roles']:
            if role['role_type'] and role['role_type']['name'] == COMPOSER:
                composer_html = ('<a href="' + role['person']['url'].replace('/data/', '/') +
                                 '">' + role['person']['name'] + '</a>')
                composers.append(composer_html)
        if data['piece']['mass']:
            for role in data['piece']['mass']['roles']:
                if role['role_type'] and role['role_type']['name'] == COMPOSER:
                    composer_html = ('<a href="' + role['person']['url'].replace('/data/', '/') +
                                     '">' + role['person']['name'] + '</a>')
                    composers.append(composer_html)
        data['composers_with_urls'] = ', '.join(composers)

        template_names = ['observation/observation_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class ObservationList(generics.ListAPIView):
    model = CRIMObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMObservationSerializer
    pagination_class = ObservationSetPagination
    renderer_classes = (
        ObservationListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'piece_id')
        return CRIMObservation.objects.all().order_by(order_by)


class ObservationDetail(generics.RetrieveAPIView):
    model = CRIMObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMObservationSerializer
    renderer_classes = (
        ObservationDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMObservation.objects.all()

    def get_object(self):
        url_arg = self.kwargs['pk']
        observation = CRIMObservation.objects.filter(pk=url_arg)
        obj = get_object_or_404(observation)
        self.check_object_permissions(self.request, obj)
        return obj


class ObservationListData(ObservationList):
    renderer_classes = (JSONRenderer,)


class ObservationDetailData(ObservationDetail):
    renderer_classes = (JSONRenderer,)
