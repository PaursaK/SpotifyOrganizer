import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Song import Song
from Album import Album
from Artist import Artist
from sklearn.cluster import KMeans
import numpy as np
from sklearn.preprocessing import StandardScaler

#user authetication
auth_manager = SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:3000",
    scope="user-library-read playlist-modify-public"
)

#profile object
sp = spotipy.Spotify(auth_manager=auth_manager)


def fetch_all_saved_tracks(sp: spotipy) -> list:
    '''fetches a list tracks in the users liked songs \n
    :param: sp -> spotify user object
    :return: list of all liked songs
    '''
    all_tracks = []
    limit = 50  # Max number of tracks per request
    offset = 0  # Offset for pagination

    while True:
        # Fetch the saved tracks
        saved_tracks = sp.current_user_saved_tracks(limit=limit, offset=offset)
        # Add the tracks to the list
        all_tracks.extend(saved_tracks['items'])
        # Check if we have fetched all the tracks
        if len(saved_tracks['items']) < limit:
            # If less than 'limit' tracks were returned, we have reached the end
            break
        # Move the offset forward to grab the next batch
        offset += limit

    return all_tracks

def getArtistForTrack(track: dict) -> Artist:
    '''grabs the first artist for a song and creates/returns an artist object
    :param: track dictionary data
    :return: artist object
    '''
    #secure the first two parameters
    artistName = track['track']['artists'][0]['name']
    artistId = track['track']['artists'][0]['id']

    #get genres the artist of track is associated with
    artistInfo = sp.artist(artist_id=artistId)
    artistGenres = genres = artistInfo.get('genres', [])

    #create artist object
    artist = Artist(artistName, artistId, artistGenres)
    return artist

def getAlbumForTrack(track: dict) -> Artist:
    '''grabs the first artist for a song and creates/returns an artist object
    :param: track dictionary data
    :return: artist object
    '''
    #grab artist
    artist = getArtistForTrack(track)
    #create album object
    album = Album(track['track']['album']['name'], track['track']['album']['id'], artist)
    return album

def getAudioFeatures(trackID: str):
    '''returns the four relevant audio features '''
    relevantAudioFeatures = {}

    audio_features = sp.audio_features(trackID)[0]

    return audio_features

def normalizeAudioFeaturesForClustering(song_list: list):
    
    '''Prepares and normalizes audio features for clustering'''
    scaler = StandardScaler()

    # Extract audio features from all songs
    audio_features = [song.getAudioFeatureList() for song in song_list if song.audioFeatures]
    audio_features = np.array(audio_features)

    # Normalize the features
    audio_features_scaled = scaler.fit_transform(audio_features)
    
    return audio_features_scaled

def clusterTracks(n_clusters, song_list):
    '''Clusters the songs and returns the cluster assignments'''
    audio_features_scaled = normalizeAudioFeaturesForClustering(song_list)

    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(audio_features_scaled)

    # Assign each song to its cluster
    for i, song in enumerate(song_list):
        song.setSongClusterID(clusters[i])

    return clusters

def create_playlist_on_spotify(sp, user_id, playlist_name, song_uris):
    '''Creates a new playlist on Spotify and adds the provided tracks.'''
    # Create a new playlist
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, description="Playlist created by clustering songs based on audio features")
    
    # Split song_uris into chunks of 100
    chunk_size = 100
    song_uris_chunks = [song_uris[i:i + chunk_size] for i in range(0, len(song_uris), chunk_size)]
    
    for chunk in song_uris_chunks:
        # Add each chunk to the playlist
        sp.playlist_add_items(playlist_id=playlist['id'], items=chunk)
    
    return playlist['id']

def create_playlists_by_clusters(sp, user_id, song_list, n_clusters):
    '''Creates playlists on Spotify based on song clusters.'''
    # Cluster the songs
    clusters = clusterTracks(n_clusters, song_list)

    # Create playlists based on the cluster assignments
    for cluster in range(n_clusters):
        # Collect all song URIs for the current cluster
        song_uris = [song.uri for song in song_list if song.cluster == cluster]
        
        if song_uris:
            # Create a unique playlist name for this cluster
            playlist_name = f"Cluster {cluster + 1} Playlist"
            print(f"Creating playlist: {playlist_name} with {len(song_uris)} songs")
            
            # Create the playlist on Spotify
            create_playlist_on_spotify(sp, user_id, playlist_name, song_uris)
        else:
            print(f"No songs found for Cluster {cluster + 1}")

if __name__ == "__main__":
    # Fetch the current user
    user = sp.current_user()
    user_id = user['id']

    # Fetch saved tracks
    all_saved_tracks = fetch_all_saved_tracks(sp)

    # Create Song objects
    songList = []
    for track in all_saved_tracks:  # Change limit as needed
        trackName = track['track']['name']
        trackId = track['track']['id']
        trackUri = track['track']['uri']
        artist = getArtistForTrack(track)
        album = getAlbumForTrack(track)
        audioFeatures = getAudioFeatures(trackId)

        song = Song(trackName, trackId, trackUri, album, artist)
        song.setAudioFeatures(audioFeatures)

        songList.append(song)

    # Cluster songs and create playlists
    n_clusters = 10  # Adjust the number of clusters
    create_playlists_by_clusters(sp, user_id, songList, n_clusters)



