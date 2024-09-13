# from abc import ABC, abstractmethod
# from typing import List, Tuple, Dict
#
# class AbstractDBManager(ABC):
#     """Абстрактный класс для соединения с базой данных с компаниями и вакансиями"""
#
#     @abstractmethod
#     def __init__(self, db_name: str) -> None:
#         pass
#
#     @abstractmethod
#     def create_the_tables(self) -> None:
#         """Создание таблиц"""
#         pass
#
#     @abstractmethod
#     def fill_the_tables(self, employers: List, vacancies: List) -> None:
#         """Заполнение базы"""
#         pass
#
#     @abstractmethod
#     def get_companies_and_vacancies_count(self) -> List[Dict]:
#         """Список всех компаний"""
#         pass
#
#     @abstractmethod
#     def get_all_vacancies(self) -> List[Tuple]:
#         """Получает список всех вакансий с указанием названия компании,
#         названия вакансии и зарплаты и ссылки на вакансию"""
#         pass
#
#     @abstractmethod
#     def get_avg_salary(self) -> int:
#         """Зп по вакансиям"""
#         pass
#
#     @abstractmethod
#     def get_vacancies_with_higher_salary(self) -> List[Tuple]:
#         """Вакансии с высоким зп"""
#         pass
#
#     @abstractmethod
#     def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
#         """Получает список всех вакансий, в названии которых содержатся ключевое слово"""
#         pass




import psycopg2

class DBManager:
    def __init__(self, db_name, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cur.execute("SELECT c.name, COUNT(v.id) FROM companies c JOIN vacancies v ON c.id = v.company_id GROUP BY c.name")
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute("SELECT v.title, c.name, v.salary, v.link FROM vacancies v JOIN companies c ON v.company_id = c.id")
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute("SELECT AVG(v.salary) FROM vacancies v")
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute("SELECT v.title, c.name, v.salary, v.link FROM vacancies v JOIN companies c ON v.company_id = c.id WHERE v.salary > %s", (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute("SELECT v.title, c.name, v.salary, v.link FROM vacancies v JOIN companies c ON v.company_id = c.id WHERE v.title ILIKE %s", (f"%{keyword}%",))
        return self.cur.fetchall()

    def close(self):
        self.conn.close()