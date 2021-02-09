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


def get_information_for_the_table(information_on_vacancies, language, site_name):
    salary = 0
    entrance = 0
    vacancies_found = information_on_vacancies[entrance]["found"]
    processed_vacancies = vacancies_found

    for information_on_vacancies in information_on_vacancies:
        pay_from = information_on_vacancies['pay_from']
        pay_to = information_on_vacancies['pay_to']

        if information_on_vacancies['currency'] == 'RUR' or pay_from or pay_to and \
            information_on_vacancies['currency'] == 'rub':

            salary += predict_rub_salary(pay_from, pay_to)

        else:
            processed_vacancies -= 1

    average_salary = int(salary / processed_vacancies)
    table_with_data_on_vacancies = {
                                    language:
                                            {
                                            'vacancies_found': vacancies_found,
                                            'vacancies_processed': processed_vacancies,
                                            'average_salary': average_salary
                                            }
                                        }

    return table_with_data_on_vacancies


def get_table(programming_languages):
    token = os.getenv('TOKEN_SUPERJOB')
    site_name = ['hh', 'sj']

    for site_name in site_name: 
        vacancies = []
 
        for language in programming_languages:

            if site_name == 'hh':
                all_vacancies = get_information_from_hh(language)
                information_on_vacancies = get_vacancies_hh(all_vacancies, language)
                vacancies.append(get_information_for_the_table(information_on_vacancies,
                                                                language, site_name)
                                                                )

            if site_name == 'sj':
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
    get_table(programming_languages)
