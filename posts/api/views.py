from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView,\
    RetrieveAPIView, RetrieveUpdateAPIView

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, \
    IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly

from posts.models import Post
from .serializers import PostDetailSerializer, PostListSerializer, PostCreateUpdateSerializer


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, IsAdminUser]


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
