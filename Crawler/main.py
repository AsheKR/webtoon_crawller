from crawler import Crawler
from data import WebtoonNotExist

if __name__ == '__main__':
    c = Crawler()

    before_choice_list = '>>1. 웹툰 목록 가져오기\n>>2. 웹툰 선택\n>>9. 웹툰 목록 갱신\n>>0. 종료하기'
    after_choice_list = '\n>>1. 웹툰 목록 가져오기\n>>2. 웹툰 재선택\n>>3. 웹툰 회차 선택\n>>0. 종료하기'
    webtoon_choice =""

    while True:
        if webtoon_choice:
            print('선택된 웹툰 : ', webtoon_choice, after_choice_list)
        else:
            print(before_choice_list)

        choice = input('입력 > ')

        if choice == "1":
            c.show_webtoon_list()
        elif choice == "2":
            webtoon_choice = input("웹툰 이름을 입력 > ")
            try:
                c.get_webtoon(webtoon_choice)
            except WebtoonNotExist as e:
                print(e)
                continue
        elif choice == '3':
            if not webtoon_choice:
                print("우선 웹툰 선택부터 해주세요.")
                continue

            for key, title in c.get_webtoon(webtoon_choice).episode_dict.items():
                print(f'{key}: {title}')

            episode_choice = input("회차를 입력 > ")
            c.get_webtoon(webtoon_choice).save_imgFiles(episode_choice)

        elif choice == '9':
            print('갱신합니다.')
            c.save_webtoon_dict()
            continue

        elif choice == '0':
            print('종료합니다.')
            break
        else:
            print('그런 선택지는 없습니다.')
            continue

