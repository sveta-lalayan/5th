import psycopg2
import configparser


def connector(config_file_path, db_name=None):
    '''Коннектор для соединения с БД.'''
    config = configparser.ConfigParser()
    config.read(config_file_path)
    database_config = dict(config.items('database'))

    # Если не передана база данных, подключаемся к базе postgres
    database_name = db_name if db_name else database_config['database']

    conn = psycopg2.connect(
        host=database_config['host'],
        database=database_name,
        user=database_config['user'],
        password=database_config['password']
    )
    conn.autocommit = True
    return conn


def create_database(conn, database_name):
    '''Создает базу данных, если она не существует.'''
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'")
            exists = cur.fetchone()
            if not exists:
                cur.execute(f'CREATE DATABASE {database_name}')
                print(f'База данных {database_name} создана.')
            else:
                print(f'База данных {database_name} уже существует.')

    except psycopg2.Error as e:
        print(f"Произошла ошибка: {e.pgerror}")
        print(f"Код ошибки: {e.pgcode}")


def drop_database(conn, database_name):
    '''Удаляет базу данных, если она существует.'''
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'")
            exists = cur.fetchone()
            if exists:
                cur.execute(f'DROP DATABASE {database_name}')
                print(f'База данных {database_name} удалена.')
            else:
                print(f'База данных {database_name} не существует.')

    except psycopg2.Error as e:
        print(f"Произошла ошибка: {e.pgerror}")
        print(f"Код ошибки: {e.pgcode}")


def tables_creator(conn, table_name_1='employers', table_name_2='vacancies'):
    '''Создает таблицы employers и vacancies.'''
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(f'''CREATE TABLE IF NOT EXISTS {table_name_1}
                            (
                                employer_id SERIAL PRIMARY KEY,
                                employer_name VARCHAR(100) NOT NULL
                            )''')

                cur.execute(f'''CREATE TABLE IF NOT EXISTS {table_name_2}
                            (  
                                vacancy_id SERIAL PRIMARY KEY,
                                employer_id INT NOT NULL,
                                region VARCHAR(100) NOT NULL,
                                vacancy VARCHAR(100) NOT NULL,
                                salary INT NOT NULL,
                                currency VARCHAR(100),
                                requirement TEXT,
                                vacancy_url VARCHAR(100) NOT NULL,
                                FOREIGN KEY (employer_id) REFERENCES {table_name_1}(employer_id)
                            )''')

    except psycopg2.Error as e:
        print(f"Произошла ошибка: {e.pgerror}")
        print(f"Код ошибки: {e.pgcode}")


def loads_into_table(conn, vacancies):
    '''Заполняет таблицы данными о вакансиях.'''
    try:
        with conn:
            with conn.cursor() as cur:
                for vac in vacancies:
                    cur.execute('INSERT INTO employers (employer_id, employer_name) VALUES '
                                '(%s, %s) ON CONFLICT (employer_id) DO NOTHING', (vac.employer_id, vac.employer_name))

                    cur.execute('INSERT INTO vacancies '
                                '(employer_id, region, vacancy, salary, currency, requirement, vacancy_url) '
                                'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                                (vac.employer_id, vac.region, vac.vacancy_name, vac.salary, vac.currency,
                                 vac.requirement, vac.vacancy_url))

    except psycopg2.Error as e:
        print(f"Произошла ошибка: {e.pgerror}")
        print(f"Код ошибки: {e.pgcode}")
