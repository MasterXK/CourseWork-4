import os
from pprint import pprint
from src.classes import SJProcessor, JSONHandler

import requests
import dotenv

dotenv.load_dotenv()
SJ_KEY = os.getenv('SJ_API_KEY')

headers = {'X-Api-App-Id': SJ_KEY}
params = {'keywords[0][keys]': 'python',
          'keywords[0][srws]': '1',
          'keywords[0][skwc]': 'or',
          'page': 0}

keywords = [{'keys': 'python',
             'srws': '10',
             'skwc': 'or'}]

response = requests.get('https://api.superjob.ru/2.0/vacancies',
                        params=params, headers=headers).json()['objects']

sj_proc = SJProcessor()
json_saver = JSONHandler()
json_saver.save(sj_proc.get_vacancies(keywords))

pprint(json_saver.read_all(), sort_dicts=False)
