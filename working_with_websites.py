import os
import copy
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


def get_information_for_the_table(information_on_vacancies):

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
    information_for_the_table = {'processed_vacancies': processed_vacancies,
                                    'found': information_on_vacancies['found'],
                                    'average_salary': average_salary
                                    }
    return information_for_the_table


def building_table(site_name, header_table, information_on_vacancies, language):

    table_data = copy.copy(header_table)
    print(language)
    information_for_the_table = get_information_for_the_table(information_on_vacancies)
    #for information_on_vacancies in information_on_vacancies:
    found = information_for_the_table['found']
    processed_vacancies = information_for_the_table['processed_vacancies']
    average_salary = information_for_the_table['average_salary']
    table_parameters = (
        language,
        found,
        processed_vacancies,
        average_salary
        )
    table_data.append(table_parameters)
    table_instance = SingleTable(table_data, '{} Moscow'.format(site_name))

    return table_instance


def get_table_hh(programming_languages):

    site_name = 'HeadHunter'
    header_table = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']]
    information_on_vacancies = []
    
    for language in programming_languages:
        all_vacancies = get_information_from_hh(language)
        information_on_vacancies = get_vacancies_hh(all_vacancies, language)

    table_with_data_on_vacancies_hh = building_table(site_name, header_table,
                                                    information_on_vacancies,
                                                    language
                                                    )
    print(table_with_data_on_vacancies_hh.table)


def get_table_sj(programming_languages):

    token = os.getenv('TOKEN_SUPERJOB')
    site_name = 'SuperJob'
    header_table = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']]
    information_on_vacancies = []

    for language in programming_languages:
        all_vacancies = get_information_from_sj(language, token)
        information_on_vacancies = get_vacancies_sj(all_vacancies, language)

    table_with_data_on_vacancies_sj = building_table(site_name, header_table,
                                                    information_on_vacancies,
                                                    language
                                                    )
    print(table_with_data_on_vacancies_sj.table)


if __name__ == '__main__':
    load_dotenv()
    programming_languages = ['Go', 'Go']
    '''
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
    '''
    get_table_hh(programming_languages)
    #get_table_sj(programming_languages)
