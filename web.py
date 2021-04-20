import requests
import json
import time
import os


# Метод для получения страницы со списком вакансий
def getPage(page=0):
    # Справочник для параметров GET-запроса
    params = {
        'text': 'NAME:Аналитик',  # Текст фильтра.
        'area': 2,  # Поиск ощуществляется по вакансиям города Санкт-Петербург
        'page': page,  # Индекс страницы поиска на HH
        'per_page': 5  # Кол-во вакансий на 1 странице
    }

    req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
    response = req.json()
    return response



def parseJobs(data):
    for i in range(5):
        job_salary = data["items"][i]["salary"]["from"]
        job_name = data["items"][i]["name"]
        job_city = data["items"][i]["address"]["city"]
        job_accept_kids = data["items"][i]["accept_kids"]
        job_published_at = data["items"][i]["published_at"]
        print(data["items"][0]["salary"]["from"])


#Считываем первые 20 вакансий
# for page in range(0, 4):
#     print(parseJobs(getPage(0)))
#     # Преобразуем текст ответа запроса в словарь Python
#     jsObj = json.loads(getPage(page))
#     time.sleep(0.25)
