from django.db import models

# Create your models here.

class Genre(models.Model):
    """
    Genre model to store all types of Genre
    """
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    Movie model to store movies data
    """
    popularity = models.FloatField()
    director = models.CharField(max_length=250, db_index=True)
    imdb_score = models.FloatField()
    name = models.CharField(max_length=250, db_index=True)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name