from abc import ABC, abstractmethod


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
