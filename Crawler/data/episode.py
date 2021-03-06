import re, requests, os, webbrowser
from bs4 import BeautifulSoup


def atoi(text):
    """
    입력받은 것이 문자면 숫자로, 숫자면 그대로 리턴해준다.

    :param text:
    :return:
    """
    return int(text) if text.isdigit() else text


def natural_keys(text):
    """
    content_image_{에피소드 회차}.jpg
    이같은 형식에서 에피소드 회차, 즉 숫자인 부분을 뽑는 함수

    :param text:
    :return:
    """
    return [atoi(c) for c in re.split('(\d+)', text)]


class Episode:
    def __init__(self, epsiode_id, title, url_thumbnail, created_date, rating):
        self.episode_id = epsiode_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self.created_date = created_date
        self.rating = rating

    def __repr__(self):
        return self.title

    def create_html(self, title, img_dir_path):
        """
        /save_data/webtoon_data/{웹툰 이름}/{에피소드 회차}
        이 안에 html 파일을 생성하는 코드

        :param title: 웹툰 이름
        :param img_dir_path: 웹툰의 해당 에피소드가 저장되는 디렉터리
        :return:
        """
        html_str = f"<h1>{title}</h1>"
        img_file_path = os.path.join(img_dir_path, title + " " + self.episode_id + ".html")

        if not os.path.exists(img_file_path):
            file_list = os.listdir(img_dir_path)
            file_list.sort(key=natural_keys)

            for src in file_list:
                html_str += f'<img src="{src}">'

            with open(img_file_path, 'wt') as f:
                f.write(html_str)

        webbrowser.get(using="google-chrome").open(img_file_path, new=2)

    def download_imgs(self, webtoon_id, img_dir_path):
        """
        특정 웹툰, 에피소드에서 jpg 파일을 가져와 저장한다.

        :param webtoon_id: img 파일을 요청할 때 url에 사용되는 웹툰 고유 ID
        :param img_dir_path: 이미지들이 저장될 디렉터리
        :return:
        """
        url = f"http://comic.naver.com/webtoon/detail.nhn?titleId={webtoon_id}&no={self.episode_id}"
        headers = {'Referer': url}

        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        imgs = soup.select('#container > #content #comic_view_area > .wt_viewer > img')

        for img in imgs:
            img_url = img['src']
            img_file_path = os.path.join(img_dir_path, img['id'] + ".jpg")

            if os.path.exists(img_file_path):
                continue

            print(img)
            response = requests.get(img_url, stream=True, headers=headers)
            with open(img_file_path, 'wb') as f:
                f.write(response.content)

    # 생성자처럼 동작하게 하는 것
    @classmethod
    def create_from_soup(cls, soup):
        """

        받는 soup Selector: table.viewList tr[class="None"]
        :param soup: BeautifulSoup 객체 또는 BeautifulSoup 객체에서
                    'select', 'find'등의 메서드를 사용해 리턴된 TAG 객체
        :return: Episode 인스턴
        """

        episode_id = re.search(r'no=(\d+)', soup.select('td')[0].select_one('a')['href']).group(1)

        title = soup.select_one('td.title > a').get_text(strip=True)
        url_img_thumbnail = soup('td')[0].select_one('a > img')['src']
        rating = soup.select_one('td div.rating_type strong').get_text(strip=True)
        created_date = soup.select_one('td.num').get_text(strip=True)

        new_episode_data = Episode(episode_id, title, url_img_thumbnail, created_date, rating)

        return new_episode_data


# 현재는 쓰이지 않지만 class=None을 검사하지 않았을 때 사용하게되것이다.
class EpisodeCreateError(Exception):
    def __init__(self, episode_id):
        self.episode_id = episode_id

    def __str__(self):
        return f'HTML로부터 Episode를 생성하는데 실패했습니다. (episode_id: {self.episode_id})'
