from rest_framework import viewsets

from api.permissions import IsAdmin
from api.serializers import TagSerializer
from recipes.models import Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тегов"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None
