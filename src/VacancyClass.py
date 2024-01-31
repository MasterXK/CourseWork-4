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
        return self.name