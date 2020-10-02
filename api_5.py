import requests
import os
from terminaltables import SingleTable
from dotenv import load_dotenv


def calculate_the_average_salary(
    the_total_salary,
        vacancies_processed):
    average_salary = (the_total_salary / vacancies_processed)
    return average_salary


def dictionary_of_site_headhunter(page, language, url_hh):
    payload = {'text': 'Программист {}'.format(
        language), 'area': '1', 'period': '30', 'per_page': '100',
        'page': '{}'.format(page), 'only_with_salary': 'True'}
    response = requests.get(url_hh, params=payload)
    response.raise_for_status()
    return response


def predict_rub_salary(information_on_vacancies, number_of_vacancies_per_page):
    salary = information_on_vacancies['items'][
        number_of_vacancies_per_page]['salary']
    return salary


def dictionary_of_site_sj(token, url_sj, language):
    auth_token = {'X-Api-App-Id': '{}'.format(token)}
    params = {'keyword': '{}'.format(
        language), 'town': 4, 'catalogues': 48, 'count': 100}
    response = requests.get(url_sj, headers=auth_token, params=params)
    response.raise_for_status()
    return response


def processed_data_by_language(
    information_about_a_specific_language,
        language):
    programming_languages_statistics = ([language, '{}'.format(
          information_about_a_specific_language[0]['vacancies_found']), '{}'
          .format(information_about_a_specific_language[0][
            'vacancies_processed']), '{}'
          .format(information_about_a_specific_language[0]['average_salary'])])
    return programming_languages_statistics


def predict_rub_salary_for_superjo(one_vacancy_in_sj):
    salary_jobs_sj = one_vacancy_in_sj['payment_from']
    return salary_jobs_sj


def collecting_information_about_vacancies_sj(
    number_of_vacancies_sj,
        vacancies_processed, average_salary):
    information_on_vacancies_in_sj.update({
        language: {
            'vacancies_found': len(number_of_vacancies_sj),
            'vacancies_processed':
                vacancies_processed, 'average_salary': int(
                  average_salary)}})
    return information_on_vacancies_in_sj


def collecting_information_about_vacancies_hh(
    languages,
        vacancies_sj,
        processed_vacancies_in_each_language,
        the_average_salary_for_language):
    information_on_vacancies_in_hh.update(({languages[id_language]: {
      'vacancies_found': number_of_vacancies[id_language],
      'vacancies_processed': processed_vacancies_in_each_language[
          id_language], 'average_salary': int(
        the_average_salary_for_language[id_language])}}))
    return information_on_vacancies_in_hh


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
    information_about_job_vacancies_hh = []
    information_about_job_vacancies_sj = []
    token = os.getenv('TOKEN_SUPERJOB')
    the_average_salary_for_language = []
    languages = []
    number_of_vacancies = []
    processed_vacancies_in_each_language = []
    url_hh = 'https://api.hh.ru/vacancies'
    url_sj = 'https://api.superjob.ru/2.0/vacancies'
    information_on_vacancies_in_hh = {}
    information_on_vacancies_in_sj = {}
    for language in programming_languages:
        full_salary = 0
        vacancies_processed = 0
        average_salary = 0
        vacancies_sj = (dictionary_of_site_sj(
            token, url_sj, language).json()["objects"])
        for separate_vacancy in range(len(vacancies_sj)):
            one_vacancy_in_sj = vacancies_sj[separate_vacancy]
            salary_jobs_sj = predict_rub_salary_for_superjo(one_vacancy_in_sj)
            if salary_jobs_sj != 0:
                vacancies_processed += 1
                full_salary += salary_jobs_sj
            if vacancies_processed != 0:
                average_salary = full_salary / vacancies_processed
            information_on_vacancies_in_sj = (
                collecting_information_about_vacancies_sj(
                    vacancies_sj,
                    vacancies_processed, average_salary))
    for language in programming_languages:
        number_of_requests = 0
        page = 0
        vacancies_processed = 0
        average_salary = 0
        the_total_salary = 0
        pages_number = dictionary_of_site_headhunter(
            page, language, url_hh).json()['pages']
        information_on_vacancies = (dictionary_of_site_headhunter(
            page, language, url_hh).json())
        for iteration_by_number_of_pages in range(pages_number):
            number_of_requests = number_of_requests + len(
              information_on_vacancies['items'])
            number_of_requests_per_page = len(
              information_on_vacancies['items'])
            for number_of_vacancies_per_page in range(
              number_of_requests_per_page):
                salary_for_the_work = predict_rub_salary(
                  information_on_vacancies, number_of_vacancies_per_page)
                if salary_for_the_work['from']:
                    vacancies_processed += 1
                    the_total_salary += salary_for_the_work['from']
        the_average_salary_for_language.append(calculate_the_average_salary(
          the_total_salary, vacancies_processed))
        languages.append(language)
        number_of_vacancies.append(number_of_requests)
        processed_vacancies_in_each_language.append(vacancies_processed)
    for id_language in range(len(programming_languages)):
        information_on_vacancies_in_hh = (
            collecting_information_about_vacancies_hh(
                languages, number_of_vacancies,
                processed_vacancies_in_each_language,
                the_average_salary_for_language))
    information_about_job_vacancies_hh.append(table_data)
    for language in information_on_vacancies_in_hh:
        information_about_a_specific_language = [
            information_on_vacancies_in_hh[language]]
        information_about_job_vacancies_hh.append(
            processed_data_by_language(
                information_about_a_specific_language, language))
        table_instance_HH = SingleTable(
            information_about_job_vacancies_hh, 'HeadHunter Moscow')
    information_about_job_vacancies_sj.append(table_data)
    for language in information_on_vacancies_in_sj:
        information_about_a_specific_language = [
          information_on_vacancies_in_sj[language]]
        information_about_job_vacancies_sj.append(
          processed_data_by_language(
                information_about_a_specific_language, language))
        table_instance_sj = SingleTable(
                information_about_job_vacancies_sj, 'SuperJob {}'.format(
                    one_vacancy_in_sj["town"]['title']))
    print(table_instance_sj.table)
    print(table_instance_HH.table)
