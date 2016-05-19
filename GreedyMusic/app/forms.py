from django import forms
from .models import TrackModel, GenreModel
class TrackForm(forms.ModelForm):
	class Meta:
		model = TrackModel
		fields = ('track_title', 'track_rating',)

class GenreForm(forms.ModelForm):
	class Meta:
		model = GenreModel
		fields = ('genre_name',)