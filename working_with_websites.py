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
    else:
        return


def get_building_table(site_name, table_data, information_on_vacancies):

    salary = 0
    entrance = 0
    processed_vacancies = information_on_vacancies[entrance]["found"]

    for information_on_vacancies in information_on_vacancies:
        pay_from = information_on_vacancies['pay_from']
        pay_to = information_on_vacancies['pay_to']

        if information_on_vacancies['currency'] == 'RUR' or pay_from or pay_to and \
            information_on_vacancies['currency'] == 'rub':

            salary += predict_rub_salary(pay_from, pay_to)

        else:
            processed_vacancies -= 1

    average_salary = int(salary / processed_vacancies)
    table_parameters = (
        language,
        information_on_vacancies['found'],
        processed_vacancies,
        average_salary
        )
    table_data.append(table_parameters)
    table_instance = SingleTable(table_data, '{} Moscow'.format(site_name))

    return table_instance


if __name__ == '__main__':
    load_dotenv()
    programming_languages = [
        'JavaScript',
        'Java',
        'PHP',
        'Python',
        'Ruby',
        'C++',
        'C#',
        'C',
        'Scala',
        'Go',
        'Swift',
        'Typescript']
    site_name = 'HeadHunter'
    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']]

    for language in programming_languages:
        all_vacancies = get_information_from_hh(language)
        information_on_vacancies = get_vacancies_hh(all_vacancies, language)
        table_with_data_on_vacancies_hh = get_building_table(site_name, table_data,
                                                            information_on_vacancies
                                                            )
    print(table_with_data_on_vacancies_hh.table)

    token = os.getenv('TOKEN_SUPERJOB')
    site_name = 'SuperJob'
    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']]

    for language in programming_languages:
        all_vacancies = get_information_from_sj(language, token)
        information_on_vacancies = get_vacancies_sj(all_vacancies, language)
        table_with_data_on_vacancies_sj = get_building_table(site_name, table_data,
                                                            information_on_vacancies
                                                            )
    print(table_with_data_on_vacancies_sj.table)
