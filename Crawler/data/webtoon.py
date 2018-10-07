import re
from collections import OrderedDict

import requests, os
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

        :return:
        """
        page = 1
        if not self._episode_dict:
            while True:
                soup = self.get_episode_page(page)
                page += 1

                episode_list = list(
                    filter(lambda e: e.get('class') is None, soup.select('div#content > table.viewList tr')[1:]))

                for one_episode in episode_list:
                    new_episode_data = Episode.create_from_soup(one_episode)
                    self._episode_dict[new_episode_data.episode_id] = new_episode_data

                if soup.select_one('div.paginate > div.page_wrap > a.next') is None:
                    break

        return self._episode_dict

    def save_imgFiles(self, index):
        """
        해당 웹툰의 특정 에피소드의 이미지를 받아 저장한다.
        /save_data/webtoon_data/{웹툰 이름}/{에피소드 회차}
        위처럼 기본적인 뼈대 폴더를 생성하는 일을 한다.

        :param index: 특정 에피소드
        :return:
        """
        now_episode = self.episode_dict[index]
        dirname = 'save_data'
        title_dirname = self.title
        episode_dirname = now_episode.episode_id

        cur_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        saved_path = os.path.join(cur_path, dirname, 'webtoon_data', title_dirname, episode_dirname)

        print(saved_path)

        if not os.path.isdir(saved_path):
            print("디렉터리 생성")
            os.makedirs(saved_path)

        now_episode.download_imgs(self.webtoon_id, saved_path)
        now_episode.create_html(self.title, saved_path)

    def get_episode(self, index):
        """
        Index번째에 해당하는 에피소드를 자신의 episode_dict프로퍼티를 사용해서 리턴
        :return:
        """
        return self.episode_dict[index]

    def get_episode_page(self, page):
        """
        해당 페이지를 가져옴
        :param page:
        :return:
        """
        url = self.url + f"&page={page}"

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        return soup


class WebtoonNotExist(Exception):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f'웹툰( 이름: {self.title}을 찾을 수 없습니다! )'
