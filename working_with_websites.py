import os
from terminaltables import SingleTable
from dotenv import load_dotenv
from hh import get_information_from_hh, get_vacancies
from sj import get_information_from_sj

TOKEN = os.getenv('TOKEN_SUPERJOB')


def collecting_information(vacancies_found, vacancies_processed,
                              average_salary, language
    ):
    information_on_vacancies = {}
    information_on_vacancies.update({
        language: {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary}}
    )
    return information_on_vacancies


def predict_rub_salary(pay_from, pay_to):

    if  pay_from and pay_from < 1001:
        pay_from *= 1001

    if pay_to and pay_to < 1001:
        pay_from *= 1001

    if pay_from and pay_to:
        return (pay_from + pay_to) / 2
    elif pay_from:
        return pay_from * 1.2
    elif pay_to:
        return pay_to * 0.8
    else:
        return


def building_table(information_on_vacancies, language, table_data, name_site):
    table_data.append([
    language,
    information_on_vacancies[language]['vacancies_found'],
    information_on_vacancies[language]['vacancies_processed'],
    information_on_vacancies[language]['average_salary']
    ])
    table_instance = SingleTable(table_data, '{} Moscow'.format(name_site))
    return table_instance


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
        'Go',
        'Objective-C',
        'Scala',
        'Swift',
        'Typescript']
    entrance = 0

    for language in programming_languages:
        salary = 0
        vacancies = get_information_from_hh(language)
        name_site = 'HeadHunter'

        for vacancies in vacancies:
            vacancies = get_vacancies(vacancies)
            vacancies_found = vacancies["found"]
            vacancies_processed = vacancies_found

            for information_on_vacancies in vacancies['vacancies'][entrance]:

                if information_on_vacancies['salary']['currency'] == 'RUR':
                    pay_from = information_on_vacancies['salary']['from']
                    pay_to = information_on_vacancies['salary']['to']
                    salary += predict_rub_salary(pay_from, pay_to)

                else:
                    vacancies_processed -= 1

        average_salary = int(salary / vacancies_processed)
        information_on_vacancies = collecting_information(vacancies_found,
                                                          vacancies_processed,
                                                          average_salary, language,
        )


        table_with_data_on_vacancies_hh = building_table(information_on_vacancies,
                                                        language, table_data,
                                                        name_site
        )
    print(table_with_data_on_vacancies_hh.table)

    table_data = [[
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']]

    for language in programming_languages:
        vacancies = get_information_from_sj(language, TOKEN)
        vacancies_found = vacancies['total']
        vacancies_processed = vacancies_found
        name_site = 'SuperJob'
        salary = 0

        for information_on_vacancies in vacancies["objects"]:
            currency = information_on_vacancies['currency']
            pay_from = information_on_vacancies['payment_from']
            pay_to = information_on_vacancies['payment_to']

            if pay_from or pay_to and currency == 'rub':

                salary += predict_rub_salary(pay_to, pay_from)

            else:
                vacancies_processed -= 1

        average_salary = int(salary / vacancies_processed)

        information_on_vacancies = collecting_information(vacancies_found,
                                                          vacancies_processed,
                                                          average_salary, language,
        )
        table_with_data_on_vacancies_sj = building_table(information_on_vacancies,
                                                        language, table_data,
                                                        name_site
        )
    print(table_with_data_on_vacancies_sj.table)
