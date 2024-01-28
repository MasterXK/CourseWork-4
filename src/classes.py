from src.abc_classes import APIProcessor
import os
import requests
import dotenv

dotenv.load_dotenv()
SJ_KEY = os.getenv('SJ_API_KEY')


class Vacancy:
    def __init__(self, name, salary: list[int, int], description, url):
        self.name = name
        self.salary = salary
        self.description = description
        self.url = url

    def __gt__(self, other):
        pass

    def __lt__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __le__(self, other):
        pass


class SJP(APIProcessor):
    headers = {'X-Api-App-Id': SJ_KEY}
    params = {}

    def get_vacancies(self, keywords):
        """
        Принимает ключевые слова для поиска вакансий. Ключевые слова должны быть переданы в виде
        [{'keys': '', 'srws': '', 'skwc': ''}, {...}],
        либо обычной строкой(тогда фильтр будет по всему тексту вакансии).
        Параметры srws и skwc обозначают критерии поиска ключевого слова keys.
        Значения параметров могут быть:
        srws:
            1 — должность
            2 — название компании
            3 — должностные обязанности
            4 — требования к квалификации
            5 — условия работы
            10 — весь текст вакансии
        skwc:
            and — все слова
            or — хотя бы одно слово
            particular — точную фразу
            nein — слова-исключения

        :param keywords: Список параметров поиска
        :return: Список вакансий(объектов)
        """

        vacancies = []

        if type(keywords) is str:
            self.params['keyword'] = keywords

        else:
            for num_of_vacancy, srch_params in enumerate(keywords):
                key = 'keywords[%d][keys]' % num_of_vacancy
                self.params[key] = srch_params['keys']
                key = 'keywords[%d][srws]' % num_of_vacancy
                self.params[key] = srch_params['srws']
                key = 'keywords[%d][skwc]' % num_of_vacancy
                self.params[key] = srch_params['skwc']

        response = requests.get('https://api.superjob.ru/2.0/vacancies',
                                params=self.params, headrs=self.headers).json()['objects']


