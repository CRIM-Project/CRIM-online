from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.relationship import CRIMRelationshipSerializer
from crim.models.relationship import CRIMRelationship


class RelationshipSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the relationship_list.html template!
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 30


class RelationshipListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Add name of relationship type
        for r in data['results']:
            # Save string for model musical type
            if r['model_observation']['mt_cf']:
                model_observation = 'Cantus firmus'
            elif r['model_observation']['mt_sog']:
                model_observation = 'Soggetto'
            elif r['model_observation']['mt_csog']:
                model_observation = 'Counter-soggetto'
            elif r['model_observation']['mt_cd']:
                model_observation = 'Contrapuntal duo'
            elif r['model_observation']['mt_fg']:
                model_observation = 'Fuga'
            elif r['model_observation']['mt_pe']:
                model_observation = 'Periodic entry'
            elif r['model_observation']['mt_id']:
                model_observation = 'Imitative duo'
            elif r['model_observation']['mt_nid']:
                model_observation = 'Non-imitative duo'
            elif r['model_observation']['mt_hr']:
                model_observation = 'Homorhythm'
            elif r['model_observation']['mt_cad']:
                model_observation = 'Cadence'
            elif r['model_observation']['mt_int']:
                model_observation = 'Interval patterns'
            elif r['model_observation']['mt_fp']:
                model_observation = 'Form and process'
            else:
                model_observation = ''
            # Likewise for derivative musical type
            if r['derivative_observation']['mt_cf']:
                derivative_observation = 'Cantus firmus'
            elif r['derivative_observation']['mt_sog']:
                derivative_observation = 'Soggetto'
            elif r['derivative_observation']['mt_csog']:
                derivative_observation = 'Counter-soggetto'
            elif r['derivative_observation']['mt_cd']:
                derivative_observation = 'Contrapuntal duo'
            elif r['derivative_observation']['mt_fg']:
                derivative_observation = 'Fuga'
            elif r['derivative_observation']['mt_pe']:
                derivative_observation = 'Periodic entry'
            elif r['derivative_observation']['mt_id']:
                derivative_observation = 'Imitative duo'
            elif r['derivative_observation']['mt_nid']:
                derivative_observation = 'Non-imitative duo'
            elif r['derivative_observation']['mt_hr']:
                derivative_observation = 'Homorhythm'
            elif r['derivative_observation']['mt_cad']:
                derivative_observation = 'Cadence'
            elif r['derivative_observation']['mt_int']:
                derivative_observation = 'Interval patterns'
            elif r['derivative_observation']['mt_fp']:
                derivative_observation = 'Form and process'
            else:
                derivative_observation = ''
            # If they're the same, use just the one;
            # otherwise use whichever has one if one doesn't (e.g. omission),
            # or include them both.
            if not model_observation and not derivative_observation:
                r['musical_type'] = '-'
            elif model_observation:
                r['musical_type'] = model_observation
            elif derivative_observation:
                r['musical_type'] = derivative_observation
            else:
                r['musical_type'] = (
                    model_observation +
                    ', ' +
                    derivative_observation
                )

        template_names = ['relationship/relationship_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class RelationshipDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['relationship/relationship_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
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
        return CRIMRelationship.objects.all().order_by(order_by)


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
        url_arg = self.kwargs['pk']
        relationship = CRIMRelationship.objects.filter(pk=url_arg)
        obj = get_object_or_404(relationship)
        self.check_object_permissions(self.request, obj)
        return obj


class RelationshipListData(RelationshipList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


class RelationshipDetailData(RelationshipDetail):
    renderer_classes = (JSONRenderer,)
