import os
from pprint import pprint
from src.APIProcessorClasses import SJProcessor, HHProcessor
from src.HandlerClasses import JSONHandler
import requests

import dotenv

dotenv.load_dotenv()
SJ_KEY = os.getenv('SJ_API_KEY')


def start_process():
    keywords = []
    sj_proc = SJProcessor()
    hh_proc = HHProcessor()
    json_handler = JSONHandler()
    keyword = ''

    while True:
        if not keyword:
            keyword = input('Введите ключевое слово для поиска: ')

        keywords.append({'text': keyword})

        srch_param = int(input('Где искать?:\n'
                               '\t1 - в названии вакансии;\n'
                               '\t2 - в названии компании;\n'
                               '\t3 - в описании вакансии;\n'
                               '\t4 - везде;\n'))

        if srch_param in [1, 2, 3]:
            keywords[-1]['param'] = srch_param

        elif srch_param == 4:
            pass

        else:
            print('Введите один из предложенных вариантов')
            continue

        more_keys = int(input('Добавить еще ключевое слово?\n'
                              '\t0 - Нет\n'
                              '\t1 - Да\n'))
        keyword = ''

        if not more_keys:
            break

    desired_salary = input('Введите желаемую зарплату: ')
    desired_salary.strip()
    salary = []
    if '-' in desired_salary:
        for elem in desired_salary.split('-'):
            salary.append(int(elem))

    elif desired_salary:
        variation = int(input('Введите возможное отклонение(+-) от желаемой зарплаты(по умолчанию 10 000): '))
        if variation:
            salary = [int(desired_salary) - variation, int(desired_salary) + variation]

    services_to_use = int(input('Где искать?\n'
                                '\t 1 - SuperJob\n'
                                '\t 2 - HeadHunter\n'
                                '\t 3 - SuperJob и HeadHunter\n'))

    vacancies = []

    if services_to_use in [1, 3]:
        vacancies.extend(sj_proc.get_vacancies(keywords, salary))

    if services_to_use in [2, 3]:
        vacancies.extend(hh_proc.get_vacancies(keywords, salary))

    if vacancies:
        json_handler.save(vacancies)
        print('Найденные вакансии сохранены.')

    else:
        print('Вакансий не найдено. Измените запрос.')
        start_process()

    make_top = input('Вывести топ вакансий по заработной плате? 1 - Да, 0 - Нет')
    if make_top:
        num_of_vacancies = int(input('Сколько вакансий вывести?'))
        pprint(json_handler.read(num_of_vacancies), sort_dicts=False)


if __name__ == '__main__':
    start_process()
