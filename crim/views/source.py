from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.source import CRIMSourceListSerializer, CRIMSourceDetailSerializer
from crim.models.document import CRIMSource

from crim.common import earliest_date

AUTHOR = 'Author'
COMPOSER = 'Composer'
PUBLISHER = 'Publisher'


class SourceSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the source_list.html template!
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15


class SourceListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        for document in data:
            # - Add `publisher` field to content: only look at roles with
            # the role type with name "Publisher", and add all such names
            # to the list, along with the url of the publisher
            # - Add `date` field to content: again, only look at roles
            # with the role type "Publisher"
            publishers = []
            dates = []
            for role in document['roles']:
                if role['role_type'] and role['role_type']['name'] == PUBLISHER:
                    publisher_html = ('<a href="' + role['person']['url'] +
                                      '">' + role['person']['name'] + '</a>')
                    publishers.append(publisher_html)
                    if role['date']:
                        dates.append(role['date'])
            document['publishers_with_url'] = '; '.join(publishers) if publishers else '-'
            # Only add one publisher's date for clarity, choosing the earliest
            document['date'] = earliest_date(dates)

        template_names = ['source/source_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class SourceDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # See SourceListHTMLRenderer for comments on getting publisher
        # names and dates
        for item in (data['piece_contents'] + data['mass_contents'] +
                     data['treatise_contents']):
            creators = []
            dates = []
            for role in item['roles']:
                if role['role_type'] and role['role_type']['name'] in (COMPOSER, AUTHOR):
                    creator_html = ('<a href="' + role['person']['url'] +
                                    '">' + role['person']['name'] + '</a>')
                    creators.append(creator_html)
                    if role['date']:
                        dates.append(role['date'])
            item['creators_with_url'] = '; '.join(creators) if creators else '-'
            item['date'] = min(dates) if dates else '-'

        # Sort roles alphabetically by role type
        data['roles'] = sorted(data['roles'],
                               key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')

        template_names = ['source/source_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class SourceList(generics.ListAPIView):
    model = CRIMSource
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMSourceListSerializer
    pagination_class = SourceSetPagination
    renderer_classes = (
        SourceListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'document_id')
        return CRIMSource.objects.all().order_by(order_by)


class SourceDetail(generics.RetrieveAPIView):
    model = CRIMSource
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMSourceDetailSerializer
    renderer_classes = (
        SourceDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMSource.objects.all()

    def get_object(self):
        url_arg = self.kwargs['document_id']
        document = CRIMSource.objects.filter(document_id=url_arg)
        if not document.exists():
            document = CRIMSource.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(document)
        self.check_object_permissions(self.request, obj)
        return obj


class SourceListData(generics.ListAPIView):
    model = CRIMSource
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMSourceListSerializer
    renderer_classes = (
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'document_id')
        return CRIMSource.objects.all().order_by(order_by)


class SourceDetailData(generics.RetrieveAPIView):
    model = CRIMSource
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMSourceDetailSerializer
    renderer_classes = (
        JSONRenderer,
    )
    queryset = CRIMSource.objects.all()

    def get_object(self):
        url_arg = self.kwargs['document_id']
        document = CRIMSource.objects.filter(document_id=url_arg)
        if not document.exists():
            document = CRIMSource.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(document)
        self.check_object_permissions(self.request, obj)
        return obj
