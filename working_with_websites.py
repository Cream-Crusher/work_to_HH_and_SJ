import os
from terminaltables import SingleTable
from dotenv import load_dotenv
from hh import (calculate_the_average_salary, predict_rub_salary,
                get_information_from_hh)
from sj import (get_information_from_sj)


def processed_data_by_language(information_about_specific_language, language):
    programming_languages_statistics = [
      language,
      information_about_specific_language['vacancies_found'],
      information_about_specific_language['vacancies_processed'],
      information_about_specific_language['average_salary']
    ]
    return programming_languages_statistics


def collecting_information_hh(languages, vacancies_sj,
                              processed_vacancies_each_language,
                              the_average_salary_for_language):
    information_vacancies_in_hh.update({
      languages[id_language]:
      {'vacancies_found': number_of_vacancies[id_language],
      'vacancies_processed': processed_vacancies_each_language[id_language],
      'average_salary': int(the_average_salary_for_language[id_language])}}
    )
    return information_vacancies_in_hh


def collecting_information_sj(number_of_vacancies_sj,
                              vacancies_processed,
                              average_salary):
    information_on_vacancies_in_sj.update({
        language: {
        'vacancies_found': len(number_of_vacancies_sj),
        'vacancies_processed': vacancies_processed,
        'average_salary': int(average_salary)}}
    )
    return information_on_vacancies_in_sj


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
      'Go',
      'Objective-C',
      'Scala',
      'Swift',
      'Typescript']
    table_data = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата']
    the_average_salary_for_language = []
    languages = []
    number_of_vacancies = []
    processed_vacancies_each_language = []
    url_hh = 'https://api.hh.ru/vacancies'
    url_sj = 'https://api.superjob.ru/2.0/vacancies'
    information_vacancies_in_hh = {}
    information_on_vacancies_in_sj = {}
    information_about_job_vacancies_sj = []
    information_about_job_vacancies_hh = []
    token = os.getenv('TOKEN_SUPERJOB')

    for language in programming_languages:
        number_of_requests = 0
        page = 0
        vacancies_processed = 0
        average_salary = 0
        the_total_salary = 0
        pages_number = get_information_from_hh(page, language, url_hh).json()['pages']

        while page < pages_number + 1:
            page += 1
            information_on_vacancies = get_information_from_hh(page, language, url_hh).json()
            number_of_requests = number_of_requests + len(information_on_vacancies['items'])
            number_of_requests_per_page = len(information_on_vacancies['items'])

            for number_of_vacancies_per_page in range(number_of_requests_per_page):
                salary_for_work = predict_rub_salary(
                        information_on_vacancies, number_of_vacancies_per_page
                )

                if salary_for_work['from'] and salary_for_work['to']:
                    vacancies_processed += 1
                    the_total_salary += (salary_for_work['from'] + salary_for_work['to']) / 2

                if salary_for_work['from'] is None:
                    vacancies_processed += 1
                    the_total_salary += salary_for_work['to'] * 0.8

                if salary_for_work['to'] is None:
                    vacancies_processed += 1
                    the_total_salary += salary_for_work['from'] * 1.2

        if vacancies_processed:
            the_average_salary_for_language.append(
                    calculate_the_average_salary(the_total_salary, vacancies_processed)
            )
        else:
            the_average_salary_for_language.append(0)

        languages.append(language)
        number_of_vacancies.append(number_of_requests)
        processed_vacancies_each_language.append(vacancies_processed)

    for id_language in range(len(programming_languages)):
        information_vacancies_in_hh = collecting_information_hh(
                    languages, number_of_vacancies,
                    processed_vacancies_each_language,
                    the_average_salary_for_language
                )
    information_about_job_vacancies_hh.append(table_data)

    for language in information_vacancies_in_hh:
        information_about_specific_language = (
                information_vacancies_in_hh[language]
        )
        information_about_job_vacancies_hh.append(
            processed_data_by_language(information_about_specific_language, language)
        )
        table_instance_HH = SingleTable(
            information_about_job_vacancies_hh,
            'HeadHunter Moscow'
        )

    for language in programming_languages:
        full_salary = 0
        vacancies_processed = 0
        average_salary = 0
        vacancies_sj = get_information_from_sj(token, url_sj, language).json()["objects"]

        for separate_vacancy in range(len(vacancies_sj)):
            one_vacancy_in_SJ = vacancies_sj[separate_vacancy]
            salary_jobs_sj = one_vacancy_in_SJ

            if salary_jobs_sj['payment_to'] and salary_jobs_sj['payment_from']:
                vacancies_processed += 1
                full_salary += (salary_jobs_sj['payment_to'] + salary_jobs_sj['payment_from']) / 2

            if salary_jobs_sj['payment_to'] and salary_jobs_sj['payment_from'] == 0:
                vacancies_processed += 1
                full_salary += salary_jobs_sj['payment_to'] * 0.8

            if salary_jobs_sj['payment_from'] and salary_jobs_sj['payment_to'] == 0:
                vacancies_processed += 1
                full_salary += salary_jobs_sj['payment_from'] * 1.2

            if vacancies_processed:
                average_salary = full_salary / vacancies_processed
            
            information_on_vacancies_in_sj = collecting_information_sj(
                vacancies_sj, vacancies_processed, average_salary
                )

    information_about_job_vacancies_sj.append(table_data)

    for language in information_on_vacancies_in_sj:
        information_about_specific_language = (
                information_on_vacancies_in_sj[language]
        )
        information_about_job_vacancies_sj.append(
            processed_data_by_language(information_about_specific_language, language)
        )
        table_instance_SJ = SingleTable(
                information_about_job_vacancies_sj,
                'SuperJob {}'.format(one_vacancy_in_SJ["town"]['title'])
        )
    print(table_instance_SJ.table)
    print(table_instance_HH.table)
