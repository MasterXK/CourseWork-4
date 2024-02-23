import os

import dotenv
import requests

from src.ABCClasses import APIProcessor
from src.VacancyClass import Vacancy

dotenv.load_dotenv()
SJ_KEY = os.getenv("SJ_API_KEY")


class SJProcessor(APIProcessor):
    headers = {"X-Api-App-Id": SJ_KEY}
    params = {"count": 100, "page": 0}

    def get_vacancies(self, keywords: str | list[dict[str, str | int]], salary) -> list[Vacancy]:
        """
        Принимает ключевые слова и зарплату для поиска вакансий.
        Каждому слову соответствует свой параметр srws.
        Массив имеет вид: [{'text': '', 'param': 'srws'}, {...}].
        Параметр srws обозначает критерии поиска ключевого слова keys.
        Значения параметра могут быть:
        srws:
            1 — должность
            2 — название компании
            3 — должностные обязанности
            4 — требования к квалификации
            5 — условия работы
            10 — весь текст вакансии

        Зарплата должна быть представлена массивом из 2 чисел: ['зарплата от', 'зарплата до']

        Функция возвращает до 100 вакансий.

        :param salary: Желаемая зарплата
        :param keywords: Список параметров поиска
        :return: Список вакансий(объектов)
        """

        vacancies = []

        for num_of_vacancy, srch_params in enumerate(keywords):
            if len(srch_params) == 1:
                self.params["keyword"] = srch_params["text"]

            else:
                key = "keywords[%d][keys]" % num_of_vacancy
                self.params[key] = srch_params["text"]
                key = "keywords[%d][srws]" % num_of_vacancy
                self.params[key] = srch_params["param"]
                key = "keywords[%d][skwc]" % num_of_vacancy
                self.params[key] = "or"

        self.params["payment_from"] = salary[0]
        self.params["payment_to"] = salary[1]

        response = requests.get(
            "https://api.superjob.ru/2.0/vacancies",
            params=self.params,
            headers=self.headers,
        ).json()["objects"]

        for vacancy in response:
            vacancies.append(
                Vacancy(
                    name=vacancy["profession"],
                    salary=[vacancy["payment_from"], vacancy["payment_to"]],
                    description=vacancy["candidat"],
                    url=vacancy["link"],
                )
            )

        return vacancies


class HHProcessor(APIProcessor):
    headers = {"HH-User-Agent": "Kursovaya/1.0 (vavilon164@yandex.ru)"}
    params = {"per_page": 100, "page": 0}

    def get_vacancies(self, keywords: list[dict], salary):
        """
        Принимает ключевые слова и зарплату для поиска вакансий.
        Каждому слову соответствует свой параметр поиска search_field
        Массив имеет вид: [{'text': '', 'param': 'search_field'}, {...}],
        либо обычной строкой(тогда фильтр будет по всему тексту вакансии).
        Параметр search_field обозначают критерии поиска ключевого слова keys.
        Значения параметра могут быть:
        search_field:
            name — должность
            company_name — название компании
            description — описание вакансии

        Зарплата должна быть представлена массивом из 2 чисел: ['зарплата от', 'зарплата до']

        Функция возвращает до 100 вакансий.

        :param salary: Желаемая зарплата
        :param keywords: Список параметров поиска
        :return: Список вакансий(объектов)
        """
        vacancies = []
        param_translate = {1: "name", 2: "company_name", 3: "description"}
        salary_from = 0
        salary_to = 0
        self.params["salary"] = round(salary[0] + (salary[1] - salary[0]) / 2)

        for srch_params in keywords:
            if len(srch_params) == 1:
                self.params["text"] = srch_params["text"]

            else:
                self.params["text"] = srch_params["text"]
                self.params["search_field"] = param_translate[srch_params["param"]]

            response = requests.get(
                "https://api.hh.ru/vacancies", params=self.params, headers=self.headers
            )
            vacs = response.json()["items"]

            for vacancy in vacs:
                try:
                    salary_from = vacancy["salary"]["from"]
                    salary_to = vacancy["salary"]["to"]

                except TypeError:
                    pass

                finally:

                    vacancies.append(
                        Vacancy(
                            name=vacancy["name"],
                            salary=[salary_from, salary_to],
                            description=vacancy["snippet"]["responsibility"],
                            url=vacancy["alternate_url"],
                        )
                    )

        return vacancies
