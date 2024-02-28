from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.decorators import action
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
)
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.pagination import CustumPagination
from api.permissions import IsAuthor
from api.serializers import (
    RecipeCreateSerializer,
    RecipeReadSerializer,
    ListOfFollowingRecipesSerializer,
    )
from api.utils import download_shopping_cart
from recipes.models import (
    Favourite,
    Recipe,
    ShoppingCart,
)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вюсет рецептов"""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthor,)
    pagination_class = CustumPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    http_method_names = [
        i for i in viewsets.ModelViewSet.http_method_names if i not in ['put']
    ]

    def get_serializer_class(self):
        """Метод получения сериализатора"""

        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        """Метод создания рецепта"""

        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Метод редактирования рецепта"""

        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        """Метод добавления и удаления рецепта из избранного """

        user = self.request.user
        recipe = get_object_or_404(
            Recipe,
            pk=pk,
        )

        if self.request.method == 'POST':
            if Favourite.objects.filter(
                user=user,
                recipe=recipe,
            ).exists():
                return Response(
                    {
                        'errors':
                        '''
                        Вы не можете добавить рецепт в избранное,
                        если он уже в избранном
                        '''
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Favourite.objects.create(
                user=user,
                recipe=recipe,
            )
            serializer = ListOfFollowingRecipesSerializer(
                recipe,
                context={'request': request},
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        if self.request.method == 'DELETE':
            if not Favourite.objects.filter(
                user=user,
                recipe=recipe,
            ).exists():
                return Response(
                    {
                        'errors':
                        '''
                        Вы не можете удалить рецепт из избранного,
                        если его ещё нет в избранном
                        '''
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorite = get_object_or_404(
                Favourite,
                user=user,
                recipe=recipe,
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        """Метод добавления и удаления рецепта из списка покупок"""
        
        user = self.request.user
        recipe = get_object_or_404(
            Recipe,
            pk=pk,
        )

        if self.request.method == 'POST':
            if ShoppingCart.objects.filter(
                user=user,
                recipe=recipe,
            ).exists():
                return Response(
                    {
                        'errors':
                        '''
                        Вы не можете добавить рецепт в покупки,
                        если он уже в покупках
                        '''
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.create(
                user=user,
                recipe=recipe,
            )
            serializer = ListOfFollowingRecipesSerializer(
                recipe,
                context={'request': request},
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        if self.request.method == 'DELETE':
            if not ShoppingCart.objects.filter(
                user=user,
                recipe=recipe,
            ).exists():
                return Response(
                    {
                        'errors':
                        '''
                        Вы не можете удалить рецепт из покупок,
                        если его нет в покупках
                        '''
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            shopping_cart = get_object_or_404(
                ShoppingCart,
                user=user,
                recipe=recipe,
            )
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        """Метод скачивания списка покупок"""

        return download_shopping_cart(request)
