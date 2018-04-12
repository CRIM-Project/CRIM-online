from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from django.contrib.auth.models import User
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.relationship import CRIMRelationshipSerializer
from crim.models.relationship import CRIMRelationship
from rest_framework.response import Response
from rest_framework import status


class RelationshipListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationship/relationship_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
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
    renderer_classes = (JSONRenderer,)  # can add html later

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'relationship_id')
        return CRIMRelationship.objects.all().order_by(order_by)


class RelationshipDetail(generics.RetrieveAPIView):
    model = CRIMRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipSerializer
    renderer_classes = (JSONRenderer,)  # can add html later
    queryset = CRIMRelationship.objects.all()

    def get_object(self):
        url_arg = self.kwargs['relationship_id']
        relationship = CRIMRelationship.objects.filter(relationship_id=url_arg)
        obj = get_object_or_404(relationship)
        self.check_object_permissions(self.request, obj)
        return obj
