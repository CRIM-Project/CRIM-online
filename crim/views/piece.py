from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.piece import CRIMPieceListSerializer, CRIMPieceDetailSerializer
from crim.models.piece import CRIMPiece
from crim.common import earliest_date

COMPOSER = 'Composer'


class PieceListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        for piece in data:
            # Put pdf and mei links into a list rather than a \n-separated string
            piece['pdf_links'] = piece['pdf_links'].split('\n')
            piece['mei_links'] = piece['mei_links'].split('\n')
            # - Add `composer` field to content: only look at roles with
            # the role type with name "Composer", and add all such names
            # to the list, along with the url of the composer
            # - Add `date` field to content: again, only look at roles
            # with the role type "Composer"
            composers = []
            dates = []
            for role in piece['roles']:
                if role['role_type'] and role['role_type']['name'] == COMPOSER:
                    composer_html = ('<a href="' + role['person']['url'] +
                                     '">' + role['person']['name'] + '</a>')
                    composers.append(composer_html)
                    if role['date']:
                        dates.append(role['date'])
            piece['composers_with_url'] = '; '.join(composers) if composers else '-'
            # Only add one composer's date for clarity, choosing the earliest.
            piece['date'] = earliest_date(dates)

        template_names = ['piece/piece_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class PieceDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Put pdf and mei links into a list rather than a \n-separated string
        data['pdf_links'] = data['pdf_links'].split('\n')
        data['mei_links'] = data['mei_links'].split('\n')
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
    renderer_classes = (
        PieceListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'piece_id')
        return CRIMPiece.objects.all().order_by(order_by)


class ModelList(generics.ListAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceListSerializer
    renderer_classes = (
        PieceListHTMLRenderer,
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
            piece = CRIMPiece.objects.filter(name_sort__iexact=url_arg)

        obj = get_object_or_404(piece)
        self.check_object_permissions(self.request, obj)
        return obj


class PieceListData(generics.ListAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceListSerializer
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'piece_id')
        return CRIMPiece.objects.all().order_by(order_by)


class ModelListData(generics.ListAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceListSerializer
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'piece_id')
        return CRIMPiece.objects.filter(mass=None).order_by(order_by)


class PieceDetailData(generics.RetrieveAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceDetailSerializer
    renderer_classes = (JSONRenderer,)
    queryset = CRIMPiece.objects.all()

    def get_queryset(self):
        return CRIMPiece.objects.filter(mass=None)

    def get_object(self):
        url_arg = self.kwargs['piece_id']
        piece = CRIMPiece.objects.filter(piece_id=url_arg)
        if not piece.exists():
            piece = CRIMPiece.objects.filter(name_sort__iexact=url_arg)

        obj = get_object_or_404(piece)
        self.check_object_permissions(self.request, obj)
        return obj
