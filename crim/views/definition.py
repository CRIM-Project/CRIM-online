from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from crim.models.definition import CRIMDefinition
from crim.serializers.definition import CRIMDefinitionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
#from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer


class DefinitionListData(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, format=None):
        definitions = CRIMDefinition.objects.all()
        serializer = CRIMDefinitionSerializer(definitions, many=True, context={'request':request})
        return Response(serializer.data)

class DefinitionDetailData(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, pk):
        definition = get_object_or_404(CRIMDefinition, pk=pk)
        serializer = CRIMDefinitionSerializer(definition, context={'request': request})
        return Response(serializer.data)
