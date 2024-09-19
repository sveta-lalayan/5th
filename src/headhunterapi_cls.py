import requests
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from src.vacancy_cls import Vacancy


class Parser(ABC):
    @abstractmethod
    def load_vacancies(self):
        pass


class HeadHunterAPI(Parser):
    """
    Класс для работы с API HeadHunter.
    Класс Parser является родительским классом.
    """
    employers_ids = {
        80: 'Альфа банк',
        78638: 'Тинькофф',
        196621: 'Fix Price',
        84585: 'Авито',
        4219: 'Теле2',
        1373: 'Аэрофлот',
        15478: 'VK',
        2180: 'Ozon',
        780654: 'Lamoda',
        1740: 'Яндекс'
    }

    def __init__(self, keyword: str = '', page_quantity: int = 5):
        self.url = 'https://api.hh.ru/vacancies'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {
            'text': keyword,
            'page': 0,
            'per_page': 100,
            'only_with_salary': 'true'
        }
        self.vacancies: List[Dict] = []
        self.parsed_vacancies: List[Vacancy] = []
        self.load_vacancies(page_quantity)
        self.api_vacancies_parser(self.vacancies)

    def load_vacancies(self, page_quantity: int = 5) -> None:
        """
        Загружает данные с API HH.ru по каждому работодателю.
        """
        for employer_id in self.employers_ids:
            self.params['employer_id'] = str(employer_id)  # Параметр employer_id должен быть строкой

            for page in range(page_quantity):
                self.params['page'] = page
                try:
                    response = requests.get(self.url, headers=self.headers, params=self.params)
                    response.raise_for_status()  # Проверка успешности запроса
                    vacancies = response.json().get('items', [])
                    self.vacancies.extend(vacancies)
                except requests.RequestException as e:
                    print(f"Ошибка при загрузке данных для эмплойера {employer_id}: {e}")
                    break

    def api_vacancies_parser(self, api_data: List[Dict]) -> List[Vacancy]:
        """
        Парсит данные с API по определенным критериям.
        """
        vacancies_list: List[Vacancy] = []

        for data in api_data:
            vacancy_name = data.get('name', 'Не указано')
            salary_info = self._parse_salary(data.get('salary'))
            requirement = self._parse_requirements(data.get('snippet', {}).get('requirement', 'нет требований'))
            vacancy_url = data.get('alternate_url', '')
            region = data.get('area', {}).get('name', 'Не указано')
            employer_info = data.get('employer', {})
            employer_id = employer_info.get('id', 'Не указано')
            employer_name = employer_info.get('name', 'Не указано')

            vacancy_instance = Vacancy(
                region=region,
                employer_id=employer_id,
                employer_name=employer_name,
                vacancy_name=vacancy_name,
                salary=salary_info['amount'],
                currency=salary_info['currency'],
                requirement=requirement,
                vacancy_url=vacancy_url
            )

            vacancies_list.append(vacancy_instance)

        self.parsed_vacancies = vacancies_list
        #return vacancies_list

    @staticmethod
    def _parse_salary(salary_data: Optional[Dict]) -> Dict[str, Optional[str]]:
        """
        Парсит информацию о зарплате.
        """
        if not salary_data or not salary_data.get('from'):
            return {'amount': 0, 'currency': 'Не указано'}

        return {
            'amount': salary_data['from'],
            'currency': salary_data.get('currency', 'Не указано')
        }

    @staticmethod
    def _parse_requirements(requirements: Optional[str]) -> str:
        """
        Убирает теги <highlighttext> из требований, если они есть.
        Если требования отсутствуют (None), возвращает 'нет требований'.
        """
        if requirements is None:
            return 'нет требований'
        return requirements.replace('<highlighttext>', '').replace('</highlighttext>', '')


# просто тест удали потом !!!!!!!!!!!!!!!
if __name__ == "__main__":
    hh_api = HeadHunterAPI(keyword='', page_quantity=5)
    for vacancy in hh_api.parsed_vacancies:
        print(vacancy)
