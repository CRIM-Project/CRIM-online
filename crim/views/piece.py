from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.piece import CRIMPieceListSerializer, CRIMPieceDetailSerializer, CRIMPieceWithObservationsSerializer, CRIMPieceWithRelationshipsSerializer
from crim.models.genre import CRIMGenre
from crim.models.piece import CRIMPiece

COMPOSER = 'composer'
PUBLISHER = 'printer'


class PieceSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the all_piece_list.html template!
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15


class AllPieceListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Add `content.filter_genre` item if there is a url parameter
        # that matches a genre in the database.
        if renderer_context['request'].GET.get('genre') and CRIMGenre.objects.filter(genre_id=renderer_context['request'].GET.get('genre')):
            data['filter_genre'] = CRIMGenre.objects.get(genre_id=renderer_context['request'].GET.get('genre'))

        template_names = ['piece/all_piece_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class ModelListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['piece/model_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class PieceDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Sort roles alphabetically by role type
        data['roles'] = sorted(data['roles'],
                               key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')
        template_names = ['piece/piece_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class PieceWithObservationsHTMLRenderer(PieceDetailHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data['show_observations'] = True
        # Sort roles alphabetically by role type
        data['roles'] = sorted(data['roles'],
                               key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')
        template_names = ['piece/piece_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class PieceWithRelationshipsHTMLRenderer(PieceDetailHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data['show_relationships'] = True
        # Sort roles alphabetically by role type
        data['roles'] = sorted(data['roles'],
                               key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')
        template_names = ['piece/piece_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class PieceList(generics.ListAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceListSerializer
    pagination_class = PieceSetPagination
    renderer_classes = (
        AllPieceListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'piece_id')
        if self.request.GET.get('genre') and CRIMGenre.objects.filter(genre_id=self.request.GET.get('genre')):
            genre = CRIMGenre.objects.get(genre_id=self.request.GET.get('genre'))
            return CRIMPiece.objects.filter(genre=genre).distinct().order_by(order_by)
        else:
            return CRIMPiece.objects.all().distinct().order_by(order_by)


class ModelList(generics.ListAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceListSerializer
    renderer_classes = (
        ModelListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'piece_id')
        return CRIMPiece.objects.filter(mass=None).order_by(order_by)


class PieceDetail(generics.RetrieveAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceDetailSerializer
    renderer_classes = (
        PieceDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMPiece.objects.all()

    def get_queryset(self):
        return CRIMPiece.objects.filter(mass=None)

    def get_object(self):
        url_arg = self.kwargs['piece_id']
        piece = CRIMPiece.objects.filter(piece_id=url_arg)
        if not piece.exists():
            piece = CRIMPiece.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(piece)
        self.check_object_permissions(self.request, obj)
        return obj


class PieceWithObservations(generics.RetrieveAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceWithObservationsSerializer
    renderer_classes = (
        PieceWithObservationsHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMPiece.objects.all()

    def get_queryset(self):
        return CRIMPiece.objects.filter(mass=None)

    def get_object(self):
        url_arg = self.kwargs['piece_id']
        piece = CRIMPiece.objects.filter(piece_id=url_arg)
        if not piece.exists():
            piece = CRIMPiece.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(piece)
        self.check_object_permissions(self.request, obj)
        return obj


class PieceWithRelationships(generics.RetrieveAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceWithRelationshipsSerializer
    renderer_classes = (
        PieceWithRelationshipsHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMPiece.objects.all()

    def get_queryset(self):
        return CRIMPiece.objects.filter(mass=None)

    def get_object(self):
        url_arg = self.kwargs['piece_id']
        piece = CRIMPiece.objects.filter(piece_id=url_arg)
        if not piece.exists():
            piece = CRIMPiece.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(piece)
        self.check_object_permissions(self.request, obj)
        return obj


class PieceListData(PieceList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


class ModelListData(ModelList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


class PieceDetailData(PieceDetail):
    renderer_classes = (JSONRenderer,)


class PieceWithObservationsData(PieceWithObservations):
    renderer_classes = (JSONRenderer,)


class PieceWithRelationshipsData(PieceWithRelationships):
    renderer_classes = (JSONRenderer,)
