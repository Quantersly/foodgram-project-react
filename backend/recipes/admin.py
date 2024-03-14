from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

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


class RecipeIngredientsFormSet(BaseInlineFormSet):

    def clean(self):
        super(RecipeIngredientsFormSet, self).clean()
        count_of_ingredients = 0
        count_of_delited = 0
        set_ingredients = set({})
        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                count_of_delited += 1
            if len(form.cleaned_data) > 3:
                count_of_ingredients += 1
                set_ingredients.add(form.cleaned_data['ingredient'])

        if count_of_ingredients == 0:
            raise ValidationError('Добавьте хотя бы 1 ингредиент')
        if count_of_ingredients == count_of_delited:
            raise ValidationError('Нельзя удалить все ингредиенты')
        if len(set_ingredients) != count_of_ingredients:
            raise ValidationError('Нельзя добавлять одинаковые ингредиенты')


class RecipeIngredientsInLine(admin.StackedInline):
    model = RecipeIngredients
    formset = RecipeIngredientsFormSet
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
