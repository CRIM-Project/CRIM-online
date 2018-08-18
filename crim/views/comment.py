from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions

from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.comment import CRIMCommentSerializer
from crim.models.comment import CRIMComment


class CommentListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['comment/comment_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class CommentDetailHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['comment/comment_detail.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data}, renderer_context)
        return template.render(context)


class CommentList(generics.ListAPIView):
    model = CRIMComment
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMCommentSerializer
    renderer_classes = (
        CommentListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', '-created')
        return CRIMComment.objects.order_by(order_by)


class CommentDetail(generics.RetrieveAPIView):
    model = CRIMComment
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMCommentSerializer
    renderer_classes = (
        CommentDetailHTMLRenderer,
        JSONRenderer,
    )
    queryset = CRIMComment.objects.all()

    def get_object(self):
        url_arg = self.kwargs['comment_id']
        comment = CRIMComment.objects.filter(comment_id=url_arg)
        if not comment.exists():
            comment = CRIMComment.objects.filter(name__iexact=url_arg)

        obj = get_object_or_404(comment)
        self.check_object_permissions(self.request, obj)
        return obj


class CommentListData(CommentList):
    renderer_classes = (JSONRenderer,)


class CommentDetailData(CommentDetail):
    renderer_classes = (JSONRenderer,)
