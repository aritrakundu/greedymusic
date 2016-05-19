from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Q
from .models import TrackModel, GenreModel
from .forms import TrackForm, GenreForm
from .props import *

def home(request):
	return HttpResponseRedirect(reverse('view_tracklist'))

def list_tracks(request):
	if request.method == 'GET':
		url_add_track = reverse('view_add_track')
		music_tracks = TrackModel.objects.all()
		context = {
			'tracks' : music_tracks,
			'url_add_track' : url_add_track,
		}
		session_context = request.session.get(SESSION_KEY)
		if session_context:
			print 'session_context' , session_context
			context.update(session_context)
			if 'tracks' not in session_context:
				context['tracks'] = music_tracks
			else:
				music_tracks = [obj.object for obj in serializers.deserialize('json', session_context.get('tracks'))]
				context['tracks'] = music_tracks
			del request.session[SESSION_KEY]	
	else:
		print 'Bad request'
	print 'context', context
	return render(request, track_template, context)

def add_music_track(request):
	if request.method == 'POST':
		try:
			instance = GenreModel.objects.get(genre_name__iexact=request.POST.get('genre_name'))
		except GenreModel.DoesNotExist:
			print 'Genre deos not exist'
			instance = None
		if instance:
			form = GenreForm(request.POST, instance=instance)
			if form.is_valid():
				instance = form.save()
				print 'Genre instance created/saved'
				form = TrackForm(request.POST)
				print 'Posted Request : ', request.POST
				if form.is_valid():
					_instance = form.save(commit=False)
					_instance.track_genre = instance
					form.save()
					print 'Form saved to model'
					context = {
						SUCCESS : 'Track Successfully added',
					}
				else:
					print 'Bad data'
					context = {
						ERRORS : 'Form submission failed. Somthing bad happened',
					}
			else:
				print 'Invalid GenreForm data'
				context = {
					WARNING : 'Somthing bad happened',
				}
		else:
			print 'Genre does not exist. Must create one first'
			context = {
				ERRORS : 'Genre does not exist. Please create one first',
			}
		request.session[SESSION_KEY] = context
	else:
		print 'Bad request'
	return HttpResponseRedirect(reverse('view_tracklist'))

def search_music_tracks(request):  #, *args, **kwargs):#query, search_term):
	query = request.GET.get('q')
	search_term = request.GET.get('search_term')
	print query, search_term
	if not query or not search_term:
			if query not in ('title', 'genre', 'all'):	print 'Bad parameters'
			return HttpResponseRedirect(reverse('view_tracklist'))
	if query == 'title':
		music_tracks = TrackModel.objects.filter(track_title__icontains=search_term)
		music_tracks = serializers.serialize("json", music_tracks)
		context = {
			'tracks' : music_tracks,
		}
	elif query == 'genre':
		music_tracks = TrackModel.objects.filter(track_genre__genre_name__icontains=search_term)
		music_tracks = serializers.serialize("json", music_tracks)
		context = {
			'tracks' : music_tracks,
		}
	else:
		music_tracks = TrackModel.objects.filter(
				Q(track_title__icontains=search_term) | Q(track_genre__genre_name__icontains=search_term))
		music_tracks = serializers.serialize("json", music_tracks)
		context = {
			'tracks' : music_tracks,
		}

	request.session[SESSION_KEY] = context
	return HttpResponseRedirect(reverse('view_tracklist'))

def get_track(request, trackid):
	if request.method == 'GET':
		try:
			track = TrackModel.objects.get(pk=trackid)
			url_edit_track = reverse('view_edit_track')
			context = {
				'track_id' : track.id,
				'track_title' : track.track_title,
				'track_genre' : track.track_genre,
				'track_rating' : track.track_rating,
				'url_edit_track' : url_edit_track,
				'back_url' : '/tracks/',
			}
			response = render(request, edit_track_template, context)
		except TrackModel.DoesNotExist:
			context = {
				ERROR : 'Track does not exist',
			}
			request.session[SESSION_KEY] = context
			response = HttpResponseRedirect(reverse('view_tracklist'))
		
		return response

def edit_track(request):
	if request.method == 'POST':
		print 'POSTed Request : ', request.POST
		id = int(request.POST.get('id'))
		genre = request.POST.get('genre_name')
		try:
			genre_instance = get_object_or_404(GenreModel, genre_name__iexact=genre)
			try:
				track_instance = get_object_or_404(TrackModel, id=id)
				form = TrackForm(request.POST, instance=track_instance)
				if form.is_valid():
					defaults = {
						'genre_name' : genre,
					}
					track_instance = form.save(commit=False)
					track_instance.track_genre = genre_instance
					form.save()
					context = {
						SUCCESS : 'Track details successfully saved',
					}
				else:
					print 'Bad data'
					context = {
						WARNING : 'Somthing bad happened',
					}
			except Http404:
				print 'Track not found'
				context = {
					ERRORS : 'Track does not exist',
			}
		except Http404:
			genre_instance = None
			context = {
				ERRORS : 'Genre does not exist. Please create one first',
			}

		
		request.session[SESSION_KEY] = context
	else:
		print 'Bad Request'
	return HttpResponseRedirect(reverse('view_tracklist'))

def list_genres(request):
	if request.method == 'GET':
		url_add_genre = reverse('view_add_genre')
		genre_list = GenreModel.objects.all()
		context = {
			'genres' : genre_list,
			'url_add_genre' : url_add_genre,
		}
		if SESSION_KEY in request.session:
			context.update(request.session.get(SESSION_KEY))
			del request.session[SESSION_KEY]
		return render(request, genre_template, context)

def add_genre(request):
	if request.method == 'POST':
		form = GenreForm(request.POST)
		if form.is_valid():
			form.save()
		else:
			print 'Bad data'
			# print 'Form errors'
			# print form.non_field_errors
			context = {
				WARNING : 'Somthing bad happened',
			}
			request.session[SESSION_KEY] = context
	else:
		print 'Bad request'
	return HttpResponseRedirect(reverse('view_genrelist'))


def get_genre(request, genreid):
	if request.method == 'GET':
		response = None
		try:
			genre = GenreModel.objects.get(pk=genreid)
			print 'Genre = ', genre
			url_rename_genre = reverse('view_rename_genre')
			context = {
				'genre_id' : genre.id,
				'genre_title' : genre.genre_name,
				'url_rename_genre' : url_rename_genre,
				'back_url' : '/genres/',
			}
			response = render(request, rename_genre_template, context)
		except GenreModel.DoesNotExist:
			context = {
				ERROR : 'Track not found',
			}
			response = HttpResponseRedirect(reverse('view_genrelist'))

		request.session[SESSION_KEY] = context
		return response
	else:
		print 'Bad Request'
		response = HttpResponseRedirect(reverse('view_genrelist'))
	return response

def rename_genre(request):
	if request.method == 'POST':
		context = dict()
		id = int(request.POST.get('id'))
		try:
			instance = get_object_or_404(GenreModel, id=id)
			form = GenreForm(request.POST, instance=instance)
			if form.is_valid():
				form.save()
			else:
				print 'Somthing bad happened'
				context = {
					WARNING : 'Invalid data',
				}
		except Http404:
			context = {
					ERRORS : 'Genre does not exist.'
				}
		request.session[SESSION_KEY] = context
	else:
		print 'Bad Request'
	return HttpResponseRedirect(reverse('view_genrelist'))