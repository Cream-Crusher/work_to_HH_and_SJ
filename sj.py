import requests


def get_information_from_sj(language, TOKEN):
    catalogue_designation=48
    maximum_number_of_vacancies = 100
    url_sj = 'https://api.superjob.ru/2.0/vacancies'
    vacancies = []
    name_town=4
    page = 0
    number_of_possible_vacancies = 0
    total_vacancies = 1
    entrance = 0
    auth_token = {
        'X-Api-App-Id': TOKEN
        }
    while number_of_possible_vacancies < total_vacancies:
        params = {
            'keyword': language,
            'page': page,
            'town': name_town,
            'catalogues': catalogue_designation,
            'count': maximum_number_of_vacancies,
            }
        response = requests.get(url_sj, headers=auth_token, params=params)
        response.raise_for_status()
        vacancies.append(response.json())
        total_vacancies = vacancies[entrance]['total']
        page += 1
        number_of_possible_vacancies += 100
    return vacancies[entrance]
