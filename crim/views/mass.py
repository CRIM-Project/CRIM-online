from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.models.mass import CRIMMass
from crim.serializers.mass import CRIMMassListSerializer, CRIMMassDetailSerializer


class MassListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        for mass in data:
            if mass['min_number_of_voices'] == mass['max_number_of_voices'] or not mass['min_number_of_voices']:
                mass['total_voice_count'] = mass['max_number_of_voices']
            else:
                mass['total_voice_count'] = '{0}-{1}'.format(
                        mass['min_number_of_voices'], mass['max_number_of_voices'])
        template_names = ['mass/mass_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class MassDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Sort roles alphabetically by role type
        try:
            data['roles'] = sorted(data['roles'],
                                   key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')
        except KeyError:
            pass

        template_names = ['mass/mass_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class MassList(generics.ListAPIView):
    model = CRIMMass
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMMassListSerializer
    renderer_classes = (
        MassListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'mass_id')
        return CRIMMass.objects.all().order_by(order_by).select_related('composer')


class MassDetail(generics.RetrieveAPIView):
    model = CRIMMass
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMMassDetailSerializer
    renderer_classes = (
        MassDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMMass.objects.all()

    def get_object(self):
        url_arg = self.kwargs['mass_id']
        mass = CRIMMass.objects.filter(mass_id=url_arg)
        if not mass.exists():
            mass = CRIMMass.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(mass)
        self.check_object_permissions(self.request, obj)
        return obj


class MassListData(MassList):
    renderer_classes = (JSONRenderer,)


class MassDetailData(MassDetail):
    renderer_classes = (JSONRenderer,)
