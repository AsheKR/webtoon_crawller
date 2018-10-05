import requests, re
from bs4 import BeautifulSoup
from data import WebtoonData, Episode

class Crawler:
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

        response = requests.get('https://comic.naver.com/webtoon/weekday.nhn')
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        col_list = soup.select_one('div.list_area.daily_all').select('.col')

        li_list = [
            li
            for col in col_list
            for li in col.select('.col_inner ul > li')
        ]

        webtoon_data_dict = {}

        for li in li_list:
            title = li.select_one('a.title').get_text(strip=True)
            url_thumbnail = li.select_one('.thumb > a > img')['src']
            webtoon_id = re.match(r'.*titleId=(\d+).*', li.select_one('.thumb > a')['href']).group(1)

            if not title in webtoon_data_dict:
                new_webtoon_data = WebtoonData(webtoon_id, title, url_thumbnail)
                webtoon_data_dict[title] = new_webtoon_data

        for key, webtoon_data in webtoon_data_dict.items():
            print(webtoon_data)

if __name__ == '__main__':
    crawler = Crawler()
    crawler.show_webtoon_list()