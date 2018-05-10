from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.serializers.role import CRIMRoleSerializer
from crim.models.role import CRIMRole


class RoleListData(generics.ListAPIView):
    model = CRIMRole
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRoleSerializer
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        return CRIMRole.objects.all()


class RoleDetailData(generics.RetrieveAPIView):
    model = CRIMRole
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRoleSerializer
    renderer_classes = (JSONRenderer,)
    queryset = CRIMRole.objects.all()

    def get_object(self):
        url_arg = self.kwargs['pk']
        role = CRIMRole.objects.filter(id=url_arg)

        obj = get_object_or_404(role)
        self.check_object_permissions(self.request, obj)
        return obj
