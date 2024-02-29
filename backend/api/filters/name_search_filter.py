from rest_framework.filters import SearchFilter


class NameSearchFilter(SearchFilter):
    """Фильтр поиска имени"""

    search_param = 'name'
