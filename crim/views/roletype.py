from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.roletype import CRIMRoleTypeSerializer
from crim.models.role import CRIMRoleType

ANALYST = 'analyst'


class RoleTypeListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['roletype/roletype_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class RoleTypeList(generics.ListAPIView):
    model = CRIMRoleType
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRoleTypeSerializer
    renderer_classes = (
        RoleTypeListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'role_type_id')
        return CRIMRoleType.objects.filter(Q(roles__isnull=False) | Q(role_type_id=ANALYST)).distinct().order_by(order_by)


class RoleTypeDetail(generics.RetrieveAPIView):
    model = CRIMRoleType
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRoleTypeSerializer
    renderer_classes = (
        JSONRenderer,
    )
    queryset = CRIMRoleType.objects.all()

    def get_object(self):
        url_arg = self.kwargs['role_type_id']
        role_type = CRIMRoleType.objects.filter(role_type_id=url_arg)
        if not role_type.exists():
            role_type = CRIMRoleType.objects.filter(name__iexact=url_arg)

        obj = get_object_or_404(role_type)
        self.check_object_permissions(self.request, obj)
        return obj


class RoleTypeListData(RoleTypeList):
    renderer_classes = (JSONRenderer,)


class RoleTypeDetailData(RoleTypeDetail):
    renderer_classes = (JSONRenderer,)
