from django.core.cache import caches
from django.shortcuts import get_object_or_404
from django.contrib.staticfiles.storage import staticfiles_storage

from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from crim.helpers.common import cache_values_to_string
from crim.models.definition import CRIMDefinition
from crim.models.observation import CRIMObservation
from crim.models.observation import CJObservation
from crim.models.piece import CRIMPiece
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.observation import CRIMObservationDetailSerializer, CRIMObservationListSerializer, CRIMObservationBriefSerializer
from crim.serializers.observation import CJObservationDetailSerializer, CJObservationListSerializer, CJObservationBriefSerializer

import os


def generate_observation_data(request, prefix=''):
    def post_data(v):
        field = request.data.get(prefix + ('_' if prefix else '') + v)
        if field == 'true':
            return True
        elif field == 'false' or field == None:
            return False
        else:
            return field

    observation_data = {}

    if post_data('piece'):
        observation_data['piece'] = CRIMPiece.objects.get(piece_id=post_data('piece'))
    if post_data('ema'):
        observation_data['ema'] = post_data('ema')
    if post_data('musical_type'):
        observation_data['musical_type'] = post_data('musical_type')
    if post_data('definition'):
        observation_data['definition'] = CRIMDefinition.objects.get(id=post_data('definition'))
    if post_data('details'):
        observation_data['details'] = post_data('details')
    if post_data('remarks'):
        observation_data['remarks'] = post_data('remarks')

    return observation_data


def create_observation_from_request(request, prefix=''):
    observation_data = generate_observation_data(request, prefix)
    observation_data['observer'] = request.user.profile.person
    new_observation = CJObservation(**observation_data)
    return new_observation


class ObservationSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the observation_list.html template!
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 150


# Deprecated class
class ObservationOldListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['observation/observation_old_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)

class ObservationListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['observation/observation_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


# Deprecated class
class ObservationOldDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        raw_mei = open(os.path.join('crim/static/mei/MEI_3.0', data['piece']['piece_id'] + '.mei')).read()
        data['mei'] = raw_mei

        template_names = ['observation/observation_old_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)

class ObservationDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        raw_mei = staticfiles_storage.open('mei/MEI_3.0/' + data['piece']['piece_id'] + '.mei').read()
        data['mei'] = raw_mei.decode()

        template_names = ['observation/observation_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


# Deprecated class
class ObservationOldList(generics.ListAPIView):
    model = CRIMObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMObservationListSerializer
    pagination_class = ObservationSetPagination
    renderer_classes = (
        ObservationOldListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'pk')
        if self.request.user.is_authenticated:
            return CRIMObservation.objects.all().order_by(order_by).select_related(
                'observer',
                'piece',
                'piece__mass',
            )
        else:
            return CRIMObservation.objects.filter(curated=True).order_by(order_by).select_related(
                'observer',
                'piece',
                'piece__mass',
            )

class ObservationList(generics.ListAPIView):
    model = CJObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CJObservationListSerializer
    pagination_class = ObservationSetPagination
    renderer_classes = (
        ObservationListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'pk')
        if self.request.user.is_authenticated:
            return CJObservation.objects.all().order_by(order_by).select_related(
                'observer',
                'piece',
                'piece__mass',
            )
        else:
            return CJObservation.objects.filter(curated=True).order_by(order_by).select_related(
                'observer',
                'piece',
                'piece__mass',
            )


# Deprecated class
class ObservationOldDetail(generics.RetrieveAPIView):
    model = CRIMObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMObservationDetailSerializer
    renderer_classes = (
        ObservationOldDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMObservation.objects.all()

    def get_object(self):
        url_arg = self.kwargs['id']
        observation = CRIMObservation.objects.filter(id=url_arg).select_related(
            'observer',
            'piece',
            'piece__mass',
        )
        obj = get_object_or_404(observation)
        self.check_object_permissions(self.request, obj)
        return obj

class ObservationDetail(generics.RetrieveAPIView):
    model = CJObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CJObservationDetailSerializer
    renderer_classes = (
        ObservationDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CJObservation.objects.all()

    def get_object(self):
        url_arg = self.kwargs['id']
        observation = CJObservation.objects.filter(id=url_arg).select_related(
            'observer',
            'piece',
            'piece__mass',
        )
        obj = get_object_or_404(observation)
        self.check_object_permissions(self.request, obj)
        return obj


# Deprecated class
class ObservationOldListData(ObservationOldList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)

class ObservationListData(ObservationList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


# Deprecated class
class ObservationOldListBriefData(ObservationOldListData):
    serializer_class = CRIMObservationBriefSerializer

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'pk')
        return CRIMObservation.objects.filter(curated=True).order_by(order_by).only(
            'observer',
            'musical_type',
            'piece',
            'ema',
        )

class ObservationListBriefData(ObservationListData):
    serializer_class = CJObservationBriefSerializer

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'pk')
        return CJObservation.objects.filter(curated=True).order_by(order_by).only(
            'observer',
            'musical_type',
            'piece',
            'ema',
        )


# Deprecated class
class ObservationOldDetailData(generics.RetrieveUpdateAPIView):
    model = CRIMObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMObservationDetailSerializer
    renderer_classes = (JSONRenderer,)
    queryset = CRIMObservation.objects.all()

    def get_object(self):
        url_arg = self.kwargs['id']
        observation = CRIMObservation.objects.filter(id=url_arg)
        obj = get_object_or_404(observation)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        if request.user.is_staff:
            instance = self.get_object()
            observation_data = generate_observation_data(request)
            for k, v in observation_data.items():
                setattr(instance, k, v)

            instance.save()

            serialized = CRIMObservationDetailSerializer(instance, data=request.data, context={'request': request})
            # serialized = self.get_serializer(instance)
            if serialized.is_valid():
                if request.user.is_staff:
                    serialized.validated_data['curated'] = True
            else:
                raise ValidationError(serialized.errors)
            self.perform_update(serialized)

            return Response(serialized.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class ObservationDetailData(generics.RetrieveUpdateAPIView):
    model = CJObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CJObservationDetailSerializer
    renderer_classes = (JSONRenderer,)
    queryset = CJObservation.objects.all()

    def get_object(self):
        url_arg = self.kwargs['id']
        observation = CJObservation.objects.filter(id=url_arg)
        obj = get_object_or_404(observation)
        self.check_object_permissions(self.request, obj)
        return obj

    def put(self, request, *args, **kwargs):
        if request.user.is_staff:
            instance = self.get_object()
            observation_data = generate_observation_data(request)
            for k, v in observation_data.items():
                setattr(instance, k, v)

            instance.save()

            serialized = CRIMObservationDetailSerializer(instance, data=request.data, context={'request': request})
            # serialized = self.get_serializer(instance)
            if serialized.is_valid():
                if request.user.is_staff:
                    serialized.validated_data['curated'] = True
            else:
                raise ValidationError(serialized.errors)
            self.perform_update(serialized)

            return Response(serialized.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ObservationCreateData(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # Not allowed to POST if there is no CRIMPerson associated with this user
        if not request.user.is_authenticated or not request.user.profile.person:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        observation_or_response = create_observation_from_request(request, '')
        if isinstance(observation_or_response, Response):
            return observation_or_response

        observation = observation_or_response
        serialized = CJObservationDetailSerializer(observation, data=request.data, context={'request': request})
        # If the user is an admin, the observation should be marked as curated.
        if serialized.is_valid():
            if request.user.is_staff:
                serialized.validated_data['curated'] = True
        else:
            return Response({'serialized': serialized, 'content': observation})

        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
