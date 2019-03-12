from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from crim.models.observation import CRIMObservation
from crim.models.relationship import CRIMRelationship
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.observation import CRIMObservationSerializer
from crim.serializers.relationship import CRIMRelationshipSerializer
from crim.views.observation import create_observation_from_request


def generate_relationship_data(request):
    def post_data(v):
        return request.POST.get(v)

    # Don't allow if more than one relationship type has been selected.
    list_of_relationship_types = [
        post_data('rt_q'),
        post_data('rt_tm'),
        post_data('rt_tnm'),
        post_data('rt_nm'),
        post_data('rt_om'),
    ]
    if sum(bool(x) for x in list_of_relationship_types) > 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    relationship_data = {}

    # If observation IDs are provided, use those; otherwise, we will
    # need fields preceded with `model_mt_` fields. If neither of these is
    # provided, we may be dealing with an update and not a new relationship.
    if post_data('model_observation'):
        model_observation = CRIMObservation.objects.get(id=post_data('model_observation'))
    elif post_data('model_piece'):
        model_observation_or_response = create_observation_from_request(request, 'model')
        if isinstance(model_observation_or_response, Response):
            return response
        else:
            model_observation = model_observation_or_response
            serialized_model = CRIMObservationSerializer(model_observation, data={}, context={'request': request})
            if not serialized_model.is_valid():
                return Response({'serialized': serialized_model, 'content': model_observation})

    if post_data('derivative_observation'):
        derivative_observation = CRIMObservation.objects.get(id=post_data('derivative_observation'))
    elif post_data('derivative_piece'):
        derivative_observation_or_response = create_observation_from_request(request, 'derivative')
        if isinstance(derivative_observation_or_response, Response):
            return response
        else:
            derivative_observation = derivative_observation_or_response
            serialized_derivative = CRIMObservationSerializer(derivative_observation, data={}, context={'request': request})
            if not serialized_derivative.is_valid():
                return Response({'serialized': serialized_derivative, 'content': derivative_observation})

    # Only save observations now, which is when we know that the entire POST will succeed
    if not post_data('model_observation') and post_data('model_piece'):
        serialized_model.save()
    if not post_data('derivative_observation') and post_data('derivative_piece'):
        serialized_derivative.save()

    if post_data('model_observation') or post_data('model_piece'):
        relationship_data['model_observation'] = model_observation

    if post_data('derivative_observation') or post_data('derivative_piece'):
        relationship_data['derivative_observation'] = derivative_observation

    if post_data('rt_q'):
        relationship_data['rt_q'] = True
        relationship_data['rt_q_x'] = True if post_data('rt_q_x') else ''
        relationship_data['rt_q_monnayage'] = True if post_data('rt_q_monnayage') else False
    elif post_data('rt_tm'):
        relationship_data['rt_tm'] = True
        relationship_data['rt_tm_snd'] = True if post_data('rt_tm_snd') else False
        relationship_data['rt_tm_minv'] = True if post_data('rt_tm_minv') else False
        relationship_data['rt_tm_retrograde'] = True if post_data('rt_tm_retrograde') else False
        relationship_data['rt_tm_ms'] = True if post_data('rt_tm_ms') else False
        relationship_data['rt_tm_transposed'] = True if post_data('rt_tm_transposed') else False
        relationship_data['rt_tm_invertible'] = True if post_data('rt_tm_invertible') else False
    elif post_data('rt_tnm'):
        relationship_data['rt_tnm'] = True
        relationship_data['rt_tnm_embellished'] = True if post_data('rt_tnm_embellished') else False
        relationship_data['rt_tnm_reduced'] = True if post_data('rt_tnm_reduced') else False
        relationship_data['rt_tnm_amplified'] = True if post_data('rt_tnm_amplified') else False
        relationship_data['rt_tnm_truncated'] = True if post_data('rt_tnm_truncated') else False
        relationship_data['rt_tnm_ncs'] = True if post_data('rt_tnm_ncs') else False
        relationship_data['rt_tnm_ocs'] = True if post_data('rt_tnm_ocs') else False
        relationship_data['rt_tnm_ocst'] = True if post_data('rt_tnm_ocst') else False
        relationship_data['rt_tnm_nc'] = True if post_data('rt_tnm_nc') else False
    elif post_data('rt_nm'):
        relationship_data['rt_nm'] = True
    elif post_data('rt_om'):
        relationship_data['rt_om'] = True

    if post_data('remarks'):
        relationship_data['remarks'] = post_data('remarks')

    return relationship_data


def create_relationship_from_request(request):
    relationship_data = generate_relationship_data(request)
    relationship_data['observer'] = request.user.profile.person
    new_relationship = CRIMRelationship(**relationship_data)
    return new_relationship


class RelationshipSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the relationship_list.html template!
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 30


class RelationshipListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationship/relationship_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class RelationshipDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationship/relationship_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class RelationshipList(generics.ListAPIView):
    model = CRIMRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipSerializer
    pagination_class = RelationshipSetPagination
    renderer_classes = (
        RelationshipListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'model_observation__piece_id')
        if self.request.user.is_authenticated:
            return CRIMRelationship.objects.all().order_by(order_by)
        else:
            return CRIMRelationship.objects.filter(curated=True).order_by(order_by)


class RelationshipDetail(generics.RetrieveAPIView):
    model = CRIMRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipSerializer
    renderer_classes = (
        RelationshipDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMRelationship.objects.all()

    def get_object(self):
        url_arg = self.kwargs['id']
        relationship = CRIMRelationship.objects.filter(id=url_arg)
        obj = get_object_or_404(relationship)
        self.check_object_permissions(self.request, obj)
        return obj


class RelationshipListData(RelationshipList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


class RelationshipDetailData(generics.RetrieveUpdateAPIView):
    model = CRIMRelationship
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMRelationshipSerializer
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

            serialized = CRIMRelationshipSerializer(instance, data=request.data, context={'request': request})
            # serialized = self.get_serializer(instance)
            serialized.is_valid(raise_exception=True)
            self.perform_update(serialized)

            response_headers = {
                'Access-Control-Allow-Methods': 'GET, PUT, HEAD, OPTIONS',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Allow-Headers': 'origin, content-type, accept',
            #     'Access-Control-Allow-Origin': 'http://127.0.0.1:8000',
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

        # If one of the observations returns an HTTP response, return that.
        relationship_or_response = create_relationship_from_request(request)
        if isinstance(relationship_or_response, Response):
            return Response

        # Otherwise, create the object.
        relationship = relationship_or_response
        serialized = CRIMRelationshipSerializer(relationship, data=request.data, context={'request': request})
        if not serialized.is_valid():
            return Response({'serialized': serialized, 'content': relationship})

        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
