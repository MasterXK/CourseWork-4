from abc import ABC, abstractmethod
import os
import requests
import dotenv
import json

dotenv.load_dotenv()
SJ_KEY = os.getenv('SJ_API_KEY')


class APIProcessor(ABC):
    @abstractmethod
    def get_vacancies(self, text_for_search):
        pass


class Handler(ABC):
    @abstractmethod
    def save(self, vacancies_list):
        pass

    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def read_if(self, salary: list[int] | int, keyword: str) -> list:
        """
        Функция считывает из файла только вакансии соответствующие параметрам.
        :param salary: Зарплата в виде ['from', 'to'] или 'значение'. Если указано значение,
        то проверяется его вхождение в промежуток 'from-to'.
        :param keyword: Ключевое слово. Проверяется по названию и описанию.
        :return: Список вакансий(объектов)
        """
        pass


class Vacancy:
    def __init__(self, name: str = '', salary: list = (0, 0), description: str = '', url: str = ''):
        self.name = name
        self.salary = salary
        self.salary.append((self.salary[1] - self.salary[0]) / 2 + self.salary[0])
        self.description = description
        self.url = url

    @classmethod
    def from_dict(cls, vacancy_data: dict):
        name = vacancy_data['name']
        salary = vacancy_data['salary']
        salary.append((vacancy_data['salary'][1] - vacancy_data['salary'][0]) / 2)
        description = vacancy_data['description']
        url = vacancy_data['url']

        return cls(name=name, salary=salary, description=description, url=url)

    def __gt__(self, other):
        return self.salary[2] > other.salary[2]

    def __lt__(self, other):
        return self.salary[2] < other.salary[2]

    def __eq__(self, other):
        return self.salary[2] == other.salary[2]

    def __ge__(self, other):
        return self.salary[2] >= other.salary[2]

    def __le__(self, other):
        return self.salary[2] <= other.salary[2]

    def __str__(self):
        return (f'{'-' * 50}\n'
                f'{self.name}\n'
                f'{self.description}\n'
                f'Зарплата от {self.salary[0]} до {self.salary[1]}\n'
                f'{self.url}')

    def __repr__(self):
        return


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
                                params=self.params, headers=self.headers).json()['objects']

        for vacancy in response:
            vacancies.append(Vacancy(name=vacancy['profession'],
                                     salary=[vacancy['payment_from'], vacancy['payment_to']],
                                     description=vacancy['candidat'],
                                     url=vacancy['link']))

        return vacancies


class HHProcessor(APIProcessor):
    headers = {'HH-User-Agent': 'Kursovaya/1.0 (vavilon164@yandex.ru)'}
    params = {'per_page': 20, 'page': 0}

    def get_vacancies(self, keywords: dict):
        """
        keywords = {'text': '', search_field': 'name/company_name/description', 'salary': int}
        :param keywords:
        :return:
        """
        vacancies = []
        salary = [0, 0, 0]
        self.params = keywords

        response = requests.get('https://api.superjob.ru/2.0/vacancies',
                                params=self.params, headers=self.headers).json()['items']

        for vacancy in response:
            try:
                salary = [vacancy['salary']['from'], vacancy['salary']['to']]

            except KeyError as err:
                pass

            finally:
                vacancies.append(Vacancy(name=vacancy['name'],
                                         salary=salary,
                                         description=vacancy['snippet']['responsibility'],
                                         url=vacancy['url']))

        return vacancies


class JSONHandler(Handler):
    def __init__(self, file_name: str = "Vacancies_list.json"):
        self.file_name = file_name

    def read_if(self, salary: list[int] | int, keyword: str) -> list[Vacancy]:
        all_vacancies = self.read_all()
        sorted_vacancies = []
        add_vacancy = True
        for vacancy in all_vacancies:
            if salary:
                if type(salary) is int:
                    if not salary >= vacancy['salary'][0] or not salary <= vacancy['salary'][1]:
                        add_vacancy = False
                        
                elif type(salary) is list:
                    if not (vacancy['salary'][0] <= salary[0] <= vacancy['salary'][1] or
                            vacancy['salary'][0] <= salary[1] <= vacancy['salary'][1]):
                        add_vacancy = False

            if keyword:
                if keyword not in vacancy['name'] and keyword not in vacancy['description']:
                    add_vacancy = False
                    
            if add_vacancy:
                sorted_vacancies.append(Vacancy.from_dict(vacancy))

        return sorted_vacancies

    def read_all(self) -> list[dict]:
        with open(self.file_name, encoding='UTF-8') as file:
            vacancies = json.load(file)

        return vacancies

    def save(self, vacancies_list: Vacancy):
        vacancies = []

        with (open(self.file_name, 'w', encoding='UTF-8') as file):
            for vacancy in vacancies_list:
                vacancies.append({'name': vacancy.name,
                                  'description': vacancy.description,
                                  'salary': vacancy.salary,
                                  'url': vacancy.url})

            json.dump(vacancies, file, ensure_ascii=False)
