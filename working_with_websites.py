import os
from terminaltables import SingleTable
from dotenv import load_dotenv
from hh import get_information_from_hh, get_vacancies_hh
from sj import get_information_from_sj, get_vacancies_sj

TOKEN = os.getenv('TOKEN_SUPERJOB')


def get_collecting_information(vacancies_processed, average_salary,
                              information_on_vacancies
    ):
    information_on_vacancies_for_the_table = {}
    information_on_vacancies_for_the_table.update({
        information_on_vacancies['language']: {
        'vacancies_found': information_on_vacancies['found'],
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary}}
    )
    return information_on_vacancies_for_the_table


def predict_rub_salary(pay_from, pay_to):

    if pay_from and pay_to:
        return (pay_from + pay_to) / 2
    elif pay_from:
        return pay_from * 1.2
    elif pay_to:
        return pay_to * 0.8
    else:
        return


def get_building_table(information_on_vacancies, language,
                      name_site, table_data
    ):
    table_parameters = (
    language,
    information_on_vacancies[language]['vacancies_found'],
    information_on_vacancies[language]['vacancies_processed'],
    information_on_vacancies[language]['average_salary']
    )
    table_data.append(table_parameters)
    table_instance = SingleTable(table_data, '{} Moscow'.format(name_site))
    return table_instance


def get_salary_and_vacancies_processed(information_on_vacancies,
                                        vacancies_processed
    ):
    salary_and_vacancies_processed = {}
    pay_from = information_on_vacancies['pay_from']
    pay_to = information_on_vacancies['pay_to']
    salary = 0

    if information_on_vacancies['currency'] == 'RUR' or pay_from or \
        pay_to and information_on_vacancies['currency'] == 'rub':

        salary = predict_rub_salary(pay_from, pay_to)

    else:
        vacancies_processed -= 1

    salary_and_vacancies_processed = {'salary': salary,
                                      'vacancies_processed': vacancies_processed
                                      }
    return salary_and_vacancies_processed


if __name__ == '__main__':
    load_dotenv()
    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']]
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
    entrance = 0

    for language in programming_languages:
        all_vacancies = get_information_from_hh(language)
        name_site = 'HeadHunter'
        information_on_vacancies = get_vacancies_hh(all_vacancies, language)
        vacancies_processed = information_on_vacancies[entrance]["found"]
        salary = 0

        for information_on_vacancies in information_on_vacancies:
            salary_and_vacancies_processed = get_salary_and_vacancies_processed(
                                            information_on_vacancies, vacancies_processed
            )
            salary += salary_and_vacancies_processed['salary']
            vacancies_processed = salary_and_vacancies_processed['vacancies_processed']


        average_salary = int(salary / vacancies_processed)
        information_on_vacancies = get_collecting_information(vacancies_processed, average_salary,                                                                          information_on_vacancies
        )
        table_with_data_on_vacancies_hh = get_building_table(information_on_vacancies,
                                                        language, name_site, table_data
        )
    print(table_with_data_on_vacancies_hh.table)

    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']]

    for language in programming_languages:
        all_vacancies = get_information_from_sj(language, TOKEN)
        information_on_vacancies = get_vacancies_sj(all_vacancies, language)
        name_site = 'SuperJob'
        salary = 0
        vacancies_processed = information_on_vacancies[entrance]['found']

        for information_on_vacancies in information_on_vacancies:

            salary_and_vacancies_processed = get_salary_and_vacancies_processed(information_on_vacancies,
                                                                                vacancies_processed
            )

            salary += salary_and_vacancies_processed['salary']
            vacancies_processed = salary_and_vacancies_processed['vacancies_processed']

        average_salary = int(salary / vacancies_processed)
        information_on_vacancies = get_collecting_information(vacancies_processed,
                                                              average_salary, information_on_vacancies
        )
        table_with_data_on_vacancies_sj = get_building_table(information_on_vacancies,
                                                        language, name_site, table_data
        )

    print(table_with_data_on_vacancies_sj.table)
