from django.contrib import admin

from .models import (
    Tag,
    Recipe,
    RecipeIngredients,
    ShoppingCart,
    Favourite,
    Ingredient
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = (
        'name',
        'color',
        'slug',
    )
    list_filter = (
        'name',
        'color',
        'slug',
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
        'measurement_unit',
    )


class RecipeIngredientsInLine(admin.TabularInline):
    model = RecipeIngredients
    autocomplete_fields = ('ingredient',)
    min_num = 1
    extra = 2


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'cooking_time',
        'image',
        'created',
    )
    search_fields = (
        'name',
        'author',
        'text',
        'cooking_time',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    readonly_fields = ('favorite_count',)

    inlines = (RecipeIngredientsInLine,)

    def favorite_count(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredients)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = (
        'recipe',
        'ingredient',
    )
    list_filter = (
        'recipe',
        'ingredient',
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )


@admin.register(Favourite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
        'recipe',
    )
