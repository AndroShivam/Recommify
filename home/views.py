import os
from django.shortcuts import render, redirect
from home.utils.api import SpotifyAPI
from home.utils.form import *
from home.utils.utils import Utils
from django.http import JsonResponse,HttpResponse


client_id = "your client id"
client_secret = "your client secret"

spotify = SpotifyAPI(client_id, client_secret)

# contains uri's of resultant tracks
uris = []
# contains code from url
url = []

def main_home(request):
    form = SearchForm()
    return render(request, 'home/home.html', {'form': form})


def get_response(request):

    if request.method == 'POST':

        uris.clear()

        # get input from input box
        artists = request.POST.get('artists')
        genres = request.POST.get('genres')
        tracks = request.POST.get('tracks')

        # get artist and track uris by from name and convert comma (",") seperated genres to list
        artist_uris = spotify.get_uris(query_string = artists, search_type = 'artist')
        track_uris = spotify.get_uris(query_string = tracks, search_type = 'track')
        genre_list = list(tracks.split(','))

        # get final url of all artists, genres, tracks (replaces spaces with '%2C')
        seed_artists_url = Utils(artist_uris).urlify()
        seed_genres_url = Utils(genre_list).urlify()
        seed_tracks_url = Utils(track_uris).urlify()

        # get recommendations by passing these values
        result = spotify.recommend(seed_artists = seed_artists_url, seed_genres = seed_genres_url, seed_tracks = seed_tracks_url)

        # append result track uri's to uris list
        for res in result['tracks']:
            uris.append(res['uri'])

        
        return JsonResponse(result) # return Json response to ajax function

    return HttpResponse('<center><h1>Something went wrong ! :(</h1></center>')       


# Authenticate current user 
def authenticate_user(request):
    auth_url = spotify.get_auth_url()
    return redirect(auth_url)


def result(request):

     # After Authentication the url looks like this https://example.com/callback?code=NApCCg..BkWtQ&state=profile%2Factivity
     # we get the code by calling get mehod


    if request.method == 'POST':
        form = ResultForm(request.POST)

        if form.is_valid():
            playlist_name = form.cleaned_data['playlist_name']
            playlist_desc = form.cleaned_data['playlist_desc']

            # Get profile date of the current user
            headers = spotify.user_authorization(code = code)
            profile_data = spotify.get_profile_data(headers = headers)

            # Get user_id to create a new playlist 
            user_id = profile_data['id']

            playlist_link = spotify.add_tracks_to_playlist(user_id = user_id, playlist_name = playlist_name, playlist_desc = playlist_desc, uris = uris)

            return render(request, 'home/result.html', {'form': form, 'playlist_link' : playlist_link})

    else:
        code = request.GET.get('code', None)
        form = ResultForm()
    return render(request, 'home/result.html',{'form': form})

