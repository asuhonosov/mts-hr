import datetime

import streamlit as st

from resume_analyser.analyzer_utils import MatchingEngine
from resume_analyser.describer import describe_job
from resume_analyser.navigation import go_forward
from resume_analyser.storage.interface import IStorage
from resume_analyser.utils.tracing import traced_operation
from resume_analyser.utils.common import clean_url
from tools.run_gpt import ModelRunner


def view_add_job(storage: IStorage):
    """Экран добавления новой вакансии"""
    st.header("Добавление новой вакансии")

    # Форма для добавления вакансии
    with st.form(key="add_job_form"):
        new_job_url = st.text_input("Ссылка на вакансию")
        new_job_url = clean_url(new_job_url)

        # todo.md: разобраться
        # manual_input = st.checkbox("Ввести данные вручную")
        #
        # # Поля для ручного ввода, отображаются только если включен ручной ввод
        # if manual_input:
        #     title = st.text_input("Название вакансии")
        #     company = st.text_input("Компания")
        #     description = st.text_area("Описание вакансии", height=300)

        submitted = st.form_submit_button("Добавить вакансию")

        if submitted:
            try:
                handled_status = add_job_by_url(new_job_url=new_job_url, storage=storage, model=st.session_state.model)
                if handled_status is not None:
                    st.error(handled_status)
                else:
                    st.success("Вакансия успешно добавлена!")
                    go_forward(stage_name='jobs_list')
            except Exception:
                st.error('Что-то пошло не так. Попробуйте позже')

def add_job_by_url(new_job_url: str, storage: IStorage, model: ModelRunner) -> str | None:
    if not new_job_url:
        return 'Введите ссылку на вакансию'

    all_jobs = storage.get_all_jobs()
    if any(job['url'] == new_job_url for job in all_jobs):
        return 'Данная вакансия уже добавлена'

    # Обработка добавления по ссылке
    with st.spinner("Изучаем вакансию..."):
        try:
            with traced_operation(op_name='describe_job_with_gpt', extra={'job_url': new_job_url}):
                job_data = describe_job(job_url=new_job_url, model=model)
                job_data["date_posted"]: datetime.date.today()
        except Exception:
            return 'Не удалось получить данные с указанной страницы'

        with traced_operation(op_name='save_job', extra={'job_data': job_data}):
            job_id = storage.add_job(job_data)

    with st.spinner("Ищем подходящие резюме для вакансии..."):
        try:
            with traced_operation(op_name='rerank_resumes_for_job', extra={'job_id': job_id}):
                matches = MatchingEngine.rerank_resumes_for_job(
                    model=model,
                    job_id=job_id,
                    job_text=job_data['full_description'],
                    resumes=storage.get_all_resumes(),
                )
            with traced_operation(op_name='update_matches', extra={'matches': matches}):
                storage.update_matches(new_matches=matches)
        except Exception:
            storage.delete_job(job_id=job_id)
            return 'Возникла проблема при поиске подходящих резюме. Попробуйте добавить вакансию позже'

    return None
