from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.genre import CRIMGenreSerializer
from crim.models.genre import CRIMGenre

COMPOSER = 'Composer'


class GenreListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['genre/genre_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class GenreList(generics.ListAPIView):
    model = CRIMGenre
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMGenreSerializer
    renderer_classes = (
        GenreListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'genre_id')
        return CRIMGenre.objects.exclude(pieces__isnull=True).order_by(order_by)


class GenreDetail(generics.RetrieveAPIView):
    model = CRIMGenre
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMGenreSerializer
    renderer_classes = (
        JSONRenderer,
    )
    queryset = CRIMGenre.objects.all()

    def get_object(self):
        url_arg = self.kwargs['genre_id']
        genre = CRIMGenre.objects.filter(genre_id=url_arg)
        if not genre.exists():
            genre = CRIMGenre.objects.filter(name__iexact=url_arg)

        obj = get_object_or_404(genre)
        self.check_object_permissions(self.request, obj)
        return obj


class GenreListData(GenreList):
    renderer_classes = (JSONRenderer,)


class GenreDetailData(GenreDetail):
    renderer_classes = (JSONRenderer,)
