from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.serializers.phrase import CRIMPhraseSerializer
from crim.models.phrase import CRIMPhrase


class PhraseListData(generics.ListAPIView):
    model = CRIMPhrase
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPhraseSerializer
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        return CRIMPhrase.objects.all()


class PhraseDetailData(generics.RetrieveAPIView):
    model = CRIMPhrase
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPhraseSerializer
    renderer_classes = (JSONRenderer,)
    queryset = CRIMPhrase.objects.all()

    def get_object(self):
        url_arg = self.kwargs['phrase_id']
        phrase = CRIMPhrase.objects.filter(id=url_arg)
        if not phrase.exists():
            phrase = CRIMPhrase.objects.filter(name__iexact=url_arg)

        obj = get_object_or_404(phrase)
        self.check_object_permissions(self.request, obj)
        return obj
