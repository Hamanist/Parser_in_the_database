# Получить данные о работодателях и их вакансиях с сайта hh.ru. Для этого используйте публичный API hh.ru и библиотеку
# requests
# .
# Выбрать не менее 10 интересных вам компаний, от которых вы будете получать данные о вакансиях по API.
# Спроектировать таблицы в БД PostgreSQL для хранения полученных данных о работодателях и их вакансиях.
# Для работы с БД используйте библиотеку psycopg2
# .
# Реализовать код, который заполняет созданные в БД PostgreSQL таблицы данными о работодателях и их вакансиях.
# Создать класс
# DBManager для работы с данными в БД.
from manager.bd_manager import DBManager
from parse_class.parse import Parse

#Parse().get_data()

# for i in Parse().get_data():
#     print(i)
DBManager().connect_bd()

# String Data Right Truncation: value too long for type character varying(50)
#Unexpected argument