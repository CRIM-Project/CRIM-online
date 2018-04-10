from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from django.contrib.auth.models import User
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.relationshiptype import CRIMRelationshipTypeSerializer
from crim.models.relationship import CRIMRelationshipType
from rest_framework.response import Response
from rest_framework import status


class RelationshipTypeListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationshiptype/relationshiptype_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class RelationshipTypeDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationshiptype/relationshiptype_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class RelationshipTypeList(generics.ListAPIView):
    model = CRIMRelationshipType
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipTypeSerializer
    renderer_classes = (JSONRenderer,)  # can add html later

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'relationship_type_id')
        return CRIMRelationshipType.objects.all().order_by(order_by)


class RelationshipTypeDetail(generics.RetrieveAPIView):
    model = CRIMRelationshipType
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipTypeSerializer
    renderer_classes = (JSONRenderer,)  # can add html later
    queryset = CRIMRelationshipType.objects.all()

    def get_object(self):
        url_arg = self.kwargs['pk']
        relationshiptype = CRIMRelationshipType.objects.filter(relationship_type_id=url_arg)
        obj = get_object_or_404(relationshiptype)
        self.check_object_permissions(self.request, obj)
        return obj
