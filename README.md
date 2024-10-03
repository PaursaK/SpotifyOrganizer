# Spotify Playlist Organizer

This project organizes your saved Spotify tracks into distinct playlists based on their audio features, using machine learning clustering algorithms. It uses Spotify's Web API to fetch your liked tracks, extracts their audio features (like danceability, energy, tempo, etc.), and clusters them into user-defined playlists.

## Features
- **Fetch Saved Tracks**: Retrieve all saved tracks from your Spotify account.
- **Cluster Songs**: Cluster the tracks based on audio features using KMeans clustering.
- **Create Playlists**: Automatically create playlists on your Spotify account for each cluster.

## Table of Contents
- [Installation](#installation)
- [Authentication Setup](#authentication-setup)
- [Usage](#usage)
- [Customization](#customization)
- [Improvements](#improvements)
## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/PaursaK/SpotifyOrganizer.git
    ```

2. Navigate to the project directory:

    ```bash
    cd SpotifyOrganizer
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Authentication Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create a new application.  
   
2. Set the **Redirect URI** to `http://localhost:3000` or any other valid URL, and copy the **Client ID** and **Client Secret**.

3. In the project code, replace the placeholders in the `SpotifyOAuth` setup with your own **Client ID**, **Client Secret**, and **Redirect URI**:

    ```python
    auth_manager = SpotifyOAuth(
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SECRET",
        redirect_uri="http://localhost:3000",
        scope="user-library-read playlist-modify-public"
    )
    ```

4. Ensure the proper OAuth scopes are defined:
    - `user-library-read` to read your saved tracks.
    - `playlist-modify-public` to create playlists in your Spotify account.

## Usage

To run the script and organize your tracks into playlists:

1. Run the main script:

    ```bash
    python main.py
    ```

2. The script will:
   - Fetch your liked songs from Spotify.
   - Extract their audio features.
   - Cluster them using KMeans.
   - Create separate playlists on your Spotify account based on the clusters.

## Customization

### Adjusting the Number of Clusters
You can modify the number of clusters (playlists) created by changing the value of `n_clusters` in the script:

```python
n_clusters = 10  # Adjust the number of clusters here
```

## Improvements

To enhance the accuracy of curated playlists in this project, consider the following strategies:

1. **Increase the Number of Clusters:** 
   - Experiment with higher values of `n_clusters` to capture finer distinctions among songs.

2. **Feature Selection:**
   - Include additional audio features that correlate with genre, such as tempo, danceability, energy, acousticness, loudness, and valence.
   - Integrate genre metadata if available.

3. **Use Genre Data for Clustering:**
   - Incorporate genre labels into your clustering approach through one-hot encoding or weighted clustering.

By implementing these strategies, you can may be able to improve the genre accuracy of the curated playlists based similar attributes.