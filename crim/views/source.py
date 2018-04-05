from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from django.contrib.auth.models import User
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.models.document import CRIMSource
from crim.serializers.source import CRIMSourceListSerializer, CRIMSourceDetailSerializer
from rest_framework.response import Response
from rest_framework import status


class SourceListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['source/source_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class SourceDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['source/source_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class SourceList(generics.ListAPIView):
    model = CRIMSource
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMSourceListSerializer
    renderer_classes = (
        # SourceListHTMLRenderer,
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
        # SourceDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMSource.objects.all()

    def get_object(self):
        url_arg = self.kwargs['pk']
        document = CRIMSource.objects.filter(document_id=url_arg)
        if not document.exists():
            document = CRIMSource.objects.filter(name_sort__iexact=url_arg)

        obj = get_object_or_404(document)
        self.check_object_permissions(self.request, obj)
        return obj
