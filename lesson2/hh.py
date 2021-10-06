"""
Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
Сохраните в json либо csv.
"""
import json

import requests
from bs4 import BeautifulSoup as bs

from lesson3.professions_repository import ProfessionRepository


def main():
    profession = input('Какую профессию будем искать?(транслит): ')
    end_page = int(input('Сколько нужно страниц?: '))
    find_and_save_jobs(end_page, profession)

    min_salary = input('Введите минимальную сумму или любую букву для выхода: ')
    if min_salary.isdigit():
        for j in ProfessionRepository().find_job_by_min_salary('programmist', int(min_salary)):
            print(j)
    print('*** Конец ***')


def find_and_save_jobs(end_page, profession):
    base_url = 'https://hh.ru'
    url = base_url + '/vacancies/' + profession
    repository = ProfessionRepository()
    with open('headers.json', 'r', encoding='utf-8') as headers_source:
        headers = json.load(headers_source)
    while url:
        page = url.split('=').pop()
        page = int(page) + 1 if page.isdigit() else 1

        response = requests.get(url, headers=headers)
        print(f'Получил ответ от hh.ru. Код: {response.status_code}. Загружена страница {page}')

        dom = bs(response.text, 'html.parser')
        jobs = dom.find_all('div', attrs={'class': 'vacancy-serp-item'})

        for job in jobs:
            job_info = get_job_info(job)
            repository.save_one_job(profession, job_info)

        if page >= end_page:
            break

        next_button = dom.find('a', attrs={'data-qa': 'pager-next'})

        if next_button:
            url = base_url + next_button['href']
        else:
            url = None
    print(f'Загружено {repository.jobs_count(profession)} записей')


def get_job_info(job):
    job_a = job.find('span', attrs={'class': 'g-user-content'}).find('a')
    job_link = job_a['href']
    job_name = job_a.text

    job_salary_span = job.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    min_salary, max_salary, currency = get_salary_values(job_salary_span)

    job_owner = job.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}) \
        .get_text() \
        .replace('\xa0', ' ')

    return {
        '_id': job_link,
        'name': job_name,
        'link': job_link,
        'min_salary': min_salary,
        'max_salary': max_salary,
        'currency': currency,
        'owner': job_owner
    }


def get_salary_values(job_salary_span):
    min_salary = None
    max_salary = None
    currency = None
    if job_salary_span:
        job_salary_span_text = job_salary_span.get_text()
        if job_salary_span_text.startswith('от'):
            min_salary = int(job_salary_span_text[3:-5].replace('\u202f', ''))
        elif job_salary_span_text.startswith('до'):
            max_salary = int(job_salary_span_text[3:-5].replace('\u202f', ''))
        else:
            min_salary, max_salary = map(lambda x: int(x.replace('\u202f', '')),
                                         job_salary_span_text[:-5].split('–'))
        currency = job_salary_span.text[-4:-1]
    return [min_salary, max_salary, currency]


if __name__ == '__main__':
    main()
