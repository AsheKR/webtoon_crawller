__all__ = (
    'WebtoonData',
    'WebtoonNotExist',
)

class WebtoonData:
    def __init__(self, webtoon_id, title, url_thumbnail):
        self.webtoon_id = webtoon_id
        self.title = title
        self.url_thumbnail = url_thumbnail

    def __repr__(self):
        return self.title


class WebtoonNotExist(Exception):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f'웹툰( 이름: {self.title}을 찾을 수 없습니다.!'
