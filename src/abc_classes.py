from abc import ABC, abstractmethod


class APIProcessor(ABC):
    def get_vacancies(self, text_for_search):
        pass
