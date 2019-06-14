import html
import re

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..models.forum import CRIMForumPost
from ..models.piece import CRIMPiece
from ..models.user import CRIMUserProfile


def index(request):
    posts = CRIMForumPost.objects.all().order_by("-created_at")
    context = {"posts": posts}
    return render(request, "forum/post_list.html", context)


def related(request, piece):
    piece = get_object_or_404(CRIMPiece, piece_id=piece)
    pid = piece.piece_id.lower()

    # Fetch all posts which mention the piece in the title or body.
    related = CRIMForumPost.objects.filter(
        Q(text__icontains=pid) | Q(title__icontains=pid)
    )
    context = {"piece": piece, "posts": related}
    return render(request, "forum/related.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        crim_user = CRIMUserProfile.objects.get(user=request.user)
        post = CRIMForumPost.objects.create(
            title=request.POST["title"].strip(),
            text=request.POST["body"].strip(),
            author=crim_user,
        )
        return redirect("forum-view-post", post.post_id)
    else:
        return render(request, "forum/create_post.html")


@login_required
def create_reply(request, parent_id):
    if request.method == "POST":
        parent = CRIMForumPost.objects.get(post_id=parent_id)
        head = parent.head
        crim_user = CRIMUserProfile.objects.get(user=request.user)
        CRIMForumPost.objects.create(
            text=request.POST["body"].strip(),
            parent=parent,
            head=head,
            author=crim_user,
        )
    return redirect("forum-view-post", parent_id)


def view_post(request, post_id):
    post = get_object_or_404(CRIMForumPost, post_id=post_id)
    # VERY IMPORTANT: escape any non-literal text that may contain HTML!
    post_title = html.escape(post.title)
    post_text = insert_links(html.escape(post.text))
    comment_tree = render_comment_tree(post.children.all())
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
    if comment.author:
        author = comment.author.name
    else:
        author = "[deleted]"
    # VERY IMPORTANT: escape any non-literal text that may contain HTML!
    author = html.escape(author)

    text = html.escape(comment.text)
    text = insert_links(text)
    base = "<li><h2>{} at {}</h2><p>{}</p><p><a href=\"{}\">reply</a></p></li>".format(
        author,
        comment.created_at.strftime("%Y-%m-%d at %H:%M"),
        text,
        reverse('forum-reply', args=[comment.post_id]),
    )
    return base + render_comment_tree(comment.children.all())


_link_regex = re.compile(r"(CRIM_Model_[0-9]{4}|CRIM_Mass_[0-9]{4}_[0-9])", re.IGNORECASE)
def insert_links(text):
    """Detect occurrences of piece IDs in the text, and insert HTML links."""
    return _link_regex.sub(lambda m: create_link(m.group(0)), text)


def create_link(piece_id):
    """Given a piece ID, return an HTML link."""
    matches = CRIMPiece.objects.filter(piece_id=piece_id)
    if matches:
        # There will be either zero or one pieces with this `piece_id`.
        piece = matches[0]
        return '<a href="{}">{}</a>'.format(piece.get_absolute_url(), piece_id)
    else:
        return piece_id
