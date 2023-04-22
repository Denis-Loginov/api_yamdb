from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'get_genres', 'category', 'description')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'year', 'description')
    filter_horizontal = ('genre',)

    @admin.display(description='Жанр')
    def get_genres(self, obj):
        """Возвращает список жанров для отображения."""
        return '\n'.join([genre.name for genre in obj.genre.all()])


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}
