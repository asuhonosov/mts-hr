from __future__ import annotations

from typing import Any
from itertools import product

import pandas as pd
import json

from yandex_cloud_ml_sdk import YCloudML
from yandex_cloud_ml_sdk._models.completions.config import ReasoningMode
from yandex_cloud_ml_sdk._models.completions.result import GPTModelResult

from resume_analyser.utils.common import read_html_text
from tools.run_gpt import ModelRunner


# =======================================================================


FULL_COMPARING_SYSTEM_PROMPT = '''Ты HR-рекрутёр. Тебе необходимо сравнить текст вакансии и текст резюме. Обращай внимание на специальность, опыт, требованиям и зарплатные ожидания в резюме кандидата и в описании вакансии.

По итогу сделай вывод, насколько кандидат с данным резюме соответствует данной вакансии. 
Также можешь выписать отдельные цитаты из резюме, где кандидат хорошо подходит, где есть сомнения, а где НЕ подходит. Выписывай именно цитаты, а не свои размышления.

Также тебе нужно выдать процент схожести. Не занижай её. Даже если кандидат не подходит, но у него в резюме есть что-то перекликающееся с вакансией, то это уже ТОЧНО больше 0 процентов схожести.
Но и не завышай процент слишком сильно. Если ты склоняешься к "есть сомнения", то процент должен быть 50% +- 10% (в зависимости от информации в резюме и вакансии).

Ответ дай в формате json со следующей структурой:
{
 "размышления о кандидате": "<твои подробные размышления о кандидате, чтобы принять окончательное решение>",
 "вывод кратко": "<да\скорее да\скорее нет\нет\есть сомнения>",
 "вывод текстом": "<обоснуй свой краткий вывод в 2-3 предложениях>",
 "процент схожести": <целое число от 0 до 100, насколько кандидат подходит к вакансии>,
 "положительные части резюме": [<здесь список точных цитат из резюме, которые показывают, почему кандидат соответствует вакансии. Если таких нет, то список пустой>],
 "сомнительные части резюме": [<здесь список точных цитат из резюме, которые вызывают сомнения, действительно ли кандидат соответствует вакансии. Если таких нет, то список пустой>],
 "негативные части резюме": [<здесь список точных цитат из резюме, которые показывают, что кандидат НЕ соответствует вакансии. Если таких нет, то список пустой>]
}
'''





def main():
    vacancies_html_paths = ['~/Documents/проекты/TA/МТС/примеры резюме/Резюме Java-разработчик (Apache Kafka, Spring Boot, PostgreSQL), Москва, 200 000 руб. в месяц - найти Программиста-разработчика Java на SuperJob, опубликовано 03.07.2025 13_51.html']
    resumes_html_paths = [
        '~/Documents/проекты/TA/МТС/примеры вакансий сайт мтс/Разработчик Java (Middle) — вакансии в МТС Финтех — Москва.html',
        '~/Documents/проекты/TA/МТС/примеры резюме/Резюме Frontend‑разработчик (React _ JavaScript), Москва, по договоренности - найти Frontend-разработчика (Javascript) на SuperJob, опубликовано 14.06.2025 12_19_39.html',
        '~/Documents/проекты/TA/МТС/примеры резюме/Резюме Кладовщик-комплектовщик, Москва, 100 000 руб. в месяц - найти Кладовщика комплектовщика на SuperJob, опубликовано 03.02.2024 17_19_53.html'
    ]

    ModelRunner()

    verdicts = []
    for (vacancy_html_path, resume_html_path) in product(vacancies_html_paths, resumes_html_paths):
        verdict = compare_vacancy_and_resume_by_html(
            vacancy_html_path=vacancy_html_path,
            resume_html_path=resume_html_path,
        )

    df = pd.DataFrame([java_mts_vac_and_java_resume, java_mts_vac_and_front_resume, java_mts_vac_and_kladov_resume])
    df.to_csv('vacs_comparison.csv', index=False)


def compare_vacancy_and_resume_by_html(vacancy_html_path: str, resume_html_path: str) -> dict[str, Any]:
    print('start comparison')
    verdict = compare_job_and_resume_by_text(
        job_text=read_html_text(html_path=vacancy_html_path),
        resume_text=read_html_text(html_path=resume_html_path),
    )
    verdict['vacancy_html_path'] = vacancy_html_path
    verdict['resume_html_path'] = resume_html_path

    return verdict


def compare_job_and_resume_by_text(
    model: ModelRunner, job_text: str, resume_text: str, query_len_threshold: int = 65_000,
) -> dict[str, Any]:
    query = f'Текст вакансии:\n{job_text}\n\nТекст резюме:\n{resume_text}'[:query_len_threshold]

    model_response = model.run_text(
        model_uri='yandexgpt-lite',
        text=query,
        system_prompt=FULL_COMPARING_SYSTEM_PROMPT,
        reasoning_mode=ReasoningMode.ENABLED_HIDDEN,
    )
    verdict = {'raw_verdict_info': model_response.text}
    try:
        prepared_verdict_text = model_response.text.replace('`', '').strip()
        data = json.loads(prepared_verdict_text)

        mapper = {
            'размышления о кандидате': 'reasoning',
            'вывод кратко': 'short_conclusion',
            'вывод текстом': 'full_conclusion',
            'процент схожести': 'match_score',
            'положительные части резюме': 'pos_parts',
            'сомнительные части резюме': 'doubt_parts',
            'негативные части резюме': 'neg_parts',
        }
        for old_key, new_key in mapper.items():
            data[new_key] = data[old_key]
            del data[old_key]

        verdict.update(data)
    except:
        print('error while got json parsing')

    return verdict


if __name__ == '__main__':
    main()
