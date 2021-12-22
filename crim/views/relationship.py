from django.core.cache import caches
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from crim.helpers.common import cache_values_to_string
from crim.models.definition import CRIMDefinition
from crim.models.observation import CJObservation
from crim.models.relationship import CRIMRelationship
from crim.models.relationship import CJRelationship
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.observation import CJObservationDetailSerializer, CJObservationListSerializer
from crim.serializers.relationship import CRIMRelationshipDetailSerializer, CRIMRelationshipListSerializer, CRIMRelationshipBriefSerializer
from crim.serializers.relationship import CJRelationshipDetailSerializer, CJRelationshipListSerializer, CJRelationshipBriefSerializer
from crim.views.observation import create_observation_from_request

import os


def generate_relationship_data(request, model_observation_id=None, derivative_observation_id=None):
    def post_data(v):
        return request.data.get(v)

    relationship_data = {}

    # If observation IDs are provided, use those; otherwise, we will
    # need fields preceded with `model_mt_` fields. If neither of these is
    # provided, we may be dealing with an update and not a new relationship.
    if post_data('model_observation_id'):
        model_observation = CJObservation.objects.get(id=post_data('model_observation_id'))
    elif post_data('model_piece'):
        model_observation_or_response = create_observation_from_request(request, 'model')
        if isinstance(model_observation_or_response, Response):
            return response
        else:
            model_observation = model_observation_or_response
            serialized_model = CJObservationDetailSerializer(model_observation, data=request.data, context={'request': request})
            if serialized_model.is_valid():
                if request.user.is_staff:
                    serialized_model.validated_data['curated'] = True
            else:
                return Response({'serialized': serialized_model, 'content': model_observation})

    if post_data('derivative_observation_id'):
        derivative_observation = CJObservation.objects.get(id=post_data('derivative_observation_id'))
    elif post_data('derivative_piece'):
        derivative_observation_or_response = create_observation_from_request(request, 'derivative')
        if isinstance(derivative_observation_or_response, Response):
            return response
        else:
            derivative_observation = derivative_observation_or_response
            serialized_derivative = CJObservationDetailSerializer(derivative_observation, data=request.data, context={'request': request})
            if serialized_derivative.is_valid():
                if request.user.is_staff:
                    serialized_derivative.validated_data['curated'] = True
            else:
                return Response({'serialized': serialized_derivative, 'content': derivative_observation})

    # Wait to save observations till now, which is when we know that the entire POST will succeed
    if not post_data('model_observation_id') and post_data('model_piece'):
        serialized_model.save()
    if not post_data('derivative_observation_id') and post_data('derivative_piece'):
        serialized_derivative.save()

    if post_data('model_observation_id') or post_data('model_piece'):
        relationship_data['model_observation'] = model_observation
    if post_data('derivative_observation_id') or post_data('derivative_piece'):
        relationship_data['derivative_observation'] = derivative_observation
    if post_data('relationship_type'):
        relationship_data['relationship_type'] = post_data('relationship_type')
    if post_data('definition'):
        relationship_data['definition'] = CRIMDefinition.objects.get(id=post_data('definition'))
    if post_data('details'):
        relationship_data['details'] = post_data('details')
    if post_data('remarks'):
        relationship_data['remarks'] = post_data('remarks')

    return relationship_data


def create_relationship_from_request(request):
    relationship_data = generate_relationship_data(request)
    relationship_data['observer'] = request.user.profile.person
    new_relationship = CJRelationship(**relationship_data)
    return new_relationship


class RelationshipSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the relationship_list.html template!
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 150


# Deprecated class
class RelationshipOldListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationship/relationship_old_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)

class RelationshipListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationship/relationship_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


# Deprecated class
class RelationshipOldDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        model_raw_mei = open(os.path.join('crim/static/mei/MEI_3.0', data['model_observation']['piece']['piece_id'] + '.mei')).read()
        data['model_observation']['mei'] = model_raw_mei

        derivative_raw_mei = open(os.path.join('crim/static/mei/MEI_3.0', data['derivative_observation']['piece']['piece_id'] + '.mei')).read()
        data['derivative_observation']['mei'] = derivative_raw_mei

        template_names = ['relationship/relationship_old_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)

class RelationshipDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        model_raw_mei = open(os.path.join('crim/static/mei/MEI_3.0', data['model_observation']['piece']['piece_id'] + '.mei')).read()
        data['model_observation']['mei'] = model_raw_mei

        derivative_raw_mei = open(os.path.join('crim/static/mei/MEI_3.0', data['derivative_observation']['piece']['piece_id'] + '.mei')).read()
        data['derivative_observation']['mei'] = model_raw_mei

        template_names = ['relationship/relationship_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


# Deprecated class
class RelationshipOldList(generics.ListAPIView):
    model = CRIMRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipListSerializer
    pagination_class = RelationshipSetPagination
    renderer_classes = (
        RelationshipOldListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'pk')
        if self.request.user.is_authenticated:
            return CRIMRelationship.objects.all().order_by(order_by).select_related(
                'observer',
                'model_observation',
                'model_observation__piece',
                'model_observation__piece__mass',
                'derivative_observation',
                'derivative_observation__piece',
                'derivative_observation__piece__mass',
            )
        else:
            return CRIMRelationship.objects.filter(curated=True).order_by(order_by).select_related(
                'observer',
                'model_observation',
                'model_observation__piece',
                'model_observation__piece__mass',
                'derivative_observation',
                'derivative_observation__piece',
                'derivative_observation__piece__mass',
            )

class RelationshipList(generics.ListAPIView):
    model = CJRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CJRelationshipListSerializer
    pagination_class = RelationshipSetPagination
    renderer_classes = (
        RelationshipListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'pk')
        if self.request.user.is_authenticated:
            return CJRelationship.objects.all().order_by(order_by).select_related(
                'observer',
                'model_observation',
                'model_observation__piece',
                'model_observation__piece__mass',
                'derivative_observation',
                'derivative_observation__piece',
                'derivative_observation__piece__mass',
            )
        else:
            return CJRelationship.objects.filter(curated=True).order_by(order_by).select_related(
                'observer',
                'model_observation',
                'model_observation__piece',
                'model_observation__piece__mass',
                'derivative_observation',
                'derivative_observation__piece',
                'derivative_observation__piece__mass',
            )


# Deprecated class
class RelationshipOldDetail(generics.RetrieveAPIView):
    model = CRIMRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipDetailSerializer
    renderer_classes = (
        RelationshipOldDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMRelationship.objects.all()

    def get_object(self):
        url_arg = self.kwargs['id']
        relationship = CRIMRelationship.objects.filter(id=url_arg)
        obj = get_object_or_404(relationship)
        self.check_object_permissions(self.request, obj)
        return obj

class RelationshipDetail(generics.RetrieveAPIView):
    model = CJRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CJRelationshipDetailSerializer
    renderer_classes = (
        RelationshipDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMRelationship.objects.all()

    def get_object(self):
        url_arg = self.kwargs['id']
        relationship = CJRelationship.objects.filter(id=url_arg)
        obj = get_object_or_404(relationship)
        self.check_object_permissions(self.request, obj)
        return obj


# Deprecated class
class RelationshipOldListData(RelationshipOldList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)

class RelationshipListData(RelationshipList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


# Deprecated class
class RelationshipOldListBriefData(RelationshipOldListData):
    serializer_class = CRIMRelationshipBriefSerializer

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'pk')
        return CRIMRelationship.objects.filter(curated=True).order_by(order_by).select_related(
            'model_observation',
            'derivative_observation',
        ).only(
            'observer',
            'relationship_type',
            'model_observation__observer',
            'model_observation__musical_type',
            'model_observation__piece',
            'model_observation__ema',
            'derivative_observation__observer',
            'derivative_observation__musical_type',
            'derivative_observation__piece',
            'derivative_observation__ema',
        )

class RelationshipListBriefData(RelationshipListData):
    serializer_class = CJRelationshipBriefSerializer

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'pk')
        return CJRelationship.objects.filter(curated=True).order_by(order_by).select_related(
            'model_observation',
            'derivative_observation',
        ).only(
            'observer',
            'relationship_type',
            'model_observation__observer',
            'model_observation__musical_type',
            'model_observation__piece',
            'model_observation__ema',
            'derivative_observation__observer',
            'derivative_observation__musical_type',
            'derivative_observation__piece',
            'derivative_observation__ema',
        )


# Deprecated class
class RelationshipOldDetailData(generics.RetrieveUpdateAPIView):
    model = CRIMRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipDetailSerializer
    lookup_field = 'id'
    renderer_classes = (JSONRenderer,)
    queryset = CRIMRelationship.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            instance = self.get_object()
            relationship_data = generate_relationship_data(request)
            for k, v in relationship_data.items():
                setattr(instance, k, v)

            instance.save()

            serialized = CRIMRelationshipDetailSerializer(instance, data=request.data, context={'request': request})
            # serialized = self.get_serializer(instance)
            if serialized.is_valid():
                if request.user.is_staff:
                    serialized.validated_data['curated'] = True
            else:
                raise ValidationError(serialized.errors)
            self.perform_update(serialized)

            response_headers = {
                'Access-Control-Allow-Methods': 'GET, PUT, HEAD, OPTIONS',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Headers': 'origin, content-type, accept',
            }
            return Response(serialized.data, headers=response_headers, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class RelationshipDetailData(generics.RetrieveUpdateAPIView):
    model = CJRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CJRelationshipDetailSerializer
    lookup_field = 'id'
    renderer_classes = (JSONRenderer,)
    queryset = CRIMRelationship.objects.all()

    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            instance = self.get_object()
            relationship_data = generate_relationship_data(request)
            for k, v in relationship_data.items():
                setattr(instance, k, v)

            instance.save()

            serialized = CJRelationshipDetailSerializer(instance, data=request.data, context={'request': request})
            # serialized = self.get_serializer(instance)
            if serialized.is_valid():
                if request.user.is_staff:
                    serialized.validated_data['curated'] = True
            else:
                raise ValidationError(serialized.errors)
            self.perform_update(serialized)

            response_headers = {
                'Access-Control-Allow-Methods': 'GET, PUT, HEAD, OPTIONS',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Headers': 'origin, content-type, accept',
            }
            return Response(serialized.data, headers=response_headers, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RelationshipCreateData(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        # Not allowed to POST if there is no CRIMPerson associated with this user
        if not request.user.is_authenticated or not request.user.profile.person:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        relationship_or_response = create_relationship_from_request(request)
        if isinstance(relationship_or_response, Response):
            return relationship_or_response

        relationship = relationship_or_response
        serialized = CJRelationshipDetailSerializer(relationship, data=request.data, context={'request': request})

        if serialized.is_valid():
            if request.user.is_staff:
                serialized.validated_data['curated'] = True
        else:
            return Response({'serialized': serialized, 'content': relationship})

        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
