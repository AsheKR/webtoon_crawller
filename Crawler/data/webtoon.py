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

        1.page값을 1부터 늘려가면서 '다음' 버튼이 안보일때까지 내용을 가져옴
        1.1 이외에 최대의 episode_id를 가져온 후 10으로 나눠서 페이지를 계산하는 방법을 채택함
        2. pickle을 사용해서 Crawler가 가진 webtoon_dict를 저장, 불러오기 하는 방식으로 중복 데이터를 웹에서 받지 않도록 함
        3, CLI를 구성해서 사용자가 셸에서 선택해서 웹툰 크롤러 기능을 사용할 수 있도록 만들기
        4. Episode의 Detail페이지에서 그림을 다운로드 받기
                request로 그림 요청시 Referer 설정을 해줘야함 <- 안하면 403 또는 400 에러 발생
                headers = {'Referer': 'http://comic.naver.com/webtoon/list.nhn?titleId=<WebtoonId>'}
                저장시
                    reponse = requests.get(<URL>)
                    open(<path>, 'wb').write(response.content)
                코드를 사용
        5, 다운로드 받은 그림을 볼 수 있는 HTML 생성하기

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
        return f'웹툰( 이름: {self.title}을 찾을 수 없습니다.!'
