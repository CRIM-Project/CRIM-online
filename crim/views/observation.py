from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.observation import CRIMObservationSerializer
from crim.models.observation import CRIMObservation
from crim.models.piece import CRIMPiece


class ObservationSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the observation_list.html template!
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 45


class ObservationListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['observation/observation_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class ObservationDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['observation/observation_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class ObservationList(generics.ListAPIView):
    model = CRIMObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMObservationSerializer
    pagination_class = ObservationSetPagination
    renderer_classes = (
        ObservationListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'piece_id')
        return CRIMObservation.objects.all().order_by(order_by)


class ObservationDetail(generics.RetrieveAPIView):
    model = CRIMObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMObservationSerializer
    renderer_classes = (
        ObservationDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMObservation.objects.all()

    def get_object(self):
        url_arg = self.kwargs['pk']
        observation = CRIMObservation.objects.filter(pk=url_arg)
        obj = get_object_or_404(observation)
        self.check_object_permissions(self.request, obj)
        return obj


class ObservationListData(ObservationList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


class ObservationDetailData(ObservationDetail):
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        observation = get_object_or_404(CRIMObservation, pk=pk)
        # Not allowed to POST if there is no CRIMPerson associated with this user
        if request.user.is_anonymous or not request.user.profile.person:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif comment.author != request.user.profile and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            serialized = CRIMObservationSerializer(observation, data=request.data, context={'request': request})
            if not serialized.is_valid():
                return Response({'serialized': serialized, 'content': observation})
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)


class ObservationCreateData(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # Not allowed to POST if there is no CRIMPerson associated with this user
        if request.user.is_anonymous or not request.user.profile.person:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            observation = CRIMObservation(
                observer=request.user.profile.person,
                piece=CRIMPiece.objects.get(piece_id=request.data['piece']),
            )
            serialized = CRIMObservationSerializer(observation, data=request.data, context={'request': request})
            if not serialized.is_valid():
                return Response({'serialized': serialized, 'content': observation})
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
