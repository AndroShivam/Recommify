class Utils:

    def __init__(self, seed_genres, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seed_genres = seed_genres

    # replace spaces with "%2C" (example - indie rock -> indie%2Crock )
    def urlify(self):
        seed_genres = self.seed_genres
        result = ''
        seperator = ''
        for genre in seed_genres:
            result = result + seperator + genre
            seperator = '%2C'
        return result