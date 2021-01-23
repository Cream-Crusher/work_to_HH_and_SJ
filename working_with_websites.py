import os
from terminaltables import SingleTable
from dotenv import load_dotenv
from hh import get_information_from_hh, get_vacancies_hh
from sj import get_information_from_sj, get_vacancies_sj


def get_collecting_information(processed_vacancies, average_salary,
                              information_on_vacancies
    ):
    information_on_vacancies_for_the_table = {}
    information_on_vacancies_for_the_table.update({
        information_on_vacancies['language']: {
        'vacancies_found': information_on_vacancies['found'],
        'processed_vacancies': processed_vacancies,
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
                        site_name, table_data
                        ):
    table_parameters = (
        language,
        information_on_vacancies[language]['vacancies_found'],
        information_on_vacancies[language]['processed_vacancies'],
        information_on_vacancies[language]['average_salary']
        )
    table_data.append(table_parameters)
    table_instance = SingleTable(table_data, '{} Moscow'.format(site_name))
    return table_instance


def get_salary_and_vacancies_processed(information_on_vacancies,
                                        processed_vacancies
                                        ):
    salary_and_vacancies_processed = {}
    pay_from = information_on_vacancies['pay_from']
    pay_to = information_on_vacancies['pay_to']
    salary = 0

    if information_on_vacancies['currency'] == 'RUR' or pay_from or \
        pay_to and information_on_vacancies['currency'] == 'rub':

        salary = predict_rub_salary(pay_from, pay_to)

    else:
        processed_vacancies -= 1

    salary_and_vacancies_processed = {'salary': salary,
                                      'processed_vacancies': processed_vacancies
                                      }
    return salary_and_vacancies_processed


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN_SUPERJOB')
    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']]
    programming_languages = ['Go']
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
    entrance = 0

    for language in programming_languages:
        all_vacancies = get_information_from_hh(language)
        site_name = 'HeadHunter'
        information_on_vacancies = get_vacancies_hh(all_vacancies, language)
        processed_vacancies = information_on_vacancies[entrance]["found"]
        salary = 0

        for information_on_vacancies in information_on_vacancies:
            salary_and_vacancies_processed = get_salary_and_vacancies_processed(
                                            information_on_vacancies, processed_vacancies
                                            )
            salary += salary_and_vacancies_processed['salary']
            processed_vacancies = salary_and_vacancies_processed['processed_vacancies']


        average_salary = int(salary / processed_vacancies)

        information_on_vacancies = get_collecting_information(processed_vacancies, average_salary,                                                              information_on_vacancies
                                                            )
        table_with_data_on_vacancies_hh = get_building_table(information_on_vacancies,
                                                            language, site_name, table_data
                                                            )
    print(table_with_data_on_vacancies_hh.table)

    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']]

    for language in programming_languages:
        all_vacancies = get_information_from_sj(language, token)
        information_on_vacancies = get_vacancies_sj(all_vacancies, language)
        site_name = 'SuperJob'
        salary = 0
        processed_vacancies = information_on_vacancies[entrance]['found']

        for information_on_vacancies in information_on_vacancies:

            salary_and_vacancies_processed = get_salary_and_vacancies_processed(information_on_vacancies,
                                                                                processed_vacancies
                                                                                )

            salary += salary_and_vacancies_processed['salary']
            processed_vacancies = salary_and_vacancies_processed['processed_vacancies']

        average_salary = int(salary / processed_vacancies)
        information_on_vacancies = get_collecting_information(processed_vacancies,
                                                            average_salary, information_on_vacancies
                                                            )
        table_with_data_on_vacancies_sj = get_building_table(information_on_vacancies,
                                                            language, site_name, table_data
                                                            )

    print(table_with_data_on_vacancies_sj.table)
