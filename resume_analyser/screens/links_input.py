import streamlit as st
from resume_analyser.comparator import compare_job_and_resume_by_text
from resume_analyser.storage.interface import IStorage
from resume_analyser.utils.common import get_text_from_url


def view_links_input_screen(storage: IStorage):
    with st.form("url_form"):
        resume_url = st.text_input("Ссылка на резюме кандидата")
        job_url = st.text_input("Ссылка на описание вакансии")

        submitted = st.form_submit_button("Сравнить")

        if submitted:
            on_submit(resume_url=resume_url, job_url=job_url)


def on_submit(resume_url: str, job_url: str):
    if not resume_url or not job_url:
        st.error("Пожалуйста, введите обе ссылки")
        return

    with st.spinner("Загрузка данных и анализ..."):
        resume_text = get_text_from_url(resume_url)
        job_text = get_text_from_url(job_url)

        if resume_text and job_text:
            # Сохраняем тексты для использования в расширенном просмотре
            st.session_state.resume_text = resume_text
            st.session_state.job_text = job_text

            # Анализ резюме и вакансии
            result = compare_job_and_resume_by_text(resume_text=resume_text, job_text=job_text)
            st.session_state.result = result
            st.session_state.stage = 'result'
            st.rerun()
