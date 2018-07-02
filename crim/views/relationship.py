from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.relationship import CRIMRelationshipSerializer
from crim.models.relationship import CRIMRelationship


class RelationshipSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the relationship_list.html template!
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 30


class RelationshipListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationship/relationship_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class RelationshipDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationship/relationship_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class RelationshipList(generics.ListAPIView):
    model = CRIMRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipSerializer
    pagination_class = RelationshipSetPagination
    renderer_classes = (
        RelationshipListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'model_observation__piece_id')
        return CRIMRelationship.objects.all().order_by(order_by)


class RelationshipDetail(generics.RetrieveAPIView):
    model = CRIMRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipSerializer
    renderer_classes = (
        RelationshipDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMRelationship.objects.all()

    def get_object(self):
        url_arg = self.kwargs['pk']
        relationship = CRIMRelationship.objects.filter(pk=url_arg)
        obj = get_object_or_404(relationship)
        self.check_object_permissions(self.request, obj)
        return obj


class RelationshipListData(RelationshipList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


class RelationshipDetailData(RelationshipDetail):
    renderer_classes = (JSONRenderer,)
