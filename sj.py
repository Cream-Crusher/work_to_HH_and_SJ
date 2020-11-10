import requests


def adding_information_about_vacancies_from_the_sj_website(
    token,
        url_sj, language,
        name_town=4,
        catalogue_designation=48,
        maximum_number_of_vacancies=100):
    auth_token = {'X-Api-App-Id': '{}'.format(token)}
    params = {'keyword': '{}'.format(
        language), 'town': name_town, 'catalogues': catalogue_designation,
        'count': maximum_number_of_vacancies}
    response = requests.get(url_sj, headers=auth_token, params=params)
    response.raise_for_status()
    return response


def predict_rub_salary_for_superjo(one_vacancy_in_SJ):
    salary_jobs_sj = one_vacancy_in_SJ
    return salary_jobs_sj
