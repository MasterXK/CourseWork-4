import os
from pprint import pprint
from src.classes import SJProcessor, HHProcessor, JSONHandler

import dotenv

dotenv.load_dotenv()
SJ_KEY = os.getenv('SJ_API_KEY')


def start_process():
    keywords = []
    sj_proc = SJProcessor()
    hh_proc = HHProcessor()
    json_saver = JSONHandler()
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

    services_to_use = int(input('Где искать?\n'
                                '\t 1 - SuperJob\n'
                                '\t 2 - HeadHunter\n'
                                '\t 3 - SuperJob и HeadHunter\n'))

    vacancies = []

    if services_to_use in [1, 3]:
        vacancies.extend(sj_proc.get_vacancies(keywords))

    elif services_to_use in [2, 3]:
        vacancies.extend(hh_proc.get_vacancies(keywords))
    pprint(vacancies)
    json_saver.save(vacancies)


if __name__ == '__main__':
    start_process()
