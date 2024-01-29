import requests


class Parse:
    """
    Класс для парсинга
    """

    def get_data(self):
        __url = 'https://api.hh.ru/vacancies'
        __params = {
            "employer_id": ['3529', '606135', '2519536', '38377', '3953333', '5902137', '676167', '3553513', '35086',
                            '5169831', '246664'],
            'per_page': '50'
        }
        response = requests.get(url=__url, params=__params)
        if response.status_code == 200:
            return self._parse(response.json())
        return None

    def _parse(self, data):
        # print(data)
        # print('')
        answer = []
        for report in data['items']:
            answer.append({
                'id': report['employer']['id'],
                'company': report['employer']['name'],
                'url': report['employer']['url'],
                'salary_min': (report['salary'] or {}).get("from"),
                'salary_max': (report['salary'] or {}).get("to"),
                'city': report['area']['name'],
                'vacancies_id': report['id'],
                'vacancies_name': report['name'],
                'url_vacancies': report['alternate_url']
            })
        return answer
