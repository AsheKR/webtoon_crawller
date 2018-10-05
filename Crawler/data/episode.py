class Episode:
    def __init__(self, epsiode_id, title, url_thumbnail, created_date, rating):
        self.episode_id = epsiode_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self.created_date = created_date
        self.rating = rating

    def __repr__(self):
        return self.title