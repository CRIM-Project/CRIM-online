from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

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


class CommentDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'comment/comment_detail.html'

    def get(self, request, comment_id):
        comment = get_object_or_404(CRIMComment, comment_id=comment_id)
        serializer = CRIMCommentSerializer(comment, context={'request': request})
        return Response({'serializer': serializer, 'content': comment})

    def post(self, request, comment_id):
        comment = get_object_or_404(CRIMComment, comment_id=comment_id)
        serializer = CRIMCommentSerializer(comment, data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'content': comment})
        serializer.save()
        return redirect('crimcomment-list')


class CommentListData(CommentList):
    renderer_classes = (JSONRenderer,)


class CommentDetailData(CommentDetail):
    renderer_classes = (JSONRenderer,)
