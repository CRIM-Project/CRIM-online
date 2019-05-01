import html
import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..models.forum import CRIMForumComment, CRIMForumPost
from ..models.piece import CRIMPiece
from ..models.user import CRIMUserProfile


def index(request):
    posts = CRIMForumPost.objects.all().order_by("-created_at")
    context = {"posts": posts}
    return render(request, "forum/index.html", context)


def related(request, piece):
    piece = get_object_or_404(CRIMPiece, piece_id=piece)
    related = []
    for post in CRIMForumPost.objects.all():
        if piece.piece_id in post.text or piece.piece_id in post.title:
            related.append(post)
    context = {"piece": piece, "posts": related}
    return render(request, "forum/related.html", context)


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
    # VERY IMPORTANT: escape any non-literal text that may contain HTML!
    post_title = insert_links(html.escape(post.title))
    post_text = insert_links(html.escape(post.text))
    comment_tree = render_comment_tree(post.crimforumcomment_set.filter(parent=None))
    context = {
        "comment_tree": comment_tree,
        "post": post,
        "post_title": post_title,
        "post_text": post_text,
    }
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
    if comment.user:
        user = comment.user.name + " (" + comment.user.user.username + ")"
    else:
        user = "[deleted]"
    # VERY IMPORTANT: escape any non-literal text that may contain HTML!
    user = html.escape(user)

    text = html.escape(comment.text)
    text = insert_links(text)
    base = "<li><h2>{} at {}</h2><p>{}</p><p><a href=\"{}\">reply</a></p></li>".format(
        user,
        comment.created_at.strftime("%I:%M %p on %B %d, %Y"),
        text,
        reverse("reply_forum_comment", args=[comment.pk]),
    )
    return base + render_comment_tree(comment.crimforumcomment_set.all())


_link_regex = re.compile(r"CRIM_Model_[0-9]{4}", re.IGNORECASE)
def insert_links(text):
    """Detect occurrences of piece IDs in the text, and insert HTML links."""
    return _link_regex.sub(lambda m: create_link(m.group(0)), text)


def create_link(piece_id):
    """Given a piece ID, return an HTML link."""
    normalized_piece_id = "CRIM_Model_" + piece_id[-4:]
    piece = CRIMPiece.objects.get(piece_id=normalized_piece_id)
    if piece is not None:
        return '<a href="{}">{}</a>'.format(piece.get_absolute_url(), piece_id)
    else:
        return piece_id
