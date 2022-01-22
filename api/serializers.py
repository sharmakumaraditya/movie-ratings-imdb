from rest_framework import serializers
from api.models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):

    # Serialize genre objects

    class Meta:
        model = Genre
        fields = ['name']


class MovieSerializer(serializers.ModelSerializer):

    # Serialize movie objects and can be used for validation too

    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['name', 'director', 'popularity', 'imdb_score', 'genre']