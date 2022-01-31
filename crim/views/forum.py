import html
import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..models.document import CRIMSource
from ..models.forum import CRIMForumPost
from ..models.mass import CRIMMass
from ..models.observation import CJObservation
from ..models.person import CRIMPerson
from ..models.piece import CRIMPiece
from ..models.relationship import CJRelationship
from ..models.user import CRIMUserProfile


def anchor(comment):
    '''Returns a sort of permalink for the comment's position on a page,
    in the form `username-00000000`, where 00000000 is the epoch timestamp
    of the comment.'''
    return comment.author.username + '-' + str(comment.created_at.strftime("%s"))


def index(request):
    posts = CRIMForumPost.objects.order_by("-created_at")
    context = {"posts": posts}
    return render(request, "forum/post_list.html", context)


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
    # Throughout: escape any non-literal text that may contain HTML!
    post = get_object_or_404(CRIMForumPost, post_id=post_id)
    if post.head:
        head = post.head
    else:
        head = post

    if post.head:
        post_title = 'Reply to ‘{}’'.format(html.escape(head.title))
        html_title = '<a href="{}">Reply</a> to <a href={}>‘{}’</a>'.format(
            reverse('forum-view-post', args=[post.head.post_id]) + '#' + anchor(post),
            reverse('forum-view-post', args=[post.head.post_id]),
            html.escape(post.head.title),
        )
    else:
        post_title = html.escape(head.title)
        html_title = post_title

    post_author = head.author.name
    html_author = '<a href="{}">{}</a>'.format(
        reverse('crimperson-detail', args=[head.author.person.person_id]),
        head.author.name,
    )
    post_text = insert_links(html.escape(post.text))
    comments = render_head(post)
    context = {
        'comments': comments,
        'post': post,
        'post_title': post_title,
        'html_title': html_title,
        'post_text': post_text,
        'post_author': post_author,
        'html_author': html_author,
    }
    return render(request, "forum/view_post.html", context)


def render_head(comment):
    return '<ul class="forum-comment head">' + render_comment(comment, color=False) + '</ul>'


def render_comment_children(comment_set, color=False):
    comment_html = ''
    for comment in comment_set:
        comment_html += render_comment(comment, color)

    if comment_html:
        return '<ul class="forum-comment">' + comment_html + '</ul>'
    else:
        return ''


def render_comment(comment, color=False):
    if comment.author:
        author = comment.author.name
    else:
        author = '[deleted]'

    # VERY IMPORTANT: escape any non-literal text that may contain HTML!
    author = html.escape(author)

    text = html.escape(comment.text)
    text = insert_links(text)
    base = '''<li class="forum-post {5}" id="{6}">
<h4 class="forum-subhead">{0}</h4>
<p class="forum-text">{2}</p>
<p><a href="{3}">{1}</a> &bull; <a href="{4}">Reply</a></p>
</li>'''.format(
        author,
        comment.created_at.strftime("%Y-%m-%d at %H:%M"),
        text,
        reverse('forum-view-post', args=[comment.post_id]),
        reverse('forum-reply', args=[comment.post_id]),
        'dark' if color else 'light',
        anchor(comment),
    )
    return base + render_comment_children(comment.children.order_by('created_at'), color=(not color))


_piece_regex = re.compile(r'(CRIM_Model_[0-9]{4}|CRIM_Mass_[0-9]{4}_[0-9])', re.IGNORECASE)
_mass_regex = re.compile(r'CRIM_Mass_[0-9]{4}(?!_)', re.IGNORECASE)
_source_regex = re.compile(r'(CRIM_Source_[0-9]{4})', re.IGNORECASE)
_person_regex = re.compile(r'(CRIM_Person_[0-9]{4})', re.IGNORECASE)
_observation_regex = re.compile(r'&lt;([0-9]+)&gt;', re.IGNORECASE)
_relationship_regex = re.compile(r'&lt;R([0-9]+)&gt;', re.IGNORECASE)
_newline_regex = re.compile(r'[\r\n]+')
def insert_links(text):
    '''Detect occurrences of piece IDs in the text, and insert HTML links.'''
    text = _piece_regex.sub(lambda m: create_link(CRIMPiece, m.group(0), piece_id=m.group(0)), text)
    text = _mass_regex.sub(lambda m: create_link(CRIMMass, m.group(0), mass_id=m.group(0)), text)
    text = _source_regex.sub(lambda m: create_link(CRIMSource, m.group(0), document_id=m.group(0)), text)
    text = _person_regex.sub(lambda m: create_link(CRIMPerson, m.group(0), person_id=m.group(0)), text)
    # the group(1) is for matching just the integer id and not the angle brackets around it.
    text = _observation_regex.sub(lambda m: create_link(CJObservation, m.group(0), id=int(m.group(1))), text)
    text = _relationship_regex.sub(lambda m: create_link(CJRelationship, m.group(0), id=int(m.group(1))), text)
    text = '<p>' + _newline_regex.sub('</p><p>', text) + '</p>'
    return text


def create_link(CRIMModel, link_text, **id_field):
    '''Given an id_field (eg {'piece_id', 'CRIM_Model_0001'}), along with the
    model object, return an HTML link.
    '''
    matches = CRIMModel.objects.filter(**id_field)
    for v in id_field.values():
        if matches:
            # There will be either zero or one pieces with this id.
            object = matches[0]
            return '<a href="{}">{}</a>'.format(object.get_absolute_url(), link_text)
        else:
            return link_text
