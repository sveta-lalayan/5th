class DBManager:
    '''Класс для подключения и работы с БД'''

    def __init__(self, con):
        self.con = con

    def get_companies_and_vacancies_count(self):
        '''Получает список компаний и количество вакансий у каждой компании'''
        with self.con, self.con.cursor() as cur:
            cur.execute('SELECT employer_name, COUNT(*) FROM vacancies '
                        'JOIN employers USING(employer_id) '
                        'GROUP BY employer_name')
            rows = cur.fetchall()
            for company, count in rows:
                print(f"Компания: {company}, Вакансий: {count}")

    def get_all_vacancies(self):
        '''Получает список всех вакансий с указанием компании, названия вакансии, зарплаты и ссылки'''
        with self.con, self.con.cursor() as cur:
            cur.execute('SELECT * FROM vacancies')
            rows = cur.fetchall()
            for vacancy in rows:
                print(f'{vacancy}\n{"-" * 100}')

    def get_avg_salary(self, currency="RUR"):
        '''Получает среднюю зарплату по вакансиям в указанной валюте (по умолчанию "RUR")'''
        with self.con, self.con.cursor() as cur:
            cur.execute('SELECT AVG(salary) FROM vacancies WHERE currency = %s', (currency,))
            avg_salary = cur.fetchone()[0]
            if avg_salary:
                print(f"Средняя зарплата: {int(avg_salary)} {currency}")
            else:
                print(f"Валюта {currency} отсутствует в базе данных")

    def get_vacancies_with_higher_salary(self, currency="RUR"):
        '''Получает вакансии с зарплатой выше средней по указанной валюте'''
        with self.con, self.con.cursor() as cur:
            cur.execute('SELECT * FROM vacancies WHERE currency = %s AND salary > '
                        '(SELECT AVG(salary) FROM vacancies WHERE currency = %s)', (currency, currency))
            rows = cur.fetchall()
            for vacancy in rows:
                print(f'{vacancy}\n{"-" * 100}')

    def get_vacancies_with_keyword(self, keyword):
        '''Получает вакансии по ключевому слову в названии'''
        with self.con, self.con.cursor() as cur:
            cur.execute('SELECT * FROM vacancies WHERE vacancy LIKE %s', (f'%{keyword}%',))
            rows = cur.fetchall()
            for vacancy in rows:
                print(f'{vacancy}\n{"-" * 100}')

    def con_close(self):
        '''Закрывает соединение с БД'''
        if self.con:
            self.con.close()
