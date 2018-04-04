from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from django.contrib.auth.models import User
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.piece import CRIMPieceListSerializer, CRIMPieceDetailSerializer
from crim.models.piece import CRIMPiece
from rest_framework.response import Response
from rest_framework import status


class PieceListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['piece/piece_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class PieceDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['piece/piece_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class PieceList(generics.ListAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceListSerializer
    renderer_classes = (
        # PieceListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'piece_id')
        return CRIMPiece.objects.all().order_by(order_by)


class PieceDetail(generics.RetrieveAPIView):
    model = CRIMPiece
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPieceDetailSerializer
    renderer_classes = (
        # PieceDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMPiece.objects.all()

    def get_object(self):
        url_arg = self.kwargs['pk']
        piece = CRIMPiece.objects.filter(piece_id=url_arg)
        if not piece.exists():
            piece = CRIMPiece.objects.filter(name_sort__iexact=url_arg)

        obj = get_object_or_404(piece)
        self.check_object_permissions(self.request, obj)
        return obj
