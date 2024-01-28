import os
from pprint import pprint

import requests
import dotenv

dotenv.load_dotenv()
SJ_KEY = os.getenv('SJ_API_KEY')

headers = {'X-Api-App-Id': SJ_KEY}
params = {'keywords[0][keys]': 'python',
          'keywords[0][srws]': '1',
          'keywords[0][skwc]': 'and'}

response = requests.get('https://api.superjob.ru/2.0/vacancies',
                        params=params, headers=headers).json()['objects']
pprint(response, sort_dicts=False)