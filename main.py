import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Song import Song
from Album import Album
from Artist import Artist
from genuisAPI import Genius
import openai
import time
import json
import networkx as nx
import matplotlib.pyplot as plt

#user authetication
auth_manager = SpotifyOAuth(
    client_id="4d75e005236345d7b7735c7d92a35f71",
    client_secret="66ae8fc0a84845bfaf94a74af0a5299d",
    redirect_uri="http://localhost:3000",
    scope="user-library-read playlist-modify-public"
)

#openai api key
openai.api_key = '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'


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


# Example usage
#Genius.get_lyrics("Shape of You", "Ed Sheeran")

def call_openai_api(prompt: str) -> str:
    """Helper function to call the OpenAI API."""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message['content']
    except openai.error.RateLimitError:
        print("Rate limit exceeded. Retrying in 10 seconds...")
        time.sleep(10)  # Wait before retrying
        return call_openai_api(prompt)  # Retry the function

def analyze_lyrics(lyrics: str) -> list:
    """Function to prompt GPT to analyze the mood of provided lyrics."""
    prompt = f"Analyze the mood of these lyrics, if there is nothing to analyze return an empty string: {lyrics}"
    content = call_openai_api(prompt)

    if content == "":
        return None
    return getMoodTags(content)

def getMoodTags(moodAnalysis: str) -> list:
    """Function to prompt GPT to get mood tags for given mood analysis."""
    prompt = f"Provide 3 simple/generic one-word mood tags listed on one line separated by a comma based on the following mood analysis of a song, if you cannot create mood tags return an empty string and nothing else: {moodAnalysis}"
    moodString = call_openai_api(prompt)

    # Format moods to be in a list
    moodList = [mood.strip() for mood in moodString.split(",") if mood.strip() and mood.strip() != '']
    return moodList

def organizeSongs(json:str):
    """Function to prompt GPT to analyze the mood of provided lyrics."""
    
    prompt = f" XXXXXX return only return a json no extra characters because I need this be properly formatted for the json.load function: {json}"
    content = call_openai_api(prompt)
    return content

def build_song_graph(song_list, attribute="genre"):
    """
    Function to build a graph where songs are connected if they share genres.

    :param song_list: List of Song objects with 'name' and 'genres' attributes.
    :return: A NetworkX graph object.
    """
    # Initialize an empty graph
    song_graph = nx.Graph()

    # Add edges between songs that share genres
    for song in song_list:
        song_name = song.name
        genres = song.genres
        mood = song.mood

        for other_song in song_list:
            if song_name != other_song.name:  # Avoid self-connections
                other_genres = other_song.genres
                other_mood = other_song.mood
                # Add an edge if they share any genre

                if attribute == "genre":
                    if set(genres) & set(other_genres):
                        song_graph.add_edge(song_name, other_song.name)
                elif attribute == "mood":
                    if set(mood) & set(other_mood):
                        song_graph.add_edge(song_name, other_song.name)


    return song_graph




#how to create playlists on the users profile (uncomment when ready to upload)
'''user = sp.current_user()
print(user)
sp.user_playlist_create(user="pkamalian98", name="test-playlist", description="just testing")
sp.playlist_add_items()'''


# Fetch all saved tracks
all_saved_tracks = fetch_all_saved_tracks(sp)

songList = []

# Print out track names and artists
count = 1
#print(all_saved_tracks)
for track in all_saved_tracks[:50]:
    #print(f"Track: {track['track']['name']} by {track['track']['artists'][0]['id']} from {track['track']['album']['id']}")

    trackName = track['track']['name']
    trackId = track['track']['id']
    artist = getArtistForTrack(track)
    album = getAlbumForTrack(track)
    song = Song(trackName, trackId, album, artist)
    print(song)
    lyrics = Genius.get_lyrics(song.name, song.artist.name)
    mood = analyze_lyrics(lyrics)
    song.setMood(mood)
    song.setLyrics(lyrics)
    print(song.mood)

    #add song to a list
    songList.append(song)
    print("-----------------------------------------------------------------------------")

#songList = [song.to_dict() for song in songList]
#print(songList)

# Example of how to use the function and visualize the graph
#song_graph_mood = build_song_graph(songList, attribute="mood")
# Example of how to use the function and visualize the graph
song_graph_genre = build_song_graph(songList, attribute="genre")

# Draw and show the graph
#nx.draw(song_graph_mood, with_labels=True)
#plt.show()

# Draw and show the graph
nx.draw(song_graph_genre, with_labels=True)
plt.show()


'''# Load the organized JSON response
jsonReponse = organizeSongs(songList)
print(jsonReponse)
try:
    jsonLoaded = json.loads(jsonReponse)
    #print(jsonLoaded)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")

#now I am able to access all my liked songs'''



