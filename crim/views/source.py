from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.source import CRIMSourceListSerializer, CRIMSourceDetailSerializer
from crim.models.document import CRIMSource


class SourceSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the source_list.html template!
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15


class SourceListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['source/source_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class SourceDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Sort roles alphabetically by role type
        data['roles'] = sorted(data['roles'],
                               key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')

        template_names = ['source/source_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
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
        return CRIMSource.objects.all().order_by(order_by).select_related('publisher')


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


class SourceListData(SourceList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


class SourceDetailData(SourceDetail):
    renderer_classes = (JSONRenderer,)
