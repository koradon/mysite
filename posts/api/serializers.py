from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

from comments.api.serializers import CommentSerializer
from comments.models import Comment

from accounts.api.serializers import UserDetailSerializer

from posts.models import Post


post_detail_url = HyperlinkedIdentityField(
        view_name="posts-api:detail",
        lookup_field="slug",
    )

delete_url = HyperlinkedIdentityField(
        view_name="posts-api:delete",
        lookup_field="slug",
    )

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'publish',
        ]


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'user',
            'title',
            'content',
            'publish',
            'image',
        ]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None

        return image


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'user',
            'title',
            'slug',
            'content',
            'html',
            'content',
            'publish',
            'image',
            'comments',
        ]

    def get_html(self, obj):
        return obj.get_markdown()

    def get_user(self, obj):
        return str("{username}".format(username=obj.user.username))

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None

        return image

    def get_comments(self, obj):
        comments_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(comments_qs, many=True).data
        return comments
