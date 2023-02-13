from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class GenreInline(admin.TabularInline):
    model = Title.genre.through
    extra = 0


class GenreAdmin(admin.ModelAdmin):
    inlines = [GenreInline, ]
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'get_genres')
    list_select_related = ('category',)
    list_display_links = ('name',)
    search_fields = ('name', 'year')
    list_filter = ('category', 'genre')
    inlines = (GenreInline,)

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])
    get_genres.short_description = 'Жанр'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'score', 'author', 'pub_date')
    list_select_related = ('author',)
    list_display_links = ('text',)
    search_fields = ('title', 'text', 'score', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    list_select_related = ('author',)
    list_display_links = ('text',)
    search_fields = ('review', 'text', 'author')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
