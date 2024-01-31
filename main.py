from manager.bd_manager import DBManager
from parse_class.parse import Parse


def main():
    Parse().get_data()
    DBManager().connect_bd()
    try:
        while True:
            user = int(input("""
        Что вам нужно:
        Получить список всех компаний и количество вакансий у каждой компании - нажмите 1
        Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию - нажмите 2
        Получает среднюю зарплату по вакансиям - нажмите 3
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям - нажмите 4
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например "python" - нажмите 5
        Выход - нажмите 0\n--->
        """))

            if user == 1:
                report = DBManager().get_companies_and_vacancies_count()
                for i in report:
                    print(*i)
            elif user == 2:
                report = DBManager().get_all_vacancies()
                for i in report:
                    print(*i)
            elif user == 3:
                report = DBManager().get_avg_salary()
                for i in report:
                    print(*i)
            elif user == 4:
                report = DBManager().get_vacancies_with_higher_salary()
                for i in report:
                    print(*i)
            elif user == 5:
                word = input("Введите слово")
                report = DBManager().get_vacancies_with_keyword(word)
                for i in report:
                    print(*i)
            else:
                print('Не правильно ввели данные')
    except ValueError:
        print("Введите число")

if __name__ == '__main__':
    main()
