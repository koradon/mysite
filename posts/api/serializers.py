from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, SerializerMethodField

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
    user = SerializerMethodField()
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

    def get_user(self, obj):
        return str("{username}".format(username=obj.user.username))

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None

        return image


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()
    image = SerializerMethodField()
    html = SerializerMethodField()

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
            'image'
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
