import requests
import json
import time
import os
from functions import iter_time
import datetime


# Метод для получения страницы со списком вакансий
def getPage(vacancy, page=0):
    # Справочник для параметров GET-запроса
    params = {
        'text': f'NAME:{vacancy}',  # Текст фильтра.
        'area': 2,  # Поиск ощуществляется по вакансиям города Санкт-Петербург
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 5  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    response = req.json()
    return response


# Метод парсит json и представляет данные в виде списка словарей
def parseJobs(data, salary):
    jobs = []
    used_id = []
    for i in range(5):
        print(data)
        try:
            job_salary = data["items"][i]["salary"]["from"]
            job_name = data["items"][i]["name"]
            job_city = data["items"][i]["address"]["city"]
            job_published_at = data["items"][i]["published_at"]
            url = data["items"][i]["alternate_url"]
            id = data["items"][i]["id"]
            if job_salary < salary or job_salary > salary:
                continue
            if id in used_id:
                continue
            else:
                used_id.append(id)
            if compareTime(job_published_at, str(datetime.datetime.now())):
                jobs.append({"name": job_name, "salary": job_salary, "city": job_city, "published_at": job_published_at,
                             "url": url})
        except TypeError as te:
            continue
    return jobs


def compareTime(published_time, now_time):
    published_date = published_time.split('T')[0]
    published_time = published_time.split('T')[1].split('+')[0]
    published_date = published_date.split('-')
    published_time = published_time.split(':')
    now_date = now_time.split()[0]
    now_date = now_date.split('-')
    now_time = now_time.split()[1].split('.')[0]
    if now_time[0] - published_date[0] < iter_time / 60:
        if now_time[1] - published_date[1] < iter_time:
            return True
    return False


def getJobs(vacancy, salary, pages=0):
    return parseJobs(getPage(vacancy, pages), salary)

# Считываем первые 20 вакансий
# for page in range(0, 4):
#     print(parseJobs(getPage(0)))
#     # Преобразуем текст ответа запроса в словарь Python
#     jsObj = json.loads(getPage(page))
#     time.sleep(0.25)
