class Vacancy():
    '''Класс для организации данных по вакансиям в удобном виде. хранит в себе полезные атрибуты по вакансиям'''

    def __init__(self, region, employer_id, employer_name, vacancy_name, salary, currency, requirement, vacancy_url):
        self.region = region
        self.employer_id = employer_id
        self.employer_name = employer_name
        self.vacancy_name = vacancy_name
        self.salary = salary
        self.currency = currency
        self.requirement = requirement
        self.vacancy_url = vacancy_url

    def __str__(self):
        cut_line = '-' * 120
        return (f"{cut_line}Регион: {self.region},\n"
                f"ID работодателя: {self.employer_id},\n"
                f"Работодатель: {self.employer_name},\n"
                f"Вакансия: {self.vacancy_name},\n"
                f"ЗП: {self.salary} {self.currency},\n"
                f"Требования: {self.requirement}),\n"
                f"ссылка на вакансию: {self.vacancy_url}")

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __lt__(self, other):
        if self.salary is not None and other.salary is not None:
            return self.salary < other.salary
