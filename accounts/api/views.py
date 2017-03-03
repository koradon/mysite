from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView,\
    RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, \
    IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination

from .serializers import UserCreateSerializer


User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()