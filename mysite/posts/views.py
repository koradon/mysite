from urllib.parse import quote_plus
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.core.mail import send_mail

from taggit.models import Tag

from comments.models import Comment
from comments.forms import CommentForm
from .forms import PostForm, EmailPostForm
from .models import Post

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the blog index.")


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None,
                    request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Succesfully created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)

    # comments
    comments = instance.comments

    initial_data = {
        "content_type": instance.get_content_type,
        "object_id": instance.id
    }
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
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

        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    post_tags_ids = instance.tags.values_list('id', flat=True)
    similar_posts = Post.objects.active().filter(tags__in=post_tags_ids).exclude(slug=instance.slug)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by("-same_tags", '-publish')[:4]

    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
        "comments": comments,
        "comment_form": form,
        "similar_posts": similar_posts,
    }
    return render(request, "post_detail.html", context)


def post_list(request, tag_slug=None):
    tag = None

    today = timezone.now().date()

    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset_list = queryset_list.filter(tags__in=[tag])

    # Query from search bar
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(Q(title__icontains=query) |
                                             Q(content__icontains=query) |
                                             Q(user__first_name__icontains=query) |
                                             Q(user__last_name__icontains=query)).distinct()

    # Splits list of posts into pages
    paginator = Paginator(queryset_list, 15)

    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "title": "Posts list",
        "objects_list": queryset,
        "page_request_var": page_request_var,
        "today": today,
        "tag": tag,
    }
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)

    form = PostForm(request.POST or None,
                    request.FILES or None,
                    instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Succesfully created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect("posts:list")


def post_share(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = '{user_name} ({user_email}) zachęca do przeczytania "{post_title}"'.format(
                user_name=cd['name'],
                user_email=cd['email'],
                post_title=post.title)

            message = 'Przeczytaj post "{post_title}" na stronie {post_url}\n\n'.format(
                post_title=post.title,
                post_url=post_url,
            )

            # send_mail(subject, message, 'admin@mysite.com', [cd['to']])
            print("Message send - not realy")
            sent = True
    else:
        form = EmailPostForm()

    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }

    return render(request, "post_share.html", context)
