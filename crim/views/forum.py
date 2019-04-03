import html

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ForumPostForm
from ..models.forum import ForumComment, ForumPost
from ..models.user import CRIMUserProfile


@login_required
def create_post(request):
    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            crim_user = CRIMUserProfile.objects.get(user=request.user)
            post = ForumPost.objects.create(
                title=form.cleaned_data["title"],
                text=form.cleaned_data["body"],
                user=crim_user,
            )
            return redirect("view_forum_post", post.pk)
    else:
        form = ForumPostForm()

    return render(request, "forum/create_post.html", {"form": form})


@login_required
def create_comment(request, post_pk):
    if request.method == "POST":
        create_or_reply_comment(post_pk, None, request)
        return redirect("view_forum_post", post_pk)
    else:
        return redirect("view_forum_post", post_pk)


@login_required
def reply_comment(request, pk):
    parent = ForumComment.objects.get(pk=pk)
    if request.method == "POST":
        create_or_reply_comment(parent.pk, pk, request)
        return redirect(parent.get_absolute_url())
    else:
        return render(request, "forum/create_comment.html", {"parent": parent})


def create_or_reply_comment(post_pk, comment_pk, request):
    if comment_pk is not None:
        parent = ForumComment.objects.get(pk=comment_pk)
    else:
        parent = None
    post = ForumPost.objects.get(pk=post_pk)
    crim_user = CRIMUserProfile.objects.get(user=request.user)
    ForumComment.objects.create(
        text=request.POST["body"], parent=parent, post=post, user=crim_user,
    )


def view_post(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    comment_tree = render_comment_tree(post.forumcomment_set.filter(parent=None))
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
    user = html.escape(str(comment.user)) if comment.user else "[deleted]"
    text = html.escape(comment.text)
    base = "<li><h2>{} at {}</h2><p>{}</p></li>".format(
        user, comment.created_at, text
    )
    return base + render_comment_tree(comment.forumcomment_set.all())
