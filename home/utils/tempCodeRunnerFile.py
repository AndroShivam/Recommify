import os

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

spotify = SpotifyAPI(client_id, client_secret)
result = spotify.search('indie')

print(result)