<h1 align="center">Recommify</h1>

<p align="center">
Recommify uses Spotify Web API to recommend music to you by mixing different artists, genres and tracks.
So that you're never out of music 🎶.<br>
</p>
<br>


<p align="center">
<img src="https://github.com/AndroShivam/Recommify/blob/main/screenshots/recommify.gif?raw=true"/>
</p>

## Check it out
- [Recommentify](https://recommentify.herokuapp.com) 

## Tech stack & Open-source libraries
- [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines.
- [Bootstrap 4](https://github.com/twbs/bootstrap) - The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web.
- [Plyr](https://github.com/sampotts/plyr) - A simple HTML5, YouTube and Vimeo player
- [Spotify for Developers](https://developer.spotify.com/) - Build experiences for millions of music lovers with playback, personalization, and much, much more.

## How to Use
1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard)
2. Login and create a new app
3. Set redirect url in app's settings (if changing name)
4. Change redirect url in api.py (if changing name)
5. Copy the client id and client secret into views.py
6. Enjoy!

## Known Issues
1. Preview_uri of 30 sec is broken (for now)
2. url out of index bound when making two playlists one after another (sometimes)
