import os
from terminaltables import SingleTable
from dotenv import load_dotenv
from hh import get_information_from_hh, get_vacancies_hh
from sj import get_information_from_sj, get_vacancies_sj


def predict_rub_salary(pay_from, pay_to):

    if pay_from and pay_to:
        return (pay_from + pay_to) / 2
    elif pay_from:
        return pay_from * 1.2
    elif pay_to:
        return pay_to * 0.8


def get_information_for_the_table(information_on_vacancies, language, site_name):
    full_salary = 0
    entrance = 0
    vacancies_found = information_on_vacancies[entrance]["found"]
    processed_vacancies = 0

    for information_on_vacancies in information_on_vacancies:
        pay_from = information_on_vacancies['pay_from']
        pay_to = information_on_vacancies['pay_to']

        if information_on_vacancies['currency'] == 'RUR'  or \
            information_on_vacancies['currency'] == 'rub':
            salary = predict_rub_salary(pay_from, pay_to)

            if salary != None:
                processed_vacancies += 1
                full_salary += salary

    average_salary = int(full_salary / processed_vacancies)
    data_on_vacancies = {
                                    language:
                                            {
                                            'vacancies_found': vacancies_found,
                                            'vacancies_processed': processed_vacancies,
                                            'average_salary': average_salary
                                            }
                                        }

    return data_on_vacancies


def get_table_hh(programming_languages):
    site_name = 'hh'
    vacancies = []

    for language in programming_languages:
        all_vacancies = get_information_from_hh(language)
        information_on_vacancies = get_vacancies_hh(all_vacancies, language)
        vacancies.append(get_information_for_the_table(information_on_vacancies,
                                                        language, site_name)
                                                        )
    print_vacancy_info(site_name, vacancies)


def get_table_sj(programming_languages, token):
    site_name = 'sj'
    vacancies = []

    for language in programming_languages:
        all_vacancies = get_information_from_sj(language, token)
        information_on_vacancies = get_vacancies_sj(all_vacancies, language)
        vacancies.append(get_information_for_the_table(information_on_vacancies,
                                                        language, site_name)
                                                        )
    print_vacancy_info(site_name, vacancies)


def print_vacancy_info(site_name, vacancies):
    table_data = [
    [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата'
    ]
    ]

    for vacancies in vacancies:
        for language in vacancies:

            table_data.append([
                language,
                vacancies[language]['vacancies_found'],
                vacancies[language]['vacancies_processed'],
                vacancies[language]['average_salary']
                ])
        table_instance = SingleTable(table_data, site_name)
    print(table_instance.table)


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN_SUPERJOB')
    programming_languages = [
        'JavaScript',
        'Java',
        'PHP',
        'Python',
        'Ruby',
        'C++',
        'C#',
        'C',
        'Go',
        'Typescript']
    get_table_hh(programming_languages)
    get_table_sj(programming_languages, token)
