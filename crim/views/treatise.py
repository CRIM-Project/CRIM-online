from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.treatise import CRIMTreatiseListSerializer, CRIMTreatiseDetailSerializer
from crim.models.document import CRIMTreatise


class TreatiseListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['treatise/treatise_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class TreatiseDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Sort roles alphabetically by role type
        try:
            data['roles'] = sorted(data['roles'],
                                   key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')
        except KeyError:
            pass

        template_names = ['treatise/treatise_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class TreatiseList(generics.ListAPIView):
    model = CRIMTreatise
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMTreatiseListSerializer
    renderer_classes = (
        TreatiseListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'document_id')
        return CRIMTreatise.objects.all().order_by(order_by).select_related(
            'author',
        )


class TreatiseDetail(generics.RetrieveAPIView):
    model = CRIMTreatise
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMTreatiseDetailSerializer
    renderer_classes = (
        TreatiseDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMTreatise.objects.all()

    def get_object(self):
        url_arg = self.kwargs['document_id']
        document = CRIMTreatise.objects.filter(document_id=url_arg)
        if not document.exists():
            document = CRIMTreatise.objects.filter(title__iexact=url_arg)

        obj = get_object_or_404(document)
        self.check_object_permissions(self.request, obj)
        return obj


class TreatiseListData(TreatiseList):
    renderer_classes = (JSONRenderer,)


class TreatiseDetailData(TreatiseDetail):
    renderer_classes = (JSONRenderer,)
