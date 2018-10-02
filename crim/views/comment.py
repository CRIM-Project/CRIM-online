from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import permissions

from crim.models.piece import CRIMPiece
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.comment import CRIMCommentListSerializer, CRIMCommentDetailSerializer
from crim.models.comment import CRIMComment


class CommentListHTMLRenderer(CustomHTMLRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        template_names = ['comment/comment_list.html']
        template = self.resolve_template(template_names)
        context = self.get_template_context({'content': data, 'request': renderer_context['request']}, renderer_context)
        return template.render(context)


class CommentList(generics.ListAPIView):
    model = CRIMComment
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CRIMCommentListSerializer
    renderer_classes = (
        CommentListHTMLRenderer,
        JSONRenderer,
    )

    def get_queryset(self):
        order_by = self.request.GET.get('order_by', '-created')
        return CRIMComment.objects.filter(alive=True).order_by(order_by)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = (
        TemplateHTMLRenderer,
        JSONRenderer,
    )
    template_name = 'comment/comment_detail.html'

    def get(self, request, comment_id):
        comment = get_object_or_404(CRIMComment, comment_id=comment_id)
        serializer = CRIMCommentDetailSerializer(comment, context={'request': request})
        pieces = CRIMPiece.objects.all().order_by('piece_id')
        return Response({'serializer': serializer, 'content': comment, 'pieces': pieces})

    def post(self, request, comment_id):
        comment = get_object_or_404(CRIMComment, comment_id=comment_id)
        if not request.user.is_anonymous and comment.author == request.user.profile:
            # If the "Confirm deletion" checkbox is selected and the Delete
            # button is pressed, then wipe out the text of the comment with [delete]
            # and set `alive` to False.
            if 'confirm-delete' in request.data and 'delete' in request.data:
                deleted_comment = request.data.copy()
                deleted_comment['text'] = '_[deleted]_'
                deleted_comment['alive'] = False
                serializer = CRIMCommentDetailSerializer(comment, data=deleted_comment, context={'request': request})
                if not serializer.is_valid():
                    return Response({'serializer': serializer, 'content': comment})
                serializer.save()
                return redirect('crimcomment-list')
            elif 'save' in request.data and comment.alive:
                serializer = CRIMCommentDetailSerializer(comment, data=request.data, context={'request': request})
                if not serializer.is_valid():
                    return Response({'serializer': serializer, 'content': comment})
                serializer.save()
                return HttpResponseRedirect(request.path_info)
            else:
                return HttpResponseRedirect(request.path_info)

    def delete(self, request, comment_id):
        comment = get_object_or_404(CRIMComment, comment_id=comment_id)
        if not request.user.is_anonymous and comment.author == request.user.profile:
            comment.delete()
        return redirect('crimcomment-list')


class CommentListData(CommentList):
    renderer_classes = (JSONRenderer,)


class CommentDetailData(CommentDetail):
    renderer_classes = (JSONRenderer,)
