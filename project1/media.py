import webbrowser


'''
This file contains the constructor __init__ that creates a Movie object
that represents a movie. It holds information such as title,
storyline, poster url, and trailer url.
It includes one method, show_trailer(), that opens a
browser using the given trailer url.
'''


class Movie():
    VALID_RATINGS = ["G", "PG", "PG-13", "R"]

    def __init__(self, movie_title, movie_storyline,
                 poster_image, trailer_youtube):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
