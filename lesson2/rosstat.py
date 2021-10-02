"""
Необходимо собрать информацию по продуктам питания с сайта:
Список протестированных продуктов на сайте Росконтроль.рф
Приложение должно анализировать несколько страниц сайта (вводим через input или аргументы).
Получившийся список должен содержать:

Наименование продукта.
Все параметры (Безопасность, Натуральность, Пищевая ценность, Качество) Не забываем преобразовать к цифрам
Общую оценку
Сайт, откуда получена информация.
Общий результат можно вывести с помощью dataFrame через Pandas. Сохраните в json либо csv.
"""
import json

import pandas
import requests
from bs4 import BeautifulSoup as bs


def main():
    host = 'https://roscontrol.com'
    base_url = host + '/category/produkti'
    product_kind = '/molochnie_produkti'
    product_type = '/siri'
    end_page = int(input('Сколько нужно страниц?: '))

    url = base_url + product_kind + product_type

    with open('headers.json', 'r', encoding='utf-8') as headers_source:
        headers = json.load(headers_source)

    products_info = pandas.DataFrame(columns=[
        'name',
        'safety',
        'naturalness',
        'nutrition_value',
        'quality',
        'total_score'
    ])
    while url:
        page = url.split('=').pop()
        page = int(page) if page.isdigit() else 1

        response = requests.get(url, headers=headers)
        print(f'Получил ответ от roscontrol.ru. Код: {response.status_code}. Загружена страница {page}')

        dom = bs(response.text, 'html.parser')
        products_links = dom.find_all('a', attrs={'class': 'block-product-catalog__item'})

        for product_link in products_links:
            product_response = requests.get(host + product_link['href'])
            product_info = get_product_info(bs(product_response.text, 'html.parser'))
            products_info = pandas.concat([products_info, product_info])

        if page >= end_page:
            break

        try:
            url = host + dom.select('a.page-num.page-item.last')[0]['href']
        except:
            url = None

    products_info.index = range(1, len(products_info) + 1)
    products_info.to_excel('products.xlsx')
    print(f'{len(products_info)} записей успешно сохранены в products.xlsx')


def get_product_info(dom):
    name = dom.find('h1', attrs={'class': 'main-title'}).get_text()
    try:
        safety, naturalness, nutrition_value, quality = \
            [int(i.get_text())
             for i in dom.find('div', attrs={'id': 'product__single-rev-rate'}).findChildren()
             if i.get_text().isdigit()]
    except:
        safety = naturalness = nutrition_value = quality = None

    try:
        total_score = [int(i.get_text())
                       for i in dom.find('div', id='product__single-rev-total').findChildren()
                       if i.get_text().isdigit()][0]
    except:
        total_score = None

    return pandas.DataFrame(data={
        'name': [name],
        'safety': [safety],
        'naturalness': [naturalness],
        'nutrition_value': [nutrition_value],
        'quality': [quality],
        'total_score': [total_score]
    })


if __name__ == '__main__':
    main()
