from abc import ABC, abstractmethod


class APIVac(ABC):
    """Абстрактный класс для работы с API сайтов вакансий"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str) -> list:
        """Метод, который служит для получения списка вакансий по запросу"""
        pass