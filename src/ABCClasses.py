from abc import ABC, abstractmethod


class APIProcessor(ABC):
    @abstractmethod
    def get_vacancies(self, text_for_search, desired_salary):
        pass


class Handler(ABC):
    @abstractmethod
    def save(self, vacancies_list):
        pass

    @abstractmethod
    def read(self, number_to_read):
        pass

    @abstractmethod
    def read_if(self, salary: list[int] | int, keyword: str) -> list:
        pass
