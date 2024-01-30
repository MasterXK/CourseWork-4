import os
from pprint import pprint
from src.classes import SJProcessor, HHProcessor, JSONHandler

import requests
import dotenv

dotenv.load_dotenv()
SJ_KEY = os.getenv('SJ_API_KEY')

headers = {'HH-User-Agent': 'Kursovaya (vavilon164@yandex.ru)'}  # {'X-Api-App-Id': SJ_KEY}
params = {'text': 'python',
          'search_field': 'name',
          'page': 0}

keywords = [{'keys': 'python',
             'srws': '1',
             'skwc': 'or'}]

keywordsh = {'text': 'python',
             'search_field': [{'value': 'name'}]}

response = requests.get('https://api.hh.ru/vacancies',
                        params=params, headers=headers).json()['items']

# sj_proc = SJProcessor()
# hh_proc = HHProcessor()
# json_saver = JSONHandler()
# json_saver.save(hh_proc.get_vacancies(keywordsh))

pprint(response, sort_dicts=False)
