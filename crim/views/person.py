from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from django.contrib.auth.models import User
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.person import CRIMPersonListSerializer, CRIMPersonDetailSerializer
from crim.models.person import CRIMPerson
from rest_framework.response import Response
from rest_framework import status


class PersonListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        for p in data:
            # Put roles into a single text field
            if p['unique_roles']:
                p['unique_roles'] = ', '.join(p['unique_roles'])
            else:
                p['unique_roles'] = ''
            # Could add work count to table
            # p['work_count'] = len(p['roles'])

        template_names = ['person/person_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
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
        # Put roles into a single text field
        data['unique_roles'] = ', '.join(data['unique_roles'])

        template_names = ['person/person_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class PersonList(generics.ListAPIView):
    model = CRIMPerson
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPersonListSerializer
    renderer_classes = (
        PersonListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'person_id')
        return CRIMPerson.objects.all().order_by(order_by)


class PersonDetail(generics.RetrieveAPIView):
    model = CRIMPerson
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPersonDetailSerializer
    renderer_classes = (
        PersonDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMPerson.objects.all()

    def get_object(self):
        url_arg = self.kwargs['person_id']
        person = CRIMPerson.objects.filter(person_id=url_arg)
        if not person.exists():
            person = CRIMPerson.objects.filter(name_sort__iexact=url_arg)

        obj = get_object_or_404(person)
        self.check_object_permissions(self.request, obj)
        return obj


class PersonListData(generics.ListAPIView):
    model = CRIMPerson
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPersonListSerializer
    renderer_classes = (
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'person_id')
        return CRIMPerson.objects.all().order_by(order_by)


class PersonDetailData(generics.RetrieveAPIView):
    model = CRIMPerson
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMPersonDetailSerializer
    renderer_classes = (
        JSONRenderer,
    )
    queryset = CRIMPerson.objects.all()

    def get_object(self):
        url_arg = self.kwargs['person_id']
        person = CRIMPerson.objects.filter(person_id=url_arg)
        if not person.exists():
            person = CRIMPerson.objects.filter(name_sort__iexact=url_arg)

        obj = get_object_or_404(person)
        self.check_object_permissions(self.request, obj)
        return obj
