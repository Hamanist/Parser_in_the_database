import os

import psycopg2
from dotenv import load_dotenv

from parse_class.parse import Parse

load_dotenv()


class DBManager:

    def connect_bd(self):
        with psycopg2.connect(
                host=os.getenv('HOST'),
                database=os.getenv('DATABASE'),
                user=os.getenv('USER_P'),
                password=os.getenv('PASSWORD')) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """CREATE TABLE IF NOT EXISTS company (
                    company_id INT PRIMARY KEY,
                    company_name VARCHAR(150) NOT NULL,
                    url_company VARCHAR(150) NOT NULL 
                    );
                    CREATE TABLE IF NOT EXISTS vacancy (
                    vacancy_id INT PRIMARY KEY,
                    vacancies_name VARCHAR(150) NOT NULL,
                    city VARCHAR(150) NOT NULL,
                    salary_min INT DEFAULT 0,
                    salary_max INT DEFAULT 0,
                    url_vacancies VARCHAR(150) NOT NULL,
                    company_id INT REFERENCES company(company_id))
                    """

                )
                report = Parse().get_data()
                for data in report:
                    curs.execute(
                        """INSERT INTO company (company_id, company_name, url_company) VALUES(%s, %s, %s)
                         ON CONFLICT DO NOTHING""",
                        (data['id'], data['company'], data['url'])

                    )

                    curs.execute(
                        """INSERT INTO vacancy (vacancy_id, vacancies_name, city, salary_min, salary_max, url_vacancies, company_id)
                         VALUES(%s, %s, %s, %s, %s, %s, %s)
                         ON CONFLICT DO NOTHING""",
                        (data['vacancies_id'], data['vacancies_name'], data['city'], data['salary_min'],
                         data['salary_max'], data['url_vacancies'], data['id'])

                    )

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """

        with psycopg2.connect(
                host=os.getenv('HOST'),
                database=os.getenv('DATABASE'),
                user=os.getenv('USER_P'),
                password=os.getenv('PASSWORD')) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    SELECT company_name, COUNT(DISTINCT vacancies_name) 
                    FROM company
                    FULL JOIN vacancy USING (company_id)
                    GROUP BY company_name
                    """
                )
                rows = curs.fetchall()
        return rows

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        with psycopg2.connect(
                host=os.getenv('HOST'),
                database=os.getenv('DATABASE'),
                user=os.getenv('USER_P'),
                password=os.getenv('PASSWORD')) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    SELECT company_name, vacancies_name, salary_min, salary_max, url_vacancies
                    FROM company
                    FULL JOIN vacancy USING (company_id)
                    """
                )
                rows = curs.fetchall()
        return rows

    def get_avg_salary(self):
        """
    Получает среднюю зарплату по вакансиям.
        """
        with psycopg2.connect(
                host=os.getenv('HOST'),
                database=os.getenv('DATABASE'),
                user=os.getenv('USER_P'),
                password=os.getenv('PASSWORD')) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    SELECT vacancies_name, company_name, round(AVG((salary_max + salary_min) / 2)) AS average_salary
                    FROM company
                    FULL JOIN vacancy USING (company_id)
                    GROUP BY vacancies_name, company_name
                    """
                )
                rows = curs.fetchall()
        return rows

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        with psycopg2.connect(
                host=os.getenv('HOST'),
                database=os.getenv('DATABASE'),
                user=os.getenv('USER_P'),
                password=os.getenv('PASSWORD')) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    SELECT vacancies_name, company_name, round(AVG((salary_max + salary_min) / 2)) AS average_salary
                    FROM company
                    WHERE (salary_max + salary_min) / 2 > (SELECT round(AVG((salary_max + salary_min) / 2))
                    FROM vacancy)
                    ORDER BY vacancies_name
                    """
                )
                rows = curs.fetchall()
        return rows

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        with psycopg2.connect(
                host=os.getenv('HOST'),
                database=os.getenv('DATABASE'),
                user=os.getenv('USER_P'),
                password=os.getenv('PASSWORD')) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    f"""
                    SELECT vacancies_name 
                    FROM vacancy
                    WHERE vacancies_name LIKE '%{keyword}%'
                    """
                )

                rows = curs.fetchall()
        return rows
