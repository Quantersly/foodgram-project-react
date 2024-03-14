from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from api.pagination import CustumPagination
from api.serializers import (
    FollowSerializer,
    UserSerializer,
)
from users.models import (
    Follow,
    User,
)


class UserFollowViewSet(UserViewSet):
    """Вьюсет для пользователей и подписок на них"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustumPagination

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        """Метод получения списка подписок пользователя"""

        user = request.user
        queryset = User.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            page,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id):
        """Метод подписки и отписки"""

        user = request.user
        author = get_object_or_404(
            User,
            id=id,
        )

        if request.method == 'POST':
            if user.id == author.id:
                return Response(
                    {
                        'detail':
                        'Вы не можете подписаться на себя'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Follow.objects.filter(
                author=author,
                user=user,
            ).exists():
                return Response(
                    {
                        'detail':
                        'Вы не можете оподписаться, если уже подписаны'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Follow.objects.create(
                user=user,
                author=author,
            )
            serializer = FollowSerializer(
                author,
                context={'request': request},
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        if not Follow.objects.filter(
            user=user,
            author=author,
        ).exists():
            return Response(
                {
                    'errors':
                    'Вы не можете отписаться, если ещё не подписаны'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription = get_object_or_404(
            Follow,
            user=user,
            author=author,
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed(request.method)

    @action(
        ["get", "delete"],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        return self.destroy(request, *args, **kwargs)
