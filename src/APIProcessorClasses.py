from src.ABCClasses import APIProcessor
from src.VacancyClass import Vacancy
import dotenv
import os
import requests


dotenv.load_dotenv()
SJ_KEY = os.getenv('SJ_API_KEY')


class SJProcessor(APIProcessor):
    headers = {'X-Api-App-Id': SJ_KEY}
    params = {'count': 10, 'page': 0}

    def get_vacancies(self, keywords: str | list[dict[str, str | int]]):
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

        Функция возвращает 10 вакансий.
        :param keywords: Список параметров поиска
        :return: Список вакансий(объектов)
        """

        vacancies = []

        for num_of_vacancy, srch_params in enumerate(keywords):
            if len(srch_params) == 1:
                self.params['keyword'] = srch_params['text']

            else:
                key = 'keywords[%d][keys]' % num_of_vacancy
                self.params[key] = srch_params['text']
                key = 'keywords[%d][srws]' % num_of_vacancy
                self.params[key] = srch_params['param']
                key = 'keywords[%d][skwc]' % num_of_vacancy
                self.params[key] = 'or'

        response = requests.get('https://api.superjob.ru/2.0/vacancies',
                                params=self.params, headers=self.headers).json()['objects']

        for vacancy in response:
            vacancies.append(Vacancy(name=vacancy['profession'],
                                     salary=[vacancy['payment_from'], vacancy['payment_to']],
                                     description=vacancy['candidat'],
                                     url=vacancy['link']))

        return vacancies


class HHProcessor(APIProcessor):
    headers = {'HH-User-Agent': 'Kursovaya/1.0 (vavilon164@yandex.ru)'}
    params = {'per_page': 10, 'page': 0}

    def get_vacancies(self, keywords: list[dict]):
        """
        keywords = {'text': '', search_field': 'name/company_name/description', 'salary': int}
        :param keywords:
        :return:
        """
        vacancies = []
        param_translate = {1: 'name', 2: 'company_name', 3: 'description'}
        salary_from = 0
        salary_to = 0

        for srch_params in keywords:
            if len(srch_params) == 1:
                self.params['text'] = srch_params['text']
            else:
                self.params['text'] = srch_params['text']
                self.params['search_field'] = param_translate[srch_params['param']]

            response = requests.get('https://api.hh.ru/vacancies',
                                    params=self.params, headers=self.headers).json()['items']

            for vacancy in response:
                try:
                    salary_from = vacancy['salary']['from']
                    salary_to = vacancy['salary']['to']

                except TypeError:
                    pass

                finally:

                    vacancies.append(Vacancy(name=vacancy['name'],
                                             salary=[salary_from, salary_to],
                                             description=vacancy['snippet']['responsibility'],
                                             url=vacancy['url']))

        return vacancies
