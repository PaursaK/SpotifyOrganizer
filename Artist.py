class Artist:

    def __init__(self, name: str, id: str, genres: list):
        '''simple constructor for artist object to easily manage relevant info about a artist'''
        self.name = name
        self.id = id
        self.genres = genres

    def __str__(self):
        return self.name
