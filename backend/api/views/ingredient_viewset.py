from rest_framework import viewsets

from api.filters import NameSearchFilter
from api.permissions import IsAdmin
from api.serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингридиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (NameSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None
