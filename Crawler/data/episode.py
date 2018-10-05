import re


class Episode:
    def __init__(self, epsiode_id, title, url_thumbnail, created_date, rating):
        self.episode_id = epsiode_id
        self.title = title
        self.url_thumbnail = url_thumbnail
        self.created_date = created_date
        self.rating = rating

    def __repr__(self):
        return self.title

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