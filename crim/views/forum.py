from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ForumPostForm
from ..models.forum import ForumPost
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


def view_post(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    return render(request, "forum/view_post.html", {"post": post})
