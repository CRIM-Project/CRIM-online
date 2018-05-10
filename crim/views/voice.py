from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.serializers.voice import CRIMVoiceSerializer
from crim.models.voice import CRIMVoice


class VoiceListData(generics.ListAPIView):
    model = CRIMVoice
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMVoiceSerializer
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        return CRIMVoice.objects.all()


class VoiceDetailData(generics.RetrieveAPIView):
    model = CRIMVoice
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMVoiceSerializer
    renderer_classes = (JSONRenderer,)
    queryset = CRIMVoice.objects.all()

    def get_object(self):
        url_arg = self.kwargs['voice_id']
        voice = CRIMVoice.objects.filter(id=url_arg)
        if not voice.exists():
            voice = CRIMVoice.objects.filter(name__iexact=url_arg)

        obj = get_object_or_404(voice)
        self.check_object_permissions(self.request, obj)
        return obj
