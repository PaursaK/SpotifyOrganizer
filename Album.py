import Artist
class Album:

    def __init__(self, title: str, id: str, artist: Artist):
        '''simple constructor for song object to easily manage relevant info about a song'''
        self.title = title
        self.id = id
        self.artist = artist

    def __str__(self):
        return self.title