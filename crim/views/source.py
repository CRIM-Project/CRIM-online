from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.source import CRIMSourceListSerializer, CRIMSourceDetailSerializer
from crim.models.document import CRIMSource

AUTHOR = 'Author'
COMPOSER = 'Composer'


class SourceListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        for document in data:
            # Put links into a list rather than a \n-separated string
            document['external_links'] = document['external_links'].split('\n')
            # - Add `author` field to content: only look at roles with
            # the role type with name "Composer", and add all such names
            # to the list, along with the url of the author
            # - Add `date` field to content: again, only look at roles
            # with the role type "Composer"
            authors = []
            dates = []
            for role in document['roles']:
                if role['role_type'] and role['role_type']['name'] == AUTHOR:
                    author_html = ('<a href="' + role['person']['url'] +
                                   '">' + role['person']['name'] + '</a>')
                    authors.append(author_html)
                    if role['date']:
                        dates.append(role['date'])
            document['authors_with_url'] = '; '.join(authors) if authors else '-'
            # Only add one author's date for clarity. Not the best sorting
            # method (since '1600' will be sorted before 'c. 1550'),
            # but it does the job here.
            document['date'] = min(dates) if dates else '-'

        template_names = ['source/source_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class SourceDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Put links into a list rather than a \n-separated string
        data['external_links'] = data['external_links'].split('\n')
        # See SourceListHTMLRenderer for comments on getting author/composer
        # names and dates
        for item in (data['piece_contents'] + data['mass_contents'] +
                     data['treatise_contents'] + data['source_contents']):
            creators = []
            dates = []
            for role in item['roles']:
                if role['role_type'] and role['role_type']['name'] in [COMPOSER, AUTHOR]:
                    creator_html = ('<a href="' + role['person']['url'] +
                                    '">' + role['person']['name'] + '</a>')
                    creators.append(creator_html)
                    if role['date']:
                        dates.append(role['date'])
            item['creators_with_url'] = '; '.join(creators) if creators else '-'
            item['date'] = min(dates) if dates else '-'

        # Sort roles alphabetically by role type
        data['roles'] = sorted(data['roles'],
                               key=lambda x: x['role_type']['name'] if x['role_type'] else 'Z')

        template_names = ['source/source_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class SourceList(generics.ListAPIView):
    model = CRIMSource
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMSourceListSerializer
    renderer_classes = (
        SourceListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', 'document_id')
        return CRIMSource.objects.all().order_by(order_by)


class SourceDetail(generics.RetrieveAPIView):
    model = CRIMSource
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMSourceDetailSerializer
    renderer_classes = (
        SourceDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMSource.objects.all()

    def get_object(self):
        url_arg = self.kwargs['document_id']
        document = CRIMSource.objects.filter(document_id=url_arg)
        if not document.exists():
            document = CRIMSource.objects.filter(name_sort__iexact=url_arg)

        obj = get_object_or_404(document)
        self.check_object_permissions(self.request, obj)
        return obj
