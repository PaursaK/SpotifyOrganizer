import Album
import Artist
class Song:

    def __init__(self, name: str, id: str, album: Album, artist: Artist):
        '''simple constructor for song object to easily manage relevant info about a song'''
        self.name = name
        self.id = id
        self.album = album
        self.artist = artist
        self.lyrics = None
        self.genres = self.artist.genres
        self.mood = None

    def setLyrics(self, lyrics: str):
        self.lyrics = lyrics

    def setMood(self, mood: list):
        self.mood = mood

    def to_dict(self):
        '''Convert the Song object to a dictionary.'''
        return {
            "name": self.name,
            "id": self.id,
            "album": self.album.title,
            "artist": self.artist.name,
            "mood": self.mood,
            "genre": self.genres
            }

    def __str__(self):
        return f'Track Name: {self.name}\nTrack Artist: {self.artist}\nTrack Album: {self.album}\nArtist Genre: {self.artist.genres}' 