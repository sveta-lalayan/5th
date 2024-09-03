from abc import ABC, abstractmethod
from typing import List, Tuple, Dict

class AbstractDBManager(ABC):
    """Абстрактный класс для соединения с базой данных с компаниями и вакансиями"""

    @abstractmethod
    def __init__(self, db_name: str) -> None:
        pass

    @abstractmethod
    def create_the_tables(self) -> None:
        """Создание таблиц"""
        pass

    @abstractmethod
    def fill_the_tables(self, employers: List, vacancies: List) -> None:
        """Заполнение базы"""
        pass

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """Список всех компаний"""
        pass

    @abstractmethod
    def get_all_vacancies(self) -> List[Tuple]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    @abstractmethod
    def get_avg_salary(self) -> int:
        """Зп по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Вакансии с высоким зп"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Получает список всех вакансий, в названии которых содержатся ключевое слово"""
        pass