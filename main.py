import os
import time

from src.db_manager_cls import DBManager
from src.headhunterapi_cls import HeadHunterAPI
from src.utils import drop_database, create_database, connector, tables_creator, loads_into_table
from universal_rooth_path import ROOT_DIR


config_file_path = os.path.join(ROOT_DIR, 'secret_data', 'db_config_file.ini')


conn = connector(config_file_path, 'postgres')


drop_database(conn, 'cw5')





create_database(conn, 'cw5')



conn = connector(config_file_path, 'cw5')


tables_creator(conn)


hh_api = HeadHunterAPI(keyword='', page_quantity=2)

vacancies = hh_api.parsed_vacancies





conn = connector(config_file_path, 'cw5')


loads_into_table(conn, vacancies)



conn = connector(config_file_path, 'cw5')


db_man = DBManager(conn)


db_man.get_companies_and_vacancies_count()

db_man.get_avg_salary()




db_man.get_vacancies_with_keyword('менеджер')


