from __future__ import annotations

from pprint import pprint
from typing import Any, cast

import pandas as pd
import json

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk._models.completions.config import ReasoningMode
from yandex_cloud_ml_sdk._models.completions.result import GPTModelResult

from resume_analyser.utils.common import scrap_html, clean_html, clean_url
from tools.run_gpt import ModelRunner


# =======================================================================


JOB_SYSTEM_PROMPT = '''Ты HR-рекрутёр. У тебя есть html вакансии. 
Тебе необходимо выделить из неё название вакансии, в какую компанию или департамент требуется сотрудник и составить краткое описание на 1-2 (максимум 3) предложения.
В кратком описании указывай только самую суть. 

Также тебе необходимо выписать полное описание вакансии. Здесь должно быть выписано и красиво оформлено то, что на странице относится к исходному описанию вакансии. Тебе ничего нельзя придумывать самому. Используй только готовые фразы из html и оформи их. Все html теги тебе нужно удалить!


Ответ дай в формате json со следующей структурой:
{
 "название вакансии": "<название вакансии>",
 "компания или департамент": "<для какой компании или департамента требуется сотрудник>",
 "краткое описание вакансии": "<краткое описание вакансии>",
 "полное описание вакансии": "<полное описание вакансии>"
}
'''

RESUME_SYSTEM_PROMPT = '''Ты HR-рекрутёр. У тебя есть html резюме. 
Тебе необходимо выделить из него имя кандидата (или хотя бы название резюме), его город, опыт работы и составить краткое описание на 1-2 (максимум 3) предложения.
В кратком описании указывай только самую суть. 

Также тебе необходимо выписать полное описание резюме. Здесь должно быть выписано и красиво оформлено то, что на странице относится к исходному описанию резюме. Тебе ничего нельзя придумывать самому. Используй только готовые фразы из html и оформи их.

Ответ дай в формате json со следующей структурой:
{
 "название резюме": "<В идеале, ФИО кандидата из резюме. Если ФИО нет, то запиши хотя бы главный заголовок из резюме (например, "программист java")>",
 "город": "<город кандидата>",
 "опыт работы": "<кратко какой стаж работы 2-3 слова>",
 "краткое описание резюме": "<краткое описание резюме>",
 "полное описание резюме": "<полное описание резюме>"
}
'''


def main():
    vacancies_html_paths = ['~/Documents/проекты/TA/МТС/примеры резюме/Резюме Java-разработчик (Apache Kafka, Spring Boot, PostgreSQL), Москва, 200 000 руб. в месяц - найти Программиста-разработчика Java на SuperJob, опубликовано 03.07.2025 13_51.html']
    resumes_html_paths = [
        '~/Documents/проекты/TA/МТС/примеры вакансий сайт мтс/Разработчик Java (Middle) — вакансии в МТС Финтех — Москва.html',
        '~/Documents/проекты/TA/МТС/примеры резюме/Резюме Frontend‑разработчик (React _ JavaScript), Москва, по договоренности - найти Frontend-разработчика (Javascript) на SuperJob, опубликовано 14.06.2025 12_19_39.html',
        '~/Documents/проекты/TA/МТС/примеры резюме/Резюме Кладовщик-комплектовщик, Москва, 100 000 руб. в месяц - найти Кладовщика комплектовщика на SuperJob, опубликовано 03.02.2024 17_19_53.html'
    ]

    jobs_urls = [
        'https://job.mtsbank.ru/vacancies/moskva/razrabotchik-java-senior--1010747',
        'https://job.mtsbank.ru/vacancies/moskva/starshiy-razrabotchik-android--1010609',
    ]
    resumes_urls = [
        'https://www.superjob.ru/resume/junior-razrabotchik-54298502.html?fromSearch=true',
        'https://www.superjob.ru/resume/programmist-43784999.html?fromSearch=true',
        'https://www.superjob.ru/resume/veduschij-testirovschik-po-55594874.html?fromSearch=true',
        'https://www.superjob.ru/resume/java-razrabotchik-55757065.html?fromSearch=true',
        'https://www.superjob.ru/resume/frontend-razrabotchik-55708483.html?fromSearch=true',
        'https://www.superjob.ru/resume/prorab-55535973.html',
        'https://www.superjob.ru/resume/android-razrabotchik-55564268.html',
    ]

    # hh_resume_urls = [
    #     'https://hh.ru/resume/08c4c14800021d447b0039ed1f785254706d4d',
    # ]
    # res = scrap_html(url=hh_resume_urls[1])
    # print(res)

    model = ModelRunner()
    job = describe_job(job_url='https://yandex.ru/jobs/vacancies/produktoviy-analitik-v-neyroekspert-33189', model=model)
    pprint(list(job.keys()))

    pprint(job)

    # for key in ['name', 'city', 'experience', 'short_description']:
    #     print(key, resume[key], sep=':')

    return


def describe_job(job_url: str, model: ModelRunner, text_len_threshold: int = 65_000) -> dict[str, Any]:
    job_url = clean_url(url=job_url)

    html = scrap_html(url=job_url)
    if html is None:
        raise ValueError('None is unexpected')
    cleaned_html = clean_html(html=html)

    generated = model.run_text(
        model_uri='yandexgpt-lite',
        text=cleaned_html[:text_len_threshold],
        system_prompt=JOB_SYSTEM_PROMPT,
    )
    json_text = generated.text.replace('```', '').strip()

    data = cast(dict[str, Any], json.loads(json_text))
    data['url'] = job_url
    data['cleaned_html'] = cleaned_html
    # old_data['full_description'] = extract_text_from_html(html=cleaned_html, need_normalize=False)

    mapper = {
        'название вакансии': 'title',
        'компания или департамент': 'company',
        'краткое описание вакансии': 'short_description',
        'полное описание вакансии': 'full_description',
    }
    for old_key, new_key in mapper.items():
        data[new_key] = data[old_key]
        del data[old_key]

    return data


def describe_resume(resume_url: str, model: ModelRunner, text_len_threshold: int = 65_000) -> dict[str, Any]:
    resume_url = clean_url(url=resume_url)

    html = scrap_html(url=resume_url)
    if html is None:
        raise ValueError('None is unexpected')

    cleaned_html = clean_html(html=html)

    generated = model.run_text(
        model_uri='yandexgpt-lite',
        text=cleaned_html[:text_len_threshold],
        system_prompt=RESUME_SYSTEM_PROMPT,
    )
    # todo.md: tbd error
    json_text = generated.text.replace('```', '').strip()

    data = cast(dict[str, Any], json.loads(json_text))
    data['url'] = resume_url
    data['cleaned_html'] = cleaned_html
    # old_data['full_description'] = extract_text_from_html(html=cleaned_html, need_normalize=False)

    mapper = {
        'название резюме': 'name',
        'город': 'city',
        'опыт работы': 'experience',
        'краткое описание резюме': 'short_description',
        'полное описание резюме': 'full_description',
    }
    for old_key, new_key in mapper.items():
        data[new_key] = data[old_key]
        del data[old_key]

    return data


if __name__ == '__main__':
    main()
