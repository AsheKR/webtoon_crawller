import re
from collections import OrderedDict

import requests
from bs4 import BeautifulSoup

from data import Episode

__all__ = (
    'WebtoonData',
    'WebtoonNotExist',
)


class WebtoonData:
    def __init__(self, webtoon_id, title, url_thumbnail):
        self.webtoon_id = webtoon_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self._episode_dict = OrderedDict()

    def __repr__(self):
        return self.title

    @property
    def url(self):
        return f'https://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon_id}'

    @property
    def episode_dict(self):
        """
        자신의 _episode_dict가 있다면 그대로 리턴
        아니라면 채워준다.
        주소는 (에피소드 리스트 URL)
            https://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon_id}

        키는 Episode의 episode_id
            에피소드 상세 URL에서 'no' GET parameter값에 해당

        webtoon_dict를 채울때와 비슷하게, 새로운 Episode클래스 인스턴스르 만들어 할당

        page값을 1부터 늘려가면서 '다음' 버튼이 안보일때까지 내용을 가져옴

        :return:
        """
        if not self._episode_dict:
            response = requests.get(self.url)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            episode_list = list(filter(lambda e: e.get('class') == None, soup.select('div#content > table.viewList tr')[1:]))

            for one_episode in episode_list:
                episode_id = re.search(r'no=(\d+)', one_episode.select('td')[0].select_one('a')['href']).group(1)

                if episode_id not in self._episode_dict:
                    title = one_episode.select_one('td.title > a').get_text(strip=True)
                    url_img_thumbnail = one_episode('td')[0].select_one('a > img')['src']
                    rating = one_episode.select_one('td div.rating_type strong').get_text(strip=True)
                    created_date = one_episode.select_one('td.num').get_text(strip=True)

                    new_episode_data = Episode(episode_id, title, url_img_thumbnail, created_date, rating)
                    self._episode_dict[episode_id] = new_episode_data

        return self._episode_dict

    def get_episode(self, index):
        """
        Index번째에 해당하는 에피소드를 자신의 episode_dict프로퍼티를 사용해서 리턴
        :return:
        """
        return self.episode_dict[index]


class WebtoonNotExist(Exception):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f'웹툰( 이름: {self.title}을 찾을 수 없습니다.!'
