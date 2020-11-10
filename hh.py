import requests


def calculate_the_average_salary(
    the_total_salary,
        vacancies_processed):
    average_salary = (the_total_salary / vacancies_processed)
    return average_salary


def adding_information_about_vacancies_from_the_hh_website(
    page,
        language, url_hh,
        City=1,
        max_page=100,
        max_number_of_days=30):
    payload = {'text': 'Программист {}'.format(
        language), 'area': City, 'period': max_number_of_days,
        'per_page': max_page,
        'page': '{}'.format(page), 'only_with_salary': 'True'}
    response = requests.get(url_hh, params=payload)
    response.raise_for_status()
    return response


def predict_rub_salary(information_on_vacancies, number_of_vacancies_per_page):
    salary = information_on_vacancies['items'][
        number_of_vacancies_per_page]['salary']
    return salary
