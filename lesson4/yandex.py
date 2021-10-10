import json
from datetime import datetime, timedelta

import requests
from lxml import html

from lesson4.news_repository import NewsRepository


def main():
    url = 'https://yandex.ru/news/'
    with open('../lesson2/headers.json', 'r', encoding='utf-8') as headers_source:
        headers = json.load(headers_source)
    repository = NewsRepository()
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news = dom.xpath('//article')
    for n in news:
        name = None
        source = None
        link = None
        date = None
        try:
            name = n.xpath('.//h2[@class="mg-card__title"]/text()')[0].replace('\xa0', ' ')
            source = n.xpath('.//a[@class="mg-card__source-link"]/text()')[0]
            link = n.xpath('.//a[@class="mg-card__link"]/@href')[0]
            date = get_date(n.xpath('.//span[@class="mg-card-source__time"]/text()')[0])
            repository.save_one_news({
                '_id': link,
                'name': name,
                'source': source,
                'date': date
            })
        except Exception as e:
            print(f'something went wrong with {[name, source, link, date]}, {e}')
            raise e

    print(repository.news_count())
    for i in repository.find_all():
        print(i)


def get_date(text: str):
    months = {'январ': 1, 'феврал': 2, 'март': 3, 'апрел': 4, 'май': 5, 'июн': 6, 'июл': 7, 'август': 8,
              'сентябр': 9, 'октябр': 10, 'ноябр': 11, 'декабр': 12}

    try:
        split_text = text.split(' ')
        if len(split_text) == 1:  # только время (15:55)
            time = text.split(':')
            return datetime.today().replace(hour=int(time[0]), minute=int(time[1]))
        elif len(split_text) == 3:  # вчера (вчера в 15:55)
            time = split_text[-1].split(':')
            date = datetime.today() - timedelta(days=1)
            return date.replace(hour=int(time[0]), minute=int(time[1]))
        else:  # для даты и времени (5 октября в 22:02)
            time = split_text[-1].split(':')
            date_string = f'{split_text[0]}/{months[split_text[1][:-1]]}/2021-{time[0]}:{time[1]}'
            return datetime.strptime(date_string, '%d/%m/%Y-%H:%M')
    except Exception as e:
        print(f'something went wrong, when parse {text} to date, {e}')


if __name__ == '__main__':
    main()
