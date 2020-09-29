import requests
import json
import os
from terminaltables import SingleTable
from dotenv import load_dotenv



def counting_data_for_statistics(the_total_salary,
vacancies_processed, language, number_of_requests):
    average_salary = (the_total_salary / vacancies_processed)
    the_average_salary_for_language.append(average_salary)
    languages.append(language)
    number_of_vacancies.append(number_of_requests)
    processed_vacancies_in_each_language.append(vacancies_processed)


def link_to_the_HeadHunter_job_page(page, language, url_hh):
    payload = {'text': 'Программист {}'.format(
        language), 'area': '1', 'period': '30', 'per_page': '100',
        'page': '{}'.format(page), 'only_with_salary': 'True'}
    response = requests.get(url_hh, params=payload)
    response.raise_for_status()
    return response


def predict_rub_salary(json_text, number_of_vacancies_per_page):
    json_text = json_text['items'][number_of_vacancies_per_page]['salary']
    return json_text


def link_to_the_superjob_job_page(token, url_SJ, language):
    auth_token = {'X-Api-App-Id': '{}'.format(token)}
    params = {'keyword': '{}'.format(
        language), 'town': 4, 'catalogues': 48, 'count': 100}
    response = requests.get(url_SJ, headers=auth_token, params=params)
    response.raise_for_status()
    return response


def predict_rub_salary_for_SuperJo(one_vacancy_in_SJ):
    salary_jobs_SJ = one_vacancy_in_SJ['payment_from']
    return salary_jobs_SJ


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
    NUMBER_OF_LANGUAGES = 13
    table_data_HH = []
    table_data_SJ = []
    token = os.getenv('TOKEN_SUPERJOB')
    the_average_salary_for_language = []
    languages = []
    number_of_vacancies = []
    processed_vacancies_in_each_language = []
    url_hh = 'https://api.hh.ru/vacancies'
    url_SJ = 'https://api.superjob.ru/2.0/vacancies'
    information_on_vacancies_in_hh = {}
    information_on_vacancies_in_SJ = {}
    for language in programming_languages:
        full_salary = 0
        vacancies_processed = 0
        average_salary = 0
        number_of_vacancies_SJ = len(link_to_the_superjob_job_page(
            token, url_SJ, language).json()["objects"])
        oll_vacancy_in_SJ = link_to_the_superjob_job_page(
            token, url_SJ, language).json()["objects"]
        for separate_vacancy in range(0, number_of_vacancies_SJ):
            one_vacancy_in_SJ = oll_vacancy_in_SJ[separate_vacancy]
            salary_jobs_SJ = predict_rub_salary_for_SuperJo(one_vacancy_in_SJ)
            if salary_jobs_SJ != 0:
                vacancies_processed += 1
                full_salary += salary_jobs_SJ
            if vacancies_processed != 0:
                average_salary = full_salary / vacancies_processed
            information_on_vacancies_in_SJ.update({
                language: {'vacancies_found': number_of_vacancies_SJ,
            'vacancies_processed': vacancies_processed, 'average_salary': int(
                average_salary)}})
    for language in programming_languages:
        number_of_requests = 0
        page = 0
        vacancies_processed = 0
        average_salary = 0
        the_total_salary = 0
        pages_number = link_to_the_HeadHunter_job_page(
            page, language, url_hh).json()['pages']
        json_text = (json.loads(link_to_the_HeadHunter_job_page(
            page, language, url_hh).text))
        for iteration_by_number_of_pages in range(0, pages_number):
            number_of_requests = number_of_requests + len(json_text['items'])
            number_of_requests_per_page = len(json_text['items'])
            while page + 1 < pages_number:
                page += 1
            for number_of_vacancies_per_page in range(
              0, number_of_requests_per_page):
                salary_for_the_work = predict_rub_salary(
                  json_text, number_of_vacancies_per_page)
                if salary_for_the_work['from']:
                    vacancies_processed += 1
                    the_total_salary += salary_for_the_work['from']
        counting_data_for_statistics(
            the_total_salary, vacancies_processed, language, number_of_requests
        )
    for id_language in range(0, NUMBER_OF_LANGUAGES):
        information_on_vacancies_in_hh.update(({languages[id_language]: {
            'vacancies_found': number_of_vacancies[id_language],
            'vacancies_processed': processed_vacancies_in_each_language[
                id_language], 'average_salary': int(
              the_average_salary_for_language[id_language])}}))
    table_data_HH.append([
          'Язык программирования',
          'Вакансий найдено',
          'Вакансий обработано',
          'Средняя зарплата'])
    for language in information_on_vacancies_in_hh:
        information_about_a_specific_language = [
            information_on_vacancies_in_hh[language]]
        table_data_HH.append([language, '{}'.format(
                information_about_a_specific_language[0]
                ['vacancies_found']), '{}'.format(
                information_about_a_specific_language[0]
                ['vacancies_processed']), '{}'.format(
                information_about_a_specific_language[0]
                ['average_salary'])])
        table_instance_HH = SingleTable(
            table_data_HH, 'HeadHunter Moscow')
    table_data_SJ.append([
          'Язык программирования',
          'Вакансий найдено',
          'Вакансий обработано',
          'Средняя зарплата'])
    for language in information_on_vacancies_in_SJ:
        information_about_a_specific_language = [
          information_on_vacancies_in_SJ[language]]
        table_data_SJ.append([language, '{}'.format(
          information_about_a_specific_language[0]['vacancies_found']), '{}'
          .format(information_about_a_specific_language[0][
            'vacancies_processed']), '{}'
          .format(information_about_a_specific_language[0]['average_salary'])])
        table_instance_SJ = SingleTable(table_data_SJ, 'SuperJob {}'.format(
          one_vacancy_in_SJ["town"]['title']))
    print(table_instance_SJ.table)
    print(table_instance_HH.table)
