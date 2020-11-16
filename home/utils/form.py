from django import forms

class SearchForm(forms.Form):
    seed_artists = forms.CharField(label = 'artist name')
    seed_genres = forms.CharField(label = 'genre name')
    seed_tracks = forms.CharField(label = 'track name')

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args , **kwargs)


        self.fields['seed_artists'].widget.attrs['id'] = 'id_artists'
        self.fields['seed_artists'].widget.attrs['placeholder'] = 'Ex. twenty one pilots, lauv'
        self.fields['seed_artists'].widget.attrs['style'] = 'width:350px; height:50px'

        self.fields['seed_genres'].widget.attrs['id'] = 'id_genres'
        self.fields['seed_genres'].widget.attrs['placeholder'] = 'Ex. rock, indie'
        self.fields['seed_genres'].widget.attrs['style'] = 'width:350px; height:50px'

        self.fields['seed_tracks'].widget.attrs['id'] = 'id_tracks'
        self.fields['seed_tracks'].widget.attrs['placeholder'] = 'Ex. let you down'
        self.fields['seed_tracks'].widget.attrs['style'] = 'width:350px; height:50px'

class ResultForm(forms.Form):
    playlist_name = forms.CharField(label = '')
    playlist_desc = forms.CharField(label = '')

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)

        self.fields['playlist_name'].widget.attrs['id'] = 'id_playlist_name'
        self.fields['playlist_name'].widget.attrs['placeholder'] = 'Playlist Name'

        self.fields['playlist_desc'].widget.attrs['id'] = 'id_playlist_desc'
        self.fields['playlist_desc'].widget.attrs['placeholder'] = 'Playlist Description'