import requests, re
from bs4 import BeautifulSoup
from data import WebtoonData, Episode, WebtoonNotExist

import os


class Crawler:
    def __init__(self):
        self._webtoon_dict = {}

    def get_webtoon(self, title):
        """
        title이 제목인 Webtoon 객체를 가져옴


        :param title:
        :return:
        """
        try:
            return self.webtoon_dict[title]
        except KeyError:
            raise WebtoonNotExist(title)

    @property
    def webtoon_dict(self):
        if not self._webtoon_dict:
            # 실제 HTTP 요청을 매번 할 필요가 없음 (파일로 저장해두고 필요할 때 갱신하는 기능이 필요)
            html = self.get_html()
            soup = BeautifulSoup(html, 'lxml')
            col_list = soup.select_one('div.list_area.daily_all').select('.col')

            li_list = [
                li
                for col in col_list
                for li in col.select('.col_inner ul > li')
            ]

            self._webtoon_dict = {}

            for li in li_list:
                title = li.select_one('a.title').get_text(strip=True)
                url_thumbnail = li.select_one('.thumb > a > img')['src']
                webtoon_id = re.match(r'.*titleId=(\d+).*', li.select_one('.thumb > a')['href']).group(1)

                if not title in self._webtoon_dict:
                    new_webtoon_data = WebtoonData(webtoon_id, title, url_thumbnail)
                    self._webtoon_dict[title] = new_webtoon_data

        return self._webtoon_dict

    def get_html(self):
        """
        전체 웹툰 목록의 HTML을 리턴한다.
        만약에 파일이 존재한다면, 해당 내용을 읽어온다.
        파일로 저장되어있지 않는다면, requests를 사용해 웹에서 받아와 리턴해준다.

        파일위치 및 명은 ./saved_data/weekday.html

        :return: html 문자열
        """

        dirname = 'save_data'
        filename = 'weekday.html'

        cur_path = os.path.dirname(os.path.abspath(__file__))
        saved_path = os.path.join(cur_path, dirname)
        saved_file = os.path.join(saved_path, filename)

        # 폴더가 없으면 생성
        if not os.path.isdir(saved_path):
            print("**폴더 생성**")
            print(saved_path)
            os.mkdir(saved_path)

        # 파일이 없으면 생성
        if not os.path.exists(saved_file):
            print("**파일 생성**")
            print(saved_file)
            try:
                response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
            except:
                print("해당 페이지를 가져오는데 실패하였습니다.!!")
            else:
                open(saved_file, 'wt').write(response.text)

        html = open(saved_file, 'rt').read()
        return html

    def show_webtoon_list(self):
        """
        전체 웹툰 제목을 출력해줌

        1. requests를 사용해서 웹툰 목록 URL을 가져옴
        2. BeautifulSoup을 사용해서 가져온 HTML 데이터를 파싱
        3. 파싱한 결과를 사용해서 Webtoon클래스 인스턴스들을 생성
        4. 생성한 인스턴스 목록을 DICT에 제목을 KEY를 사용해서 할당
        5. dict를 순회하며 제목들을 출력


        crawler = Cralwer()
        crawler.show_webtoon_list()
        :return:
        """

        for key, webtoon_data in self.webtoon_dict.items():
            print(webtoon_data)


if __name__ == '__main__':
    crawler = Crawler()
    print(crawler.get_webtoon('호곡'))
