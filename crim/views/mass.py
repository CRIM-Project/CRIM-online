from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.models.mass import CRIMMass
from crim.serializers.mass import CRIMMassListSerializer, CRIMMassDetailSerializer

from crim.common import earliest_date

COMPOSER = 'Composer'


class MassListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        for mass in data:
            # - Add `composer` field to content: only look at roles with
            # the role type with name "Composer", and add all such names
            # to the list, along with the url of the composer
            # - Add `date` field to content: again, only look at roles
            # with the role type "Composer"
            composers = []
            dates = []
            for role in mass['roles']:
                if role['role_type'] and role['role_type']['name'] == COMPOSER:
                    composer_html = ('<a href="' + role['person']['url'].replace('/data/', '/') +
                                     '">' + role['person']['name'] + '</a>')
                    composers.append(composer_html)
                    if role['date']:
                        dates.append(role['date'])
            mass['composers_with_url'] = '; '.join(composers) if composers else '-'
            # Only add one composer's date for clarity, choosing the earliest.
            mass['date'] = earliest_date(dates)

        template_names = ['mass/mass_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class MassDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Sort roles alphabetically by role type
        data['roles'] = sorted(data['roles'],
                               key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')

        template_names = ['mass/mass_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
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
        return CRIMMass.objects.all().order_by(order_by)


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


class MassListData(generics.ListAPIView):
    model = CRIMMass
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMMassListSerializer
    renderer_classes = (
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'mass_id')
        return CRIMMass.objects.all().order_by(order_by)


class MassDetailData(generics.RetrieveAPIView):
    model = CRIMMass
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMMassDetailSerializer
    renderer_classes = (
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
