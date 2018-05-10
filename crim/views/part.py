from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.serializers.part import CRIMPartSerializer
from crim.models.part import CRIMPart


class PartListData(generics.ListAPIView):
    model = CRIMPart
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPartSerializer
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        return CRIMPart.objects.all()


class PartDetailData(generics.RetrieveAPIView):
    model = CRIMPart
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPartSerializer
    renderer_classes = (JSONRenderer,)
    queryset = CRIMPart.objects.all()

    def get_object(self):
        url_arg = self.kwargs['part_id']
        part = CRIMPart.objects.filter(id=url_arg)
        if not part.exists():
            part = CRIMPart.objects.filter(name__iexact=url_arg)

        obj = get_object_or_404(part)
        self.check_object_permissions(self.request, obj)
        return obj
