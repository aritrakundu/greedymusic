from __future__ import unicode_literals
from django.db import models

# Create your models here.

class GenreModel(models.Model):
	genre_name = models.CharField(blank=False, unique=True, max_length=20)

	def __str__(self):
		return self.genre_name

class TrackModel(models.Model):
	CHOICES = (
	    ('1', '1 star'),
	    ('2', '2 stars'),
	    ('3', '3 stars'),
		('4', '4 stars'),
		('5', '5 stars'),
  	)

	track_title = models.CharField(blank=False, max_length=20)
	track_genre = models.ForeignKey(GenreModel, on_delete=models.CASCADE, null=False)#models.CharField(blank=False, max_length=20)
	track_rating = models.CharField(blank=True, choices=CHOICES, max_length=10)

	class Meta:
		unique_together = ('track_title', 'track_genre')

	def __str__(self):
		return self.track_title
