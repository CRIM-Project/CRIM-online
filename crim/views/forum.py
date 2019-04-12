import html

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..models.forum import CRIMForumComment, CRIMForumPost
from ..models.user import CRIMUserProfile


@login_required
def create_post(request):
    if request.method == "POST":
        crim_user = CRIMUserProfile.objects.get(user=request.user)
        post = CRIMForumPost.objects.create(
            title=request.POST["title"].strip(),
            text=request.POST["body"].strip(),
            user=crim_user,
        )
        return redirect("view_forum_post", post.pk)
    else:
        return render(request, "forum/create_post.html")


@login_required
def create_comment(request, post_pk):
    if request.method == "POST":
        create_or_reply_comment(post_pk, None, request)
        return redirect("view_forum_post", post_pk)
    else:
        return redirect("view_forum_post", post_pk)


@login_required
def reply_comment(request, pk):
    parent = CRIMForumComment.objects.get(pk=pk)
    if request.method == "POST":
        create_or_reply_comment(parent.post.pk, pk, request)
        return redirect(parent.get_absolute_url())
    else:
        return render(request, "forum/reply_comment.html", {"parent": parent})


def create_or_reply_comment(post_pk, comment_pk, request):
    if comment_pk is not None:
        parent = CRIMForumComment.objects.get(pk=comment_pk)
    else:
        parent = None
    post = CRIMForumPost.objects.get(pk=post_pk)
    crim_user = CRIMUserProfile.objects.get(user=request.user)
    CRIMForumComment.objects.create(
        text=request.POST["body"].strip(), parent=parent, post=post, user=crim_user,
    )


def view_post(request, pk):
    post = get_object_or_404(CRIMForumPost, pk=pk)
    comment_tree = render_comment_tree(post.crimforumcomment_set.filter(parent=None))
    context = {"comment_tree": comment_tree, "post": post}
    return render(request, "forum/view_post.html", context)


def render_comment_tree(comment_set):
    comment_html = ""
    for comment in comment_set:
        comment_html += render_comment(comment)

    if comment_html:
        return "<ul>" + comment_html + "</ul>"
    else:
        return ""


def render_comment(comment):
    # VERY IMPORTANT: escape any non-literal text that may contain HTML!
    if comment.user:
        user = comment.user.name + " (" + comment.user.user.username + ")"
    else:
        user = "[deleted]"
    user = html.escape(user)

    text = html.escape(comment.text)
    base = "<li><h2>{} at {}</h2><p>{}</p><p><a href=\"{}\">reply</a></p></li>".format(
        user,
        comment.created_at.strftime("%I:%M %p on %B %d, %Y"),
        text,
        reverse("reply_forum_comment", args=[comment.pk]),
    )
    return base + render_comment_tree(comment.crimforumcomment_set.all())
