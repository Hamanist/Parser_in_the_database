import requests


class Parse:
    """
    Класс для парсинга
    """

    @staticmethod
    def get_salary(salary):
        salary_list = [0, 0]
        if salary and salary['from'] and salary['from'] != 0:
            salary_list[0] = salary['from']
        if salary and salary['to'] and salary['to'] != 0:
            salary_list[1] = salary['to']
        return salary_list

    def get_data(self):
        __url = 'https://api.hh.ru/vacancies'
        __params = {
            "employer_id": ['3529', '606135', '2519536', '38377', '3953333', '5902137', '676167', '3553513', '35086',
                            '5169831', '246664'],
            'per_page': '100'
        }
        response = requests.get(url=__url, params=__params)
        if response.status_code == 200:
            return self._parse(response.json())
        return None

    def _parse(self, data):
        answer = []
        for report in data['items']:
            salary_min, salary_max = self.get_salary(report['salary'])
            answer.append({
                'id': report['employer']['id'],
                'company': report['employer']['name'],
                'url': report['employer']['url'],
                'salary_min': salary_min,
                'salary_max': salary_max,
                'city': report['area']['name'],
                'vacancies_id': report['id'],
                'vacancies_name': report['name'],
                'url_vacancies': report['alternate_url']
            })
        return answer
