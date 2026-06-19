from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from api.permissions import IsAuthorOrReadOnly
from posts.models import Group, Post

from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    """Тут вся логика для постов"""

    queryset = Post.objects.select_related('author', 'group').all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """При создании поста
        автоматически ставлю текущего пользователя автором
        """
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Сообщества только читаем, создавать их через API не даём"""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Здесь работаю с комментариями конкретного поста"""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_post(self):
        """Сначала достаю пост из url, к которому относятся комментарии"""
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        """Отдаю только комментарии текущего поста"""
        return self.get_post().comments.select_related('author', 'post')

    def perform_create(self, serializer):
        """При создании комментария сам подставляю автора и пост"""
        serializer.save(
            author=self.request.user,
            post=self.get_post(),
        )


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Тут пользователь смотрит свои подписки и создаёт новые"""

    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        """Показываю только подписки текущего пользователя"""
        return self.request.user.follower.select_related('user', 'following')

    def perform_create(self, serializer):
        """При создании подписки сам записываю текущего пользователя"""
        serializer.save(user=self.request.user)
