from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ForumPostForm
from ..models.forum import ForumPost


def create_post(request):
    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = ForumPost.objects.create(text=form.cleaned_data["body"])
            return redirect("view_forum_post", post.pk)
    else:
        form = ForumPostForm()

    return render(request, "forum/create_post.html", {"form": form})


def view_post(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    return render(request, "forum/view_post.html", {"post": post})
