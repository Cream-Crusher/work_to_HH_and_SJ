import requests


def get_information_from_hh(language):
    hh_url = 'https://api.hh.ru/vacancies'
    page = 0
    vacancies = []
    pages = 100
    city = 1
    entrance = 0
    params = {
        'text': 'Программист {}'.format(language),
        'area': city,
        'page': page,
        'only_with_salary': 'True'}

    while page < pages:
        params['page'] = page
        response = requests.get(hh_url, params=params)
        response.raise_for_status()
        vacancies.append(response.json())
        pages = vacancies[entrance]['pages']
        page += 1

    return vacancies


def get_vacancies_hh(all_vacancies, language):
    information_on_vacancies = []
    vacancies = []
    vacancies.extend(all_vacancies)

    for part_vacancies in vacancies:
        for vacancies in part_vacancies['items']:
            pay_from = vacancies['salary']['from']
            pay_to = vacancies['salary']['to']

            if  pay_from and pay_from < 400:
                pay_from *= 1000

            if pay_to and pay_to < 400:
                pay_from *= 1000

            vacancies = {'language': language,
                    'pay_from': pay_from,
                    'pay_to':  pay_to,
                    'currency': vacancies['salary']['currency'],
                    'found': part_vacancies['found']
                    }
            information_on_vacancies.append(vacancies)
    return information_on_vacancies
