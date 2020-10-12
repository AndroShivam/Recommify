import requests
import datetime
import base64
import os
import json
from urllib.parse import urlencode, quote

class SpotifyAPI(object):
	
	access_token = None
	current_user_access_token = None
	refresh_token = None
	access_token_expires = datetime.datetime.now()
	access_token_did_expire = True

	client_id = None
	client_secret = None

	# urls
	SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
	SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
	SPOTIFY_REDIRECT_URI = "https://recommify.herokuapp.com/result"
	SPOTIFY_API_URL = "https://api.spotify.com/v1"
	SPOTIFY_RECOMMENDATION_URL = "https://api.spotify.com/v1/recommendations?"
	SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"


	scope = "playlist-modify-public playlist-modify-private playlist-read-private user-read-recently-played"

	
	def __init__(self, client_id, client_secret, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.client_id = client_id
		self.client_secret = client_secret
	
	def get_client_credentials(self):
		"""
		Returns a base64 encoded string
		"""
		client_id = self.client_id
		client_secret = self.client_secret
		if client_secret == None or client_id == None:
			raise Exception("You must set client_id and client_secret")
		client_creds = f"{client_id}:{client_secret}"
		client_creds_b64 = base64.b64encode(client_creds.encode())
		return client_creds_b64.decode()

		
	def get_token_data(self):
		return {
			"grant_type": "client_credentials"
		} 

	def get_token_headers(self):
		client_creds_b64 = self.get_client_credentials()
		return {
			"Authorization": f"Basic {client_creds_b64}"
		}
	
	def perform_auth(self):
		token_url = self.SPOTIFY_TOKEN_URL
		token_data = self.get_token_data()
		token_headers = self.get_token_headers()
		r = requests.post(token_url, data=token_data, headers=token_headers)
		if r.status_code not in range(200, 299):
			raise Exception("Could not authenticate client.")
			# return False
		data = r.json()
		now = datetime.datetime.now()
		access_token = data['access_token']
		expires_in = data['expires_in'] # seconds
		expires = now + datetime.timedelta(seconds=expires_in)
		self.access_token = access_token
		self.access_token_expires = expires
		self.access_token_did_expire = expires < now
		return True


	def get_access_token(self):
		token = self.access_token
		expires = self.access_token_expires
		now = datetime.datetime.now()
		if expires < now:
			self.perform_auth()
			return self.get_access_token()
		elif token == None:
			self.perform_auth()
			return self.get_access_token() 
		return token
	
	def get_resource_header(self):
		access_token = self.get_access_token()
		headers = {
			"Authorization": f"Bearer {access_token}"
		}
		return headers
		

	def user_authorization(self, code):	
		code_payload = {
			"grant_type": "authorization_code",
			"code": str(code),
			"redirect_uri": self.SPOTIFY_REDIRECT_URI
		}
		
		post_request = requests.post(self.SPOTIFY_TOKEN_URL, data=code_payload, headers= self.get_token_headers())

		# Tokens are Returned to Application
		response_data = json.loads(post_request.text)

		print('this is code')
		print(code)
		print('this is response data')
		print(response_data)

		self.current_user_access_token = response_data["access_token"]
		refresh_token = response_data["refresh_token"]
		token_type = response_data["token_type"]
		expires_in = response_data["expires_in"]

		now = datetime.datetime.now()
		expires = now + datetime.timedelta(seconds=expires_in)

		if expires < now:
			authorization_header = {"Authorization" : f"Bearer {self.refresh_token}"}
		else:
			authorization_header = {"Authorization": f"Bearer {self.current_user_access_token}"}
		return authorization_header


	
	
	# URL for user Authentication
	def get_auth_url(self):
		query_params = {
			"client_id" : self.client_id,
			"response_type" :"code",
			"redirect_uri" : self.SPOTIFY_REDIRECT_URI,
			"scope" : self.scope
		}
		url_args = "&".join([f"{key}={quote(str(val))}" for key, val in query_params.items()])
		print(f"{self.SPOTIFY_AUTH_URL}/?{url_args}")
		return f"{self.SPOTIFY_AUTH_URL}/?{url_args}"

	# Get user profile data (we require user_id only to create playlist)
	def get_profile_data(self, headers):
		endpoint_url = "{}/me".format(self.SPOTIFY_API_URL)
		profile_response = requests.get(endpoint_url, headers = headers)
		print(profile_response.json())
		profile_data = json.loads(profile_response.text)
		return profile_data

	# Create playlist using user_id
	def create_playlist(self, user_id, playlist_name, playlist_desc):
		endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
		request_body = json.dumps({
			"name": playlist_name,
			"description": playlist_desc,
			"public": False
		})

		response = requests.post(url = endpoint_url,
		data = request_body, headers = {"Content-Type":"application/json",
		"Authorization": f"Bearer {self.current_user_access_token}"
		})

		return response.json()

	# Add tracks to playlist using playlist id and resulant uris
	def add_tracks_to_playlist(self, user_id, playlist_name, playlist_desc, uris = []):
		playlist = self.create_playlist(user_id = user_id, playlist_name = playlist_name, playlist_desc = playlist_desc)
		playlist_id = playlist['id'];

		endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

		request_body = json.dumps({
			"uris" : uris
		})

		response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
                        "Authorization": f"Bearer {self.current_user_access_token}"})

		if response.status_code == 201:
			return playlist['external_urls']['spotify']
		else:
			raise Exception("Something went Wrong! :(")

	# Get uri's of Artists and tracks by their name (artist and track names we got from input box)
	def get_uris(self, query_string, search_type):
		query_list = list(query_string.split(','))
		uris = []

		for query in query_list:
			headers = self.get_resource_header()
			data = urlencode({"q": query, "type": search_type.lower()})
			lookup_url = f"{self.SPOTIFY_SEARCH_URL}?{data}"
			response = requests.get(lookup_url, headers=headers)
			if response.status_code not in range(200, 299):  
				return {}
			response = response.json()

			if search_type.lower() == 'artist':
				items = response['artists']['items']
				uri = items[0]['id']
				uris.append(uri)
			elif search_type.lower() == 'track':
				item = response['tracks']['items']
				uri = item[0]['id']
				uris.append(uri)

		return uris

	# recommends tracks based on various params like seed_artists, seed_genres, seed_tracks (there are still alot of params you can pass lookup at docs)
	def recommend(self,seed_artists, seed_genres, seed_tracks, limit = 10, market = 'US', target_danceability = 0): 
		headers = self.get_resource_header()
		lookup_url = f'{self.SPOTIFY_RECOMMENDATION_URL}limit={limit}&market={market}&seed_artists={seed_artists}&seed_genres={seed_genres}&seed_tracks={seed_tracks}&target_danceability={target_danceability}'
		response = requests.get(lookup_url, headers = self.get_resource_header())
		if response.status_code not in range(200, 299):  
			return {}
		return response.json()



