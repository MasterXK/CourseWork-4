import json

from src.ABCClasses import Handler
from src.VacancyClass import Vacancy


class JSONHandler(Handler):
    def __init__(self, file_name: str = "Vacancies_list.json"):
        self.file_name = file_name

    def read_if(
        self, keyword: str = None, salary: list[int] | int = None
    ) -> list[Vacancy]:
        """
        Функция считывает из файла только вакансии соответствующие параметрам.

        :param salary: Зарплата в виде ['from', 'to'] или 'значение'. Если указано значение,
        то проверяется его вхождение в промежуток 'from-to'.
        :param keyword: Ключевое слово. Проверяется по названию и описанию.
        :return: Список вакансий(объектов)
        """
        all_vacancies = self.read()
        filtered_vacancies = []
        add_vacancy = True
        for vacancy in all_vacancies:
            if salary:
                if type(salary) is int:
                    if not salary >= vacancy["salary"][0]:
                        add_vacancy = False

                elif type(salary) is list:
                    if not (
                        vacancy["salary"][0] <= salary[0] <= vacancy["salary"][1]
                        or vacancy["salary"][0] <= salary[1] <= vacancy["salary"][1]
                    ):
                        add_vacancy = False
                else:
                    return "Неверный формат зарплаты."

            if keyword:
                if (
                    keyword not in vacancy["name"]
                    and keyword not in vacancy["description"]
                ):
                    add_vacancy = False

            if add_vacancy:
                filtered_vacancies.append(Vacancy.from_dict(vacancy))

        return filtered_vacancies

    def read(self, number_to_read=False) -> list[dict]:
        with open(self.file_name, encoding="UTF-8") as file:
            vacancies = json.load(file)

        if number_to_read:
            return vacancies[:number_to_read]
        return vacancies

    def save(self, vacancies_list: Vacancy):
        vacancies = []

        with open(self.file_name, "w", encoding="UTF-8") as file:
            for vacancy in vacancies_list:
                vacancies.append(
                    {
                        "name": vacancy.name,
                        "description": vacancy.description,
                        "salary": vacancy.salary,
                        "url": vacancy.url,
                    }
                )

            json.dump(vacancies, file, ensure_ascii=False, indent=4)
