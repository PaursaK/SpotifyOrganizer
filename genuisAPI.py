import requests
from bs4 import BeautifulSoup

class Genius:


    def get_lyrics(song_title, artist_name):
        base_url = "https://api.genius.com"
        access_token = "OZ0EwugJE2nOqBjEFKHNvVngnChhgXP84jH0gdBN-XTf97Oa9PQ1OJgE5_5kpCim"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Search for the song
        search_url = f"{base_url}/search"
        params = {"q": f"{song_title} {artist_name}"}
        response = requests.get(search_url, headers=headers, params=params)

        # Check if the response is successful
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None

        json_data = response.json()

        # Get the first song result
        if json_data['response']['hits']:
            song_path = json_data['response']['hits'][0]['result']['path']
            lyrics_url = f"https://genius.com{song_path}"  # Genius lyrics are in the webpage
            print(lyrics_url)
            return Genius.scrape_lyrics(lyrics_url)  # You can scrape the page for lyrics
        else:
            print("Song not found.")
            return None
        
    def scrape_lyrics(lyrics_url):
        # Fetch the webpage
        try:
            response = requests.get(lyrics_url)
            
            if response.status_code != 200:
                print(f"Error fetching lyrics: {response.status_code}")
                return None

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the div with lyrics
            lyrics_div = soup.find('div', {'data-lyrics-container': 'true'})

            # Check if lyrics_div is found
            if lyrics_div is None:
                print("Lyrics div not found.")
                return None

            # Extract all text within the div, handling <br> for line breaks
            lyrics = lyrics_div.get_text(separator="\n").strip()

            # Check if lyrics is empty
            if not lyrics:
                print("No lyrics found in the div.")
                return None

            return lyrics

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        

        '''#print(soup)

        # Look for the lyrics within the webpage
        lyrics_div = soup.find("div", class_="lyrics")  # Old Genius layout
        if lyrics_div:
            return lyrics_div.get_text(strip=True)

        # New Genius layout
        lyrics_div = soup.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")
        if lyrics_div:
            return lyrics_div.get_text(separator="\n", strip=True)

        print("Lyrics not found.")
        return None'''


