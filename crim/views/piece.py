from django.core.cache import caches
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer

from crim.helpers.common import cache_values_to_string
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.piece import CRIMPieceListSerializer, CRIMPieceDetailSerializer, CRIMPieceScoreSerializer, CRIMPieceWithSourcesSerializer, CRIMPieceWithRelationshipsSerializer, CRIMPieceWithRelationshipsDataSerializer, CRIMPieceWithDiscussionsSerializer
from crim.models.forum import CRIMForumPost
from crim.models.genre import CRIMGenre
from crim.models.piece import CRIMPiece

import os
import re
import verovio


def render_piece(piece_id, page_number):
    tk = verovio.toolkit()
    raw_mei = open(os.path.join('crim/static/mei/MEI_3.0', piece_id + '.mei')).read()

    tk.setOption('noHeader', 'true')
    tk.setOption('noFooter', 'true')
    # Calculate optimal size of score window based on number of voices
    tk.setOption('pageHeight', '1152')
    tk.setOption('adjustPageHeight', 'true')
    tk.setOption('spacingSystem', '12')
    tk.setOption('spacingDurDetection', 'true')
    tk.setOption('pageWidth', '2048')

    tk.loadData(raw_mei)
    tk.setScale(35)

    svg = tk.renderToSVG(page_number)
    # print('Saving cache for ' + repr(cache_values_to_string(piece_id, page_number)))
    caches['pieces'].set(cache_values_to_string(piece_id, page_number), svg, None)

    return svg


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
        # Sort roles alphabetically by role type, including mass roles
        all_roles = data['mass']['roles'] + data['roles'] if data['mass'] else data['roles']
        data['roles'] = sorted(all_roles, key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')

        page_number_string = renderer_context['request'].GET.get('p')
        page_number = eval(page_number_string) if page_number_string else 1
        data['page_number'] = page_number

        # Load the svg from cache based on piece and page number
        cached_svg = caches['pieces'].get(cache_values_to_string(data['piece_id'], page_number))

        # print(repr(cache_values_to_string(data['piece_id'], page_number)))
        if cached_svg:
            # print('We have a cache for <{}> page {}'.format(data['piece_id'], page_number))
            data['svg'] = cached_svg
        # If it wasn't in cache, then render the MEI
        else:
            # print('NO CACHE for <{}> page {}'.format(data['piece_id'], page_number))
            data['svg'] = render_piece(data['piece_id'], page_number)

        template_names = ['piece/piece_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class PieceWithSourcesHTMLRenderer(PieceDetailHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data['show_sources'] = True
        # Sort roles alphabetically by role type, including mass roles
        all_roles = data['mass']['roles'] + data['roles'] if data['mass'] else data['roles']
        data['roles'] = sorted(all_roles, key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')

        template_names = ['piece/piece_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class PieceWithRelationshipsHTMLRenderer(PieceDetailHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data['show_relationships'] = True
        # Sort roles alphabetically by role type, including mass roles
        all_roles = data['mass']['roles'] + data['roles'] if data['mass'] else data['roles']
        data['roles'] = sorted(all_roles, key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')

        template_names = ['piece/piece_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class PieceWithDiscussionsHTMLRenderer(PieceDetailHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data['show_discussions'] = True

        # Fetch all posts which mention the piece in the title or body.
        pid = data['piece_id'].lower()
        related = CRIMForumPost.objects.filter(
            Q(text__icontains=pid) | Q(title__icontains=pid)
        )
        data['discussions'] = related

        # Sort roles alphabetically by role type, including mass roles
        all_roles = data['mass']['roles'] + data['roles'] if data['mass'] else data['roles']
        data['roles'] = sorted(all_roles, key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')

        template_names = ['piece/piece_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
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
        genre_name = self.request.GET.get('genre')
        if genre_name:
            return CRIMPiece.objects.filter(genre__genre_id=genre_name).distinct().order_by(order_by).select_related('genre', 'composer')
        else:
            # We want to put models before masses when sorting by piece_id
            if order_by == 'piece_id':
                return CRIMPiece.objects.distinct().order_by(
                        F('mass').asc(nulls_first=True), 'piece_id').select_related('genre', 'composer')
            else:
                return CRIMPiece.objects.all().distinct().order_by(order_by).select_related('genre', 'composer')


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
        return CRIMPiece.objects.filter(mass=None).order_by(order_by).select_related('genre', 'composer')


class PieceDetail(generics.RetrieveAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceScoreSerializer
    renderer_classes = (
        PieceDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMPiece.objects.all()

    def get_object(self):
        url_arg = self.kwargs['piece_id']
        piece = CRIMPiece.objects.filter(piece_id=url_arg).prefetch_related(
            'roles_as_piece__role_type',
            'roles_as_piece__person',
            'mass__roles_as_mass__role_type',
            'mass__roles_as_mass__person',
        )
        if not piece.exists():
            piece = CRIMPiece.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(piece)
        self.check_object_permissions(self.request, obj)
        return obj


class PieceWithSources(generics.RetrieveAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceWithSourcesSerializer
    renderer_classes = (
        PieceWithSourcesHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMPiece.objects.all()

    def get_object(self):
        url_arg = self.kwargs['piece_id']
        piece = CRIMPiece.objects.filter(piece_id=url_arg).prefetch_related(
            'sources__roles_as_source',
            'roles_as_piece__role_type',
            'roles_as_piece__person',
            'mass__roles_as_mass__role_type',
            'mass__roles_as_mass__person',
            'phrases__part',
        )
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

    def get_object(self):
        url_arg = self.kwargs['piece_id']
        piece = CRIMPiece.objects.filter(piece_id=url_arg).prefetch_related(
            'roles_as_piece__role_type',
            'roles_as_piece__person',
            'mass__roles_as_mass__role_type',
            'mass__roles_as_mass__person',
        )
        if not piece.exists():
            piece = CRIMPiece.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(piece)
        self.check_object_permissions(self.request, obj)
        return obj


class PieceWithDiscussions(generics.RetrieveAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceWithDiscussionsSerializer
    renderer_classes = (
        PieceWithDiscussionsHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMPiece.objects.all()

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
    serializer_class = CRIMPieceDetailSerializer


class PieceWithRelationshipsData(generics.RetrieveAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceWithRelationshipsDataSerializer
    renderer_classes = (JSONRenderer,)
    queryset = CRIMPiece.objects.all()

    def get_object(self):
        url_arg = self.kwargs['piece_id']
        piece = CRIMPiece.objects.filter(piece_id=url_arg).prefetch_related(
            'roles_as_piece__role_type',
            'roles_as_piece__person',
            'mass__roles_as_mass__role_type',
            'mass__roles_as_mass__person',
            'relationships_as_model__observer',
            'relationships_as_model__model_observation__observer',
            'relationships_as_model__model_observation__piece',
            'relationships_as_model__derivative_observation__observer',
            'relationships_as_model__derivative_observation__piece',
            'relationships_as_derivative__observer',
            'relationships_as_derivative__model_observation__observer',
            'relationships_as_derivative__model_observation__piece',
            'relationships_as_derivative__derivative_observation__observer',
            'relationships_as_derivative__derivative_observation__piece',
        )
        if not piece.exists():
            piece = CRIMPiece.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(piece)
        self.check_object_permissions(self.request, obj)
        return obj
