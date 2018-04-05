from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from django.contrib.auth.models import User
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.genre import CRIMGenreSerializer
from crim.models.genre import CRIMGenre
from rest_framework.response import Response
from rest_framework import status


class GenreListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['genre/genre_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class GenreDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['genre/genre_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class GenreList(generics.ListAPIView):
    model = CRIMGenre
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMGenreSerializer
    renderer_classes = (JSONRenderer,)  # can add html later

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'genre_id')
        return CRIMGenre.objects.all().order_by(order_by)


class GenreDetail(generics.RetrieveAPIView):
    model = CRIMGenre
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMGenreSerializer
    renderer_classes = (JSONRenderer,)  # can add html later
    queryset = CRIMGenre.objects.all()

    def get_object(self):
        url_arg = self.kwargs['pk']
        genre = CRIMGenre.objects.filter(genre_id=url_arg)
        if not genre.exists():
            genre = CRIMGenre.objects.filter(name_sort__iexact=url_arg)

        obj = get_object_or_404(genre)
        self.check_object_permissions(self.request, obj)
        return obj
