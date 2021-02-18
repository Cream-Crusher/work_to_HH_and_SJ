import requests


def get_information_from_hh(language):

    hh_url = 'https://api.hh.ru/vacancies'
    page = 0
    vacancies = []
    vacancies_the_page = 100
    city_number = 1
    entrance = 0
    params = {
        'text': 'Программист {}'.format(language),
        'area': city_number,
        'page': page,
        'only_with_salary': 'True'
    }

    while page < vacancies_the_page:
        params['page'] = page
        response = requests.get(hh_url, params=params)
        response.raise_for_status()
        vacancies.append(response.json())
        vacancies_the_page = vacancies[entrance]['pages']
        page += 1

    return vacancies


def get_vacancies_hh(all_vacancies, language):

    information_on_vacancies = []
    
    for part_vacancies in all_vacancies:
        for vacancy in part_vacancies['items']:
            pay_from = vacancy['salary']['from']
            pay_to = vacancy['salary']['to']

            if  pay_from and pay_from < 400:
                pay_from *= 1000

            if pay_to and pay_to < 400:
                pay_from *= 1000

            vacancy = {
                'language': language,
                'pay_from': pay_from,
                'pay_to':  pay_to,
                'currency': vacancy['salary']['currency'],
                'found': part_vacancies['found']
            }
            information_on_vacancies.append(vacancy)
    return information_on_vacancies
