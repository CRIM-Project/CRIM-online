from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from django.contrib.auth.models import User
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.musicaltype import CRIMMusicalTypeSerializer
from crim.models.relationship import CRIMMusicalType
from rest_framework.response import Response
from rest_framework import status


class MusicalTypeListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['musicaltype/musicaltype_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class MusicalTypeDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['musicaltype/musicaltype_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class MusicalTypeList(generics.ListAPIView):
    model = CRIMMusicalType
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMMusicalTypeSerializer
    renderer_classes = (JSONRenderer,)  # can add html later

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'musical_type_id')
        return CRIMMusicalType.objects.all().order_by(order_by)


class MusicalTypeDetail(generics.RetrieveAPIView):
    model = CRIMMusicalType
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMMusicalTypeSerializer
    renderer_classes = (JSONRenderer,)  # can add html later
    queryset = CRIMMusicalType.objects.all()

    def get_object(self):
        url_arg = self.kwargs['pk']
        musicaltype = CRIMMusicalType.objects.filter(musical_type_id=url_arg)
        obj = get_object_or_404(musicaltype)
        self.check_object_permissions(self.request, obj)
        return obj
