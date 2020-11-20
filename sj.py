import requests


def get_information_from_sj(token, url_sj,
                            language, name_town=4,
                            catalogue_designation=48,
                            maximum_number_of_vacancies=100):
    auth_token = {
        'X-Api-App-Id': '{}'.format(token)
        }
    params = {
        'keyword': language,
        'town': name_town,
        'catalogues': catalogue_designation,
        'count': maximum_number_of_vacancies
        }
    response = requests.get(url_sj, headers=auth_token, params=params)
    response.raise_for_status()
    return response
