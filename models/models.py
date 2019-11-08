class Movie:
    def __init__(self,title,year):
        self.title=title
        self.year=year

    def __str__(self):
        return '<Movie {}>'.format(self.title)
