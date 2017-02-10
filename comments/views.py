from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from .models import Comment
from .forms import CommentForm


# Create your views here.
def comment_thread(request, id):
    obj = get_object_or_404(Comment, id=id)
    original_post = obj.content_object.get_absolute_url()

    initial_data = {
        "content_type": obj.content_type,
        "object_id": obj.object_id,
    }

    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(user=request.user,
                                                             content_type=content_type,
                                                             object_id=obj_id,
                                                             content=content_data,
                                                             parent=parent_obj)

        return HttpResponseRedirect(parent_obj.get_absolute_url())

    context = {
        "comment": obj,
        "form": form,
        "original_post": original_post,
    }
    return render(request, "comment_thread.html", context)


def comment_delete(request, id):
    obj = get_object_or_404(Comment, id=id)

    if request.method == POST:
        parent_object_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "Comment deleted")
        return HttpResponseRedirect(parent_object_url)

    context = {
        "object": obj,
    }

    return render(request, "confirm_delete.html", context)
