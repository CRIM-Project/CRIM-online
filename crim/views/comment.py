from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from rest_framework import generics, permissions, status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from crim.models.piece import CRIMPiece
from crim.renderers.custom_html_renderer import CustomHTMLRenderer
from crim.serializers.comment import CRIMCommentListSerializer, CRIMCommentDetailSerializer, CRIMCommentDetailDataSerializer
from crim.models.comment import CRIMComment

import datetime


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


class CommentDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'comment/comment_detail.html'

    def get(self, request, comment_id):
        comment = get_object_or_404(CRIMComment, comment_id=comment_id)
        serialized = CRIMCommentDetailSerializer(comment, context={'request': request})
        pieces = CRIMPiece.objects.all().order_by('piece_id')
        return Response({'serialized': serialized, 'comment': comment, 'pieces': pieces})

    def post(self, request, comment_id):
        comment = get_object_or_404(CRIMComment, comment_id=comment_id)
        if not request.user.is_anonymous and (comment.author == request.user.profile or request.user.is_staff):
            # If the "Confirm deletion" checkbox is selected and the Delete
            # button is pressed, then wipe out the text of the comment with [delete]
            # and set `alive` to False.
            if 'confirm-delete' in request.data and 'delete' in request.data:
                deleted_comment = request.data.copy()
                deleted_comment['text'] = '_[deleted]_'
                deleted_comment['alive'] = False
                serialized = CRIMCommentDetailSerializer(comment, data=deleted_comment, context={'request': request})
                if not serialized.is_valid():
                    return Response({'serializer': serializer, 'content': comment})
                serialized.save()
                return redirect('crimcomment-list')
            else:
                if 'save' in request.data and comment.alive:
                    serialized = CRIMCommentDetailSerializer(comment, data=request.data, context={'request': request})
                    if not serialized.is_valid():
                        return Response({'serialized': serialized, 'content': comment})
                    serialized.save()
                return HttpResponseRedirect(request.path_info)
        else:
            return HttpResponseRedirect(request.path_info)


class CommentListData(CommentList):
    renderer_classes = (JSONRenderer,)


class CommentDetailData(CommentDetail):
    renderer_classes = (JSONRenderer,)

    def get(self, request, comment_id):
        comment = get_object_or_404(CRIMComment, comment_id=comment_id)
        serialized = CRIMCommentDetailDataSerializer(comment, context={'request': request})
        return Response(serialized.data)

    def post(self, request):
        comment = get_object_or_404(CRIMComment, comment_id=comment_id)
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif (comment.author != request.user.profile and not request.user.is_staff) or not comment.alive:
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            serialized = CRIMCommentDetailDataSerializer(comment, data=request.data, context={'request': request})
            if not serialized.is_valid():
                return Response({'serialized': serialized, 'content': comment})
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)


class CommentCreateData(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            comment = CRIMComment(author = request.user.profile)
            serialized = CRIMCommentDetailDataSerializer(comment, data=request.data, context={'request': request})
            if not serialized.is_valid():
                return Response({'serialized': serialized, 'content': comment})
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
