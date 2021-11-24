from django.core.cache import caches
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from crim.helpers.common import cache_values_to_string
from crim.models.definition import CRIMDefinition
from crim.models.observation import CRIMObservation
from crim.models.observation import CJObservation
from crim.models.piece import CRIMPiece
from crim.omas.localapi import slice_from_file
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.observation import CRIMObservationDetailSerializer, CRIMObservationListSerializer, CRIMObservationBriefSerializer
from crim.serializers.observation import CJObservationDetailSerializer, CJObservationListSerializer, CJObservationBriefSerializer

import os
import re
import verovio
import xml.etree.ElementTree as ET


def render_observation(observation_id, piece_id, ema, explicit_page_number=None):
    ET.register_namespace('', 'http://www.music-encoding.org/ns/mei')
    tk = verovio.toolkit()
    raw_mei = open(os.path.join('crim/static/mei/MEI_3.0', piece_id + '.mei')).read()
    cited_mei = slice_from_file(raw_mei, ema)
    plist_match = re.search(r'type="ema_highlight" plist="([^"]*)"', cited_mei)
    plist = plist_match.group(1) if plist_match else None
    highlight_list = plist.replace('#','').split() if plist else []

    tk.setOption('noHeader', 'true')
    tk.setOption('noFooter', 'true')
    # Calculate optimal size of score window based on number of voices
    tk.setOption('pageHeight', '1152')
    tk.setOption('adjustPageHeight', 'true')
    tk.setOption('spacingSystem', '12')
    tk.setOption('spacingDurDetection', 'true')
    tk.setOption('pageWidth', '2048')

    tk.loadData(cited_mei)
    tk.setScale(35)

    # If a page number has not been explicitly given, make it the first
    # page that has a highlighted element.
    if explicit_page_number:
        # print(repr(explicit_page_number))
        page_number = explicit_page_number
    else:
        if highlight_list:
            page_number = tk.getPageWithElement(highlight_list[0])
        else:
            page_number = 1

    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xml', 'http://www.w3.org/XML/1998/namespace')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    rendered_svg_xml = ET.fromstring(tk.renderToSVG(page_number))

    for id in highlight_list:
        element = rendered_svg_xml.find(".//*[@id='{0}']".format(id))
        if element:
            if 'class' in element.attrib:
                element.set('class', element.attrib['class'] + ' cw-highlighted')
            else:
                element.set('class', ' cw-highlighted')

    svg = ET.tostring(rendered_svg_xml).decode()
    # print('Saving cache for ' + repr(cache_values_to_string(observation_id, explicit_page_number)))
    # caches['observations'].set(
    #         cache_values_to_string(observation_id, explicit_page_number),
    #         (svg, page_number),
    #         None,
    #     )
    return (svg, page_number)


def generate_observation_data(request, prefix=''):
    def post_data(v):
        field = request.POST.get(prefix + '_' + v)
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
        page_number_string = renderer_context['request'].GET.get('p')
        explicit_page_number = eval(page_number_string) if page_number_string else None

        # Load the svg and page number from cache based on observation id
        # and explicit page number
        # print(repr(cache_values_to_string(data['id'], explicit_page_number)))
        cached_data = caches['observations'].get(cache_values_to_string(data['id'], explicit_page_number))
        if cached_data:
            # print('We have a cache for <{}> page {}'.format(data['id'], explicit_page_number))
            (data['svg'], data['page_number']) = cached_data

        # If it wasn't in cache, then render the MEI
        else:
            # print('NO CACHE for <{}> page {}'.format(data['id'], explicit_page_number))
            (data['svg'], data['page_number']) = render_observation(
                    data['id'],
                    data['piece']['piece_id'],
                    data['ema'],
                    explicit_page_number,
                )

        template_names = ['observation/observation_old_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)

class ObservationDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        page_number_string = renderer_context['request'].GET.get('p')
        explicit_page_number = eval(page_number_string) if page_number_string else None

        # Load the svg and page number from cache based on observation id
        # and explicit page number
        # print(repr(cache_values_to_string(data['id'], explicit_page_number)))
        cached_data = caches['observations'].get(cache_values_to_string(data['id'], explicit_page_number))
        if cached_data:
            # print('We have a cache for <{}> page {}'.format(data['id'], explicit_page_number))
            (data['svg'], data['page_number']) = cached_data

        # If it wasn't in cache, then render the MEI
        else:
            # print('NO CACHE for <{}> page {}'.format(data['id'], explicit_page_number))
            (data['svg'], data['page_number']) = render_observation(
                    data['id'],
                    data['piece']['piece_id'],
                    data['ema'],
                    explicit_page_number,
                )

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
