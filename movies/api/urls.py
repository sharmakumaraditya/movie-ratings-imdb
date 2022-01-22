from django.urls import path
from api.views import MoviesList

urlpatterns = [
    path('movies', MoviesList.as_view(), name='movies'),
]