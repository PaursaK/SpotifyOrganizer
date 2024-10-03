import Album
import Artist
class Song:

    def __init__(self, name: str, id: str, uri: str, album: Album, artist: Artist):
        '''simple constructor for song object to easily manage relevant info about a song'''
        self.name = name
        self.id = id
        self.uri = uri
        self.album = album
        self.artist = artist
        self.genres = self.artist.genres
        self.audioFeatures = None
        self.cluster = None


    def setSongClusterID(self, clusterID):
        self.cluster = clusterID


    def setAudioFeatures(self, audioFeatures):
        self.audioFeatures = audioFeatures
    
    def getAudioFeatureList(self):
        '''Returns a list of audio features: [danceability, energy, tempo, valence]'''
        if self.audioFeatures:
            return [
                self.audioFeatures['danceability'],
                self.audioFeatures['energy'],
                self.audioFeatures['tempo'],
                self.audioFeatures['valence']
            ]
        return []

    def __str__(self):
        return f'Track Name: {self.name}\nTrack Artist: {self.artist}\nTrack Album: {self.album}\nArtist Genre: {self.artist.genres}' 