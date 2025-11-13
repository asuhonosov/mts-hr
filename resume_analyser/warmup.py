import datetime

import streamlit as st

from resume_analyser.comparator import compare_job_and_resume_by_text
from resume_analyser.screens.add_job import add_job_by_url
from resume_analyser.screens.add_resume import add_resume_by_url
from resume_analyser.storage.file_storage import FileStorage
from resume_analyser.utils.common import clean_url
from tools.run_gpt import ModelRunner


def warmup_storage():
    model = ModelRunner()
    storage = FileStorage()

    jobs_urls = [
        'https://job.mtsbank.ru/vacancies/moskva/razrabotchik-java-senior--1010747',
        'https://job.mtsbank.ru/vacancies/moskva/starshiy-razrabotchik-android--1010609',
        'https://job.mtsbank.ru/vacancies/moskva/rukovoditel-tsentra-razvitiya-partnerskoy-seti--1010607',
        'https://yandex.ru/jobs/vacancies/produktoviy-analitik-v-neyroekspert-33189',
        'https://www.superjob.ru/vakansii/proizvoditel-rabot-50773241.html?vacancyshouldhighlight=true',
        'https://hh.ru/vacancy/122435598?utm_medium=cpc_hh&utm_source=clickmehhru&utm_campaign=962352&utm_local_campaign=1407055&utm_content=1006905',
    ]
    resumes_urls = [
        'https://hh.ru/resume/08c4c14800021d447b0039ed1f785254706d4d',
        'https://www.superjob.ru/resume/junior-razrabotchik-54298502.html?fromSearch=true',
        'https://www.superjob.ru/resume/rukovoditel-otdela-prodazh-46870692.html?fromSearch=true',
        'https://www.superjob.ru/resume/programmist-43784999.html?fromSearch=true',
        'https://www.superjob.ru/resume/veduschij-testirovschik-po-55594874.html?fromSearch=true',
        'https://www.superjob.ru/resume/java-razrabotchik-55757065.html?fromSearch=true',
        'https://www.superjob.ru/resume/frontend-razrabotchik-55708483.html?fromSearch=true',
        'https://www.superjob.ru/resume/prorab-55535973.html',
        'https://www.superjob.ru/resume/android-razrabotchik-55564268.html',
    ]

    for job_url in jobs_urls:
        job_url = clean_url(url=job_url)
        add_job_by_url(new_job_url=job_url, storage=storage, model=model)

    for resume_url in resumes_urls:
        resume_url = clean_url(url=resume_url)
        add_resume_by_url(new_resume_url=resume_url, storage=storage, model=model)


def rerank_for_some_jobs():
    items = [
        {
            'job_url': 'https://job.mtsbank.ru/vacancies/moskva/razrabotchik-java-senior--1010747',
            'resume_url': 'https://www.superjob.ru/resume/java-razrabotchik-55757065.html?fromSearch=true',
        },
        {
            'job_url': 'https://job.mtsbank.ru/vacancies/moskva/rukovoditel-tsentra-razvitiya-partnerskoy-seti--1010607',
            'resume_url': 'https://www.superjob.ru/resume/rukovoditel-otdela-prodazh-46870692.html?fromSearch=true',
        },
    ]

    model = ModelRunner()
    storage = FileStorage()

    new_matches = []
    for item in items:
        job_url = clean_url(item['job_url'])
        resume_url = clean_url(item['resume_url'])

        for job in storage.get_all_jobs():
            if job['url'] != job_url:
                continue
            print(job['title'])

            for resume in storage.get_all_resumes():
                if resume['url'] != resume_url:
                    continue

                print('  > ', resume['name'])

                # Рассчитываем оценку соответствия
                comparison = compare_job_and_resume_by_text(model=model, job_text=job['full_description'], resume_text=resume['full_description'])
                new_matches.append({
                    'resume_id': resume['id'],
                    'job_id': job['id'],
                    **comparison,
                })
            #
            # matches = MatchingEngine.rerank_resumes_for_job(
            #     model=model,
            #     job_id=job['id'],
            #     job_text=job['full_description'],
            #     resumes=storage.get_all_resumes(),
            # )
            storage.update_matches(new_matches=new_matches)


# @lru_cache(maxsize=1)
def warmup_state():
    # Состояние приложения
    if 'stage' not in st.session_state:
        st.session_state.stage = 'jobs_list'
    if 'stages_stack' not in st.session_state:
        st.session_state.stages_stack = ['jobs_list']
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""
    if 'job_text' not in st.session_state:
        st.session_state.job_text = ""
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = "simple"
    if 'model' not in st.session_state:
        st.session_state.model = ModelRunner()

    if 'current_job_id' not in st.session_state:
        st.session_state.current_job_id = None

    if 'current_resume_id' not in st.session_state:
        st.session_state.current_resume_id = None

    if 'jobs' not in st.session_state:
        # Пример списка вакансий для MVP
        st.session_state.jobs = [
            {
                "id": 1,
                "title": "Python разработчик",
                "company": "TechInnovate",
                "date_posted": datetime.date(2023, 10, 15),
                "url": "https://example.com/job1",
                "description": "Требуется Python разработчик с опытом работы от 3 лет. Знание Django, Flask, SQL. Опыт работы с Docker, CI/CD."
            },
            {
                "id": 2,
                "title": "Frontend Developer (React)",
                "company": "WebSolutions",
                "date_posted": datetime.date(2023, 10, 10),
                "url": "https://example.com/job2",
                "description": "Ищем опытного Frontend разработчика со знанием React, Redux, TypeScript. Опыт коммерческой разработки от 2 лет."
            },
            {
                "id": 3,
                "title": "Data Scientist",
                "company": "AnalyticsPro",
                "date_posted": datetime.date(2023, 10, 5),
                "url": "https://example.com/job3",
                "description": "В команду требуется Data Scientist. Опыт работы с Python, pandas, scikit-learn, TensorFlow. Знание SQL обязательно."
            },
            {
                "id": 4,
                "title": "DevOps инженер",
                "company": "CloudTech",
                "date_posted": datetime.date(2023, 10, 2),
                "url": "https://example.com/job4",
                "description": "Ищем DevOps инженера с опытом работы с Kubernetes, Docker, Terraform, AWS/GCP. Опыт автоматизации CI/CD."
            },
            {
                "id": 5,
                "title": "Product Manager",
                "company": "ProductLabs",
                "date_posted": datetime.date(2023, 9, 28),
                "url": "https://example.com/job5",
                "description": "Требуется Product Manager с опытом вывода цифровых продуктов на рынок. Понимание UX/UI, аналитика, работа с командой разработки."
            }
        ]

    if 'resumes' not in st.session_state:
        # Пример списка резюме для MVP
        st.session_state.resumes = [
            {
                "id": 101,
                "name": "Иванов Иван Иванович",
                "position": "Python Developer",
                "experience": "5 лет",
                "url": "https://example.com/resume101",
                "match_score": 0.92,
                "text": "Опытный Python разработчик с 5-летним стажем. Работал в проектах с использованием Django, Flask. Имею опыт с SQL и NoSQL базами данных. Участвовал в Agile-командах."
            },
            {
                "id": 102,
                "name": "Петрова Анна Сергеевна",
                "position": "Full Stack Developer",
                "experience": "4 года",
                "url": "https://example.com/resume102",
                "match_score": 0.85,
                "text": "Full Stack разработчик с опытом работы 4 года. Навыки: Python, Django, JavaScript, React. Опыт работы с PostgreSQL, MongoDB. Участвовала в разработке высоконагруженных систем."
            },
            {
                "id": 103,
                "name": "Сидоров Алексей Петрович",
                "position": "Python Backend Engineer",
                "experience": "3 года",
                "url": "https://example.com/resume103",
                "match_score": 0.78,
                "text": "Backend разработчик на Python. Опыт: 3 года. Проекты с использованием Django, DRF, Flask. Знание SQL, опыт с Docker. Участие в CI/CD настройке."
            },
            {
                "id": 104,
                "name": "Козлова Екатерина Александровна",
                "position": "Python Data Engineer",
                "experience": "2 года",
                "url": "https://example.com/resume104",
                "match_score": 0.65,
                "text": "Data Engineer с опытом работы 2 года. Работа с большими данными, ETL-процессы. Навыки: Python, Pandas, SQL, Spark. Опыт работы с облачными платформами."
            },
            {
                "id": 105,
                "name": "Морозов Дмитрий Владимирович",
                "position": "Junior Python Developer",
                "experience": "1 год",
                "url": "https://example.com/resume105",
                "match_score": 0.58,
                "text": "Junior Python Developer с опытом работы 1 год. Знание основ Python, Django. Начальный опыт работы с базами данных. Активно изучаю новые технологии."
            }
        ]



if __name__ == '__main__':
    warmup_storage()