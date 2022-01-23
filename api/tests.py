from django.test import TestCase
from io import StringIO
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from django.conf import settings
from api.views import MoviesList
from api.models import Movie, Genre
import json



class MovieTest(TestCase):
    # Unit test case for custom management command to populate database and search api.

    def setUp(self):
        # Get instance of APIRequestFactory To mock request object which will be directly passed to views as a first argument

        self.request_factory = APIRequestFactory()
        self.movies_url = reverse("movies")
        self.view = MoviesList.as_view()
        self.movies = self.create_movies()

    def create_movies(self):
        # if file is to big for memory we can then use pandas
        # currently this works for now
        try:
            json_file = f'{settings.BASE_DIR}/imdb-task.json'
            movies = []

            with open(json_file) as file:
                movies_data = file.read()
                movies_list = json.loads(movies_data)

                single_movie = {}
                for movie_obj in movies_list:
                    single_movie['popularity'] = movie_obj.get('99popularity')
                    single_movie['director'] = movie_obj.get('director')
                    single_movie['imdb_score'] = movie_obj.get('imdb_score')
                    single_movie['name'] = movie_obj.get('name')

                    movie, created = Movie.objects.get_or_create(
                        **single_movie)
                    genres = movie_obj.get('genre')

                    # create and link genres to movies
                    for genre in genres:
                        name = genre.strip()
                        genre, created = Genre.objects.get_or_create(name=name)
                        movie.genre.add(genre)

                    movie.save()
                    movies.append(movie)

                return movies

        except IOError as e:
            print(f'FIle not found, {e}')
            return

    def test_command_output(self):
        out = StringIO()
        call_command('populate_db', stdout=out)
        self.assertIn('Successfully inserted the data in database',
                      out.getvalue().strip())

    def test_search_movies_by_name_director_popularity_imdb_score(self):
        params = {'search': 'simpsons,Kirkland,90,9'}
        request = self.request_factory.get(
            self.movies_url, params, format='json')
        response = self.view(request)
        response.render()

        json_response = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert len(json_response) == 1
        assert json_response[0]['name'] == 'The Simpsons'

    def test_search_movies_with_pagination(self):
        params = {'search': 'Simpsons', 'limit': 10, 'offset': 0}
        request = self.request_factory.get(
            self.movies_url, params, format='json')
        response = self.view(request)
        response.render()

        json_response = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert len(json_response) == 4
        assert json_response['results'][0]['name'] == 'The Simpsons'

    def test_search_movies_by_name_and_genre(self):
        params = {'search': 'the,horror'}
        request = self.request_factory.get(
            self.movies_url, params, format='json')
        response = self.view(request)
        response.render()

        json_response = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert len(json_response) == 13
        assert json_response[0]['name'] == 'The Exorcist'

    def test_search_movies_by_name_and_director(self):
        params = {'search': 'psycho,hitchcock'}
        request = self.request_factory.get(
            self.movies_url, params, format='json')
        response = self.view(request)
        response.render()

        json_response = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert len(json_response) == 1
        assert json_response[0]['name'] == 'Psycho'

    def test_search_movies(self):
        params = {'search': 'cabiria'}
        request = self.request_factory.get(
            self.movies_url, params, format='json')
        response = self.view(request)
        response.render()

        json_response = json.loads(response.content)
        assert response.status_code == status.HTTP_200_OK
        assert len(json_response) == 1
        assert json_response[0]['name'] == 'Cabiria'

    def test_search_movies_by_all_params_with_pagination(self):
        params = {'search': 'the,john,70,7', 'limit': 10, 'offset': 0}
        request = self.request_factory.get(
            self.movies_url, params, format='json')
        response = self.view(request)
        response.render()

        json_response = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert json_response['count'] == 1
        assert json_response['results'][0]['name'] == 'The Lost Patrol'

    def test_search_movies_by_genre(self):
        params = {'search': 'War'}
        request = self.request_factory.get(
            self.movies_url, params, format='json')
        response = self.view(request)
        response.render()

        json_response = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert len(json_response) == 28
        assert json_response[0]['name'] == 'Star Wars'
