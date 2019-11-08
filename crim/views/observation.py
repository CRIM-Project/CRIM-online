from django.core.cache import caches
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from crim.common import cache_values_to_string
from crim.omas.localapi import slice_from_file
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.observation import CRIMObservationSerializer
from crim.models.observation import CRIMObservation
from crim.models.piece import CRIMPiece

import os
import re
import verovio
import xml.etree.ElementTree as ET


def render_observation(id, piece_id, ema, explicit_page_number=None):
    observation_cache = caches['observations']

    ET.register_namespace('', 'http://www.music-encoding.org/ns/mei')
    tk = verovio.toolkit()
    raw_mei = open(os.path.join('crim/static/mei', piece_id + '.mei')).read()
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
    observation_cache.set(cache_values_to_string(id, explicit_page_number), (svg, page_number), None)
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

    # Don't allow if more than one musical type has been selected.
    list_of_musical_types = [
        post_data('mt_cf'),
        post_data('mt_sog'),
        post_data('mt_csog'),
        post_data('mt_cd'),
        post_data('mt_fg'),
        post_data('mt_pe'),
        post_data('mt_id'),
        post_data('mt_nid'),
        post_data('mt_hr'),
        post_data('mt_cad'),
        post_data('mt_int'),
        post_data('mt_fp'),
    ]
    if sum(bool(x) for x in list_of_musical_types) > 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    observation_data = {}
    if post_data('piece'):
        observation_data['piece'] = CRIMPiece.objects.get(piece_id=post_data('piece'))
    if post_data('ema'):
        observation_data['ema'] = post_data('ema')

    if post_data('mt_cf'):
        observation_data['mt_cf'] = True
        observation_data['mt_cf_voices'] = post_data('mt_cf_voices') if post_data('mt_cf_voices') else ''
        observation_data['mt_cf_dur'] = True if post_data('mt_cf_dur') else False
        observation_data['mt_cf_mel'] = True if post_data('mt_cf_mel') else False
    elif post_data('mt_sog'):
        observation_data['mt_sog'] = True
        observation_data['mt_sog_voices'] = post_data('mt_sog_voices') if post_data('mt_sog_voices') else ''
        observation_data['mt_sog_dur'] = True if post_data('mt_sog_dur') else False
        observation_data['mt_sog_mel'] = True if post_data('mt_sog_mel') else False
        observation_data['mt_sog_ostinato'] = True if post_data('mt_sog_ostinato') else False
        observation_data['mt_sog_periodic'] = True if post_data('mt_sog_periodic') else False
    elif post_data('mt_csog'):
        observation_data['mt_csog'] = True
        observation_data['mt_csog_voices'] = post_data('mt_csog_voices') if post_data('mt_csog_voices') else ''
        observation_data['mt_csog_dur'] = True if post_data('mt_csog_dur') else False
        observation_data['mt_csog_mel'] = True if post_data('mt_csog_mel') else False
    elif post_data('mt_cd'):
        observation_data['mt_cd'] = True
        observation_data['mt_cd_voices'] = post_data('mt_cd_voices') if post_data('mt_cd_voices') else ''
    elif post_data('mt_fg'):
        observation_data['mt_fg'] = True
        observation_data['mt_fg_voices'] = post_data('mt_fg_voices') if post_data('mt_fg_voices') else ''
        observation_data['mt_fg_int'] = post_data('mt_fg_int') if post_data('mt_fg_int') else ''
        observation_data['mt_fg_tint'] = post_data('mt_fg_tint') if post_data('mt_fg_tint') else ''
        observation_data['mt_fg_periodic'] = True if post_data('mt_fg_periodic') else False
        observation_data['mt_fg_strict'] = True if post_data('mt_fg_strict') else False
        observation_data['mt_fg_flexed'] = True if post_data('mt_fg_flexed') else False
        observation_data['mt_fg_sequential'] = True if post_data('mt_fg_sequential') else False
        observation_data['mt_fg_inverted'] = True if post_data('mt_fg_inverted') else False
        observation_data['mt_fg_retrograde'] = True if post_data('mt_fg_retrograde') else False
    elif post_data('mt_pe'):
        observation_data['mt_pe'] = True
        observation_data['mt_pe_voices'] = post_data('mt_pe_voices') if post_data('mt_pe_voices') else ''
        observation_data['mt_pe_int'] = post_data('mt_pe_int') if post_data('mt_pe_int') else ''
        observation_data['mt_pe_tint'] = post_data('mt_pe_tint') if post_data('mt_pe_tint') else ''
        observation_data['mt_pe_strict'] = True if post_data('mt_pe_strict') else False
        observation_data['mt_pe_flexed'] = True if post_data('mt_pe_flexed') else False
        observation_data['mt_pe_flt'] = True if post_data('mt_pe_flt') else False
        observation_data['mt_pe_sequential'] = True if post_data('mt_pe_sequential') else False
        observation_data['mt_pe_added'] = True if post_data('mt_pe_added') else False
        observation_data['mt_pe_invertible'] = True if post_data('mt_pe_invertible') else False
    elif post_data('mt_id'):
        observation_data['mt_id'] = True
        observation_data['mt_id_voices'] = post_data('mt_id_voices') if post_data('mt_id_voices') else ''
        observation_data['mt_id_int'] = post_data('mt_id_int') if post_data('mt_id_int') else ''
        observation_data['mt_id_tint'] = post_data('mt_id_tint') if post_data('mt_id_tint') else ''
        observation_data['mt_id_strict'] = True if post_data('mt_id_strict') else False
        observation_data['mt_id_flexed'] = True if post_data('mt_id_flexed') else False
        observation_data['mt_id_flt'] = True if post_data('mt_id_flt') else False
        observation_data['mt_id_invertible'] = True if post_data('mt_id_invertible') else False
    elif post_data('mt_nid'):
        observation_data['mt_nid'] = True
        observation_data['mt_nid_voices'] = post_data('mt_nid_voices') if post_data('mt_nid_voices') else ''
        observation_data['mt_nid_int'] = post_data('mt_nid_int') if post_data('mt_nid_int') else ''
        observation_data['mt_nid_tint'] = post_data('mt_nid_tint') if post_data('mt_nid_tint') else ''
        observation_data['mt_nid_strict'] = True if post_data('mt_nid_strict') else False
        observation_data['mt_nid_flexed'] = True if post_data('mt_nid_flexed') else False
        observation_data['mt_nid_flt'] = True if post_data('mt_nid_flt') else False
        observation_data['mt_nid_sequential'] = True if post_data('mt_nid_sequential') else False
        observation_data['mt_nid_invertible'] = True if post_data('mt_nid_invertible') else False
    elif post_data('mt_hr'):
        observation_data['mt_hr'] = True
        observation_data['mt_hr_voices'] = post_data('mt_hr_voices') if post_data('mt_hr_voices') else ''
        observation_data['mt_hr_simple'] = True if post_data('mt_hr_simple') else False
        observation_data['mt_hr_staggered'] = True if post_data('mt_hr_staggered') else False
        observation_data['mt_hr_sequential'] = True if post_data('mt_hr_sequential') else False
        observation_data['mt_hr_fauxbourdon'] = True if post_data('mt_hr_fauxbourdon') else False
    elif post_data('mt_cad'):
        observation_data['mt_cad'] = True
        observation_data['mt_cad_cantizans'] = post_data('mt_cad_cantizans') if post_data('mt_cad_cantizans') else ''
        observation_data['mt_cad_tenorizans'] = post_data('mt_cad_tenorizans') if post_data('mt_cad_tenorizans') else ''
        observation_data['mt_cad_type'] = post_data('mt_cad_type') if post_data('mt_cad_type') else ''
        observation_data['mt_cad_tone'] = post_data('mt_cad_tone') if post_data('mt_cad_tone') else ''
        observation_data['mt_cad_dtv'] = post_data('mt_cad_dtv') if post_data('mt_cad_dtv') else ''
        observation_data['mt_cad_dti'] = post_data('mt_cad_dti') if post_data('mt_cad_dti') else ''
    elif post_data('mt_int'):
        observation_data['mt_int'] = True
        observation_data['mt_int_voices'] = post_data('mt_int_voices') if post_data('mt_int_voices') else ''
        observation_data['mt_int_p6'] = True if post_data('mt_int_p6') else False
        observation_data['mt_int_p3'] = True if post_data('mt_int_p3') else False
        observation_data['mt_int_c35'] = True if post_data('mt_int_c35') else False
        observation_data['mt_int_c83'] = True if post_data('mt_int_c83') else False
        observation_data['mt_int_c65'] = True if post_data('mt_int_c65') else False
    elif post_data('mt_fp'):
        observation_data['mt_fp'] = True
        observation_data['mt_fp_ir'] = True if post_data('mt_fp_ir') else False
        observation_data['mt_fp_range'] = post_data('mt_fp_range') if post_data('mt_fp_range') else ''
        observation_data['mt_fp_comment'] = post_data('mt_fp_comment') if post_data('mt_fp_comment') else ''

    if post_data('remarks'):
        observation_data['remarks'] = post_data('remarks')

    return observation_data


def create_observation_from_request(request, prefix=''):
    observation_data = generate_observation_data(request, prefix)
    observation_data['observer'] = request.user.profile.person
    new_observation = CRIMObservation(**observation_data)
    return new_observation


class ObservationSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the observation_list.html template!
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 150


class ObservationListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['observation/observation_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class ObservationDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        page_number_string = renderer_context['request'].GET.get('p')
        explicit_page_number = eval(page_number_string) if page_number_string else ''
        observation_cache = caches['observations']

        # Load the svg and page number from cache based on observation id
        # and explicit page number
        cached_data = observation_cache.get(cache_values_to_string(data['id'], explicit_page_number))
        if cached_data:
            (data['svg'], data['page_number']) = cached_data

        # If it wasn't in cache, then render the MEI
        else:
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
        order_by = self.request.GET.get('order_by', 'pk')
        if self.request.user.is_authenticated:
            return CRIMObservation.objects.all().order_by(order_by)
        else:
            return CRIMObservation.objects.filter(curated=True).order_by(order_by)


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
        url_arg = self.kwargs['id']
        observation = CRIMObservation.objects.filter(id=url_arg)
        obj = get_object_or_404(observation)
        self.check_object_permissions(self.request, obj)
        return obj


class ObservationListData(ObservationList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


class ObservationDetailData(generics.RetrieveUpdateAPIView):
    model = CRIMObservation
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMObservationSerializer
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

            serialized = CRIMObservationSerializer(instance, data=request.data, context={'request': request})
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
        serialized = CRIMObservationSerializer(observation, data=request.data, context={'request': request})
        # If the user is an admin, the observation should be marked as curated.
        if serialized.is_valid():
            if request.user.is_staff:
                serialized.validated_data['curated'] = True
        else:
            return Response({'serialized': serialized, 'content': observation})

        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
