import requests


def get_information_from_hh(language):
    hh_url = 'https://api.hh.ru/vacancies'
    page = 0
    vacancies = []
    pages = 100
    city=1

    params = {
        'text': 'Программист {}'.format(language),
        'area': city,
        'page': page,
        'only_with_salary': 'True'}

    while page < pages:
        params['page'] = page
        response = requests.get(hh_url, params=params)
        response.raise_for_status()
        pages = response.json()['pages']
        page += 1
        vacancies.append(response.json())
    return vacancies


def get_vacancies(vacancies):
    vacancies = {'vacancies': [vacancies['items']],
                'found': vacancies['found']
                }
    return vacancies
