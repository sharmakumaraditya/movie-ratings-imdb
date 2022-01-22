from django.contrib import admin
from api.models import Movie, Genre

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'director', 'popularity', 'imdb_score']
    list_filter = ['genre']
    search_fields = ['name', 'director']


class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)