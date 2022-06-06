#from django.core.exceptions import DoesNotExist
from django.db.models import Min
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer

from crim.models.person import CRIMPerson
from crim.models.role import CRIMRoleType
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.person import CRIMPersonListSerializer, CRIMPersonDetailSerializer

ANALYST = 'analyst'


class PersonSetPagination(PageNumberPagination):
    # CAREFUL: the attribute `page_size` MUST match the
    # `rangelist` parameter in the person_list.html template!
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 15


class PersonListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Add `content.filter_role_type` item if there is a url parameter
        # that matches a role type in the database.
        if renderer_context['request'].GET.get('role') and CRIMRoleType.objects.filter(role_type_id=renderer_context['request'].GET.get('role')):
            data['filter_role_type'] = CRIMRoleType.objects.get(role_type_id=renderer_context['request'].GET.get('role'))

        template_names = ['person/person_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class PersonDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        def role_has_work(role):
            return role['mass'] or role['piece'] or role['treatise'] or role['source']
        data['has_works'] = False
        for role in data['roles']:
            if role_has_work(role):
                data['has_works'] = True
                break

        template_names = ['person/person_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class PersonList(generics.ListAPIView):
    model = CRIMPerson
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPersonListSerializer
    pagination_class = PersonSetPagination
    renderer_classes = (
        PersonListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'person_id')
        if self.request.GET.get('role') and CRIMRoleType.objects.filter(role_type_id=self.request.GET.get('role')):
            if self.request.GET.get('role') == ANALYST:
                return CRIMPerson.objects.exclude(observations__isnull=True, relationships__isnull=True).distinct().order_by(order_by)
            else:
                role_type = CRIMRoleType.objects.get(role_type_id=self.request.GET.get('role'))
                return CRIMPerson.objects.filter(roles__role_type=role_type).distinct().order_by(order_by)
        else:
            return CRIMPerson.objects.exclude(person_id='CRIM_Person_0000').distinct().annotate(role=Min('roles__role_type')).order_by(order_by)


class PersonDetail(generics.RetrieveAPIView):
    model = CRIMPerson
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPersonDetailSerializer
    renderer_classes = (
        PersonDetailHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        queryset = CRIMPerson.objects.all()
        order_by = self.request.GET.get('order_by', 'pk')
        queryset.prefetch_related().order_by(order_by)

        return queryset


    def get_object(self):
        url_arg = self.kwargs['person_id']
        person = CRIMPerson.objects.filter(person_id=url_arg)
        if not person.exists():
            person = CRIMPerson.objects.filter(name__iexact=url_arg)

        obj = get_object_or_404(person)
        self.check_object_permissions(self.request, obj)
        return obj


class PersonListData(PersonList):
    pagination_class = None
    renderer_classes = (JSONRenderer,)


class PersonDetailData(PersonDetail):
    renderer_classes = (JSONRenderer,)
