import requests
import json
import time
import os


# Метод для получения страницы со списком вакансий
def getPage(page=0):
    # Справочник для параметров GET-запроса
    params = {
        'text': 'NAME:Аналитик',  # Текст фильтра. В имени должно быть слово "Аналитик"
        'area': 2,  # Поиск ощуществляется по вакансиям города Санкт-Петербург
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 5  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    data = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


# def parseJobs(data):
#     job_salary = data["salary"]["from"]
#     job_name = data["name"]
#     job_city = data["address"]["city"]
#     job_accept_kids = data["accept_kids"]
#     job_published_at = data["published_at"]

# Считываем первые 20 вакансий
for page in range(0, 4):
    # Преобразуем текст ответа запроса в словарь Python
    jsObj = json.loads(getPage(page))
    time.sleep(0.25)
