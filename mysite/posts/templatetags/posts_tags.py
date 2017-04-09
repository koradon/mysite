from django import template
from django.db.models import Count

register = template.Library()

from ..models import Post


@register.simple_tag
def total_posts():
    return Post.objects.active().count()


@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.objects.active()[:count]
    return {"latest_posts": latest_posts}
