from django.core.management.base import BaseCommand, CommandError
from api.models import Movie, Genre
from django.conf import settings
import json


class Command(BaseCommand):
    # Inserts the Data from json file to database

    def handle(self, *args, **kwargs):

        json_file = f'{settings.BASE_DIR}/../imdb-task.json'

        with open(json_file) as file:
            moviesData = file.read()
            moviesList = json.loads(moviesData)

            # creating generators for fast and memory efficient processing
            moviesGenerator = (movie for movie in moviesList)
            singleMovie = {}
            for movieObj in moviesGenerator:
                singleMovie['popularity'] = movieObj.get('99popularity')
                singleMovie['director'] = movieObj.get('director')
                singleMovie['imdb_score'] = movieObj.get('imdb_score')
                singleMovie['name'] = movieObj.get('name')

                movie, created = Movie.objects.get_or_create(**singleMovie)
                genres = movieObj.get('genre')

                # creating and linking genres to movies
                for genre in genres:
                    name = genre.strip()
                    genre, created = Genre.objects.get_or_create(name=name)
                    movie.genre.add(genre)
                movie.save()