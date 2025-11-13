from pathlib import Path
from pprint import pprint
from typing import Any

import requests
import numpy as np
from scipy.spatial.distance import cdist

from resume_analyser.utils import read_html_text
from settings import YCSettings
from tools.run_gpt import ModelRunner

yc_settings = YCSettings()

doc_uri = f"emb://{yc_settings.folder_id}/text-search-doc/latest"
query_uri = f"emb://{yc_settings.folder_id}/text-search-query/latest"
embed_url = "https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"
headers = {
    "Content-Type": "application/json", 
    "Authorization": f"Bearer {yc_settings.token}", 
    "x-folder-id": f"{yc_settings.folder_id}",
}

RESUME_REDUCING_SYSTEM_PROMPT = '''Сократи текст до одного предложения. Выпиши только самые ключевые слова: предметная область специалиста, специализация, уровень мастерства кандидата.'''
VACANCY_REDUCING_SYSTEM_PROMPT = '''Сократи текст до одного предложения. Выпиши только самые ключевые слова: предметная область вакансии, специализация, необходимый уровень мастерства кандидата.'''


def main():
    examples = [
        dict(
            vacancy_html_path='~/Documents/проекты/TA/МТС/примеры резюме/Резюме Java-разработчик (Apache Kafka, Spring Boot, PostgreSQL), Москва, 200 000 руб. в месяц - найти Программиста-разработчика Java на SuperJob, опубликовано 03.07.2025 13_51.html',
            resume_html_path='~/Documents/проекты/TA/МТС/примеры вакансий сайт мтс/Разработчик Java (Middle) — вакансии в МТС Финтех — Москва.html',
        ),
        dict(
            vacancy_html_path='~/Documents/проекты/TA/МТС/примеры резюме/Резюме Java-разработчик (Apache Kafka, Spring Boot, PostgreSQL), Москва, 200 000 руб. в месяц - найти Программиста-разработчика Java на SuperJob, опубликовано 03.07.2025 13_51.html',
            resume_html_path='~/Documents/проекты/TA/МТС/примеры резюме/Резюме Frontend‑разработчик (React _ JavaScript), Москва, по договоренности - найти Frontend-разработчика (Javascript) на SuperJob, опубликовано 14.06.2025 12_19_39.html',
        ),
        dict(
            vacancy_html_path='~/Documents/проекты/TA/МТС/примеры резюме/Резюме Java-разработчик (Apache Kafka, Spring Boot, PostgreSQL), Москва, 200 000 руб. в месяц - найти Программиста-разработчика Java на SuperJob, опубликовано 03.07.2025 13_51.html',
            resume_html_path='~/Documents/проекты/TA/МТС/примеры резюме/Резюме Кладовщик-комплектовщик, Москва, 100 000 руб. в месяц - найти Кладовщика комплектовщика на SuperJob, опубликовано 03.02.2024 17_19_53.html',
        ),
    ]

    model_runner = ModelRunner()
    for example in examples:
        vacancy_text = read_html_text(html_path=example['vacancy_html_path'])
        resume_text = read_html_text(html_path=example['resume_html_path'])

        reduced_vacancy_text = vacancy_text
        # reduced_vacancy_text = model_runner.run_text(
        #     model_uri='yandexgpt', text=vacancy_text, system_prompt=TEXT_REDUCING_SYSTEM_PROMPT
        # ).text

        reduced_resume_text = model_runner.run_text(
            model_uri='yandexgpt-lite', text=resume_text, system_prompt=RESUME_REDUCING_SYSTEM_PROMPT
        ).text

        reduced_vacancy_text = Path(example['vacancy_html_path']).name
        reduced_resume_text = Path(example['resume_html_path']).name

        res = calc_similarity(vacancy_text=reduced_vacancy_text, resume_text=reduced_resume_text)
        res['vacancy_name'] = Path(example['vacancy_html_path']).name
        res['resume_name'] = Path(example['resume_html_path']).name
        res['reduced_resume_text'] = reduced_resume_text
        # res['reduced_vacancy_text'] = reduced_vacancy_text

        pprint(res)


def calc_similarity(vacancy_text: str, resume_text: str) -> dict[str, Any]:
    # Создаем эмбеддинг текстов
    query_embedding = get_embedding(resume_text, text_type="query")
    docs_embedding = [get_embedding(doc_text, text_type="query") for doc_text in [vacancy_text]]

    # Вычисляем косинусное расстояние и сходство
    dist = cdist(query_embedding[None, :], docs_embedding, metric="cosine")
    sim = 1 - dist

    return {
        'dist': dist,
        'sim': sim,
    }


def get_embedding(text: str, text_type: str = "doc") -> np.array:
    query_data = {
        "modelUri": doc_uri if text_type == "doc" else query_uri,
        "text": text,
    }
    response = requests.post(embed_url, json=query_data, headers=headers)
    try:
        return np.array(response.json()["embedding"])
    except:
        print(response)
        raise


if __name__ == '__main__':
    main()
