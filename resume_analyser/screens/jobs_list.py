import streamlit as st

from resume_analyser.navigation import go_forward
from resume_analyser.storage.interface import IStorage
from resume_analyser.utils.tracing import traced_operation


def view_jobs_list(storage: IStorage):
    st.header("Доступные вакансии")

    # Поиск по вакансиям
    search_query = st.text_input("🔍 Поиск вакансий", "")

    # Фильтруем вакансии по поисковому запросу
    filtered_jobs = storage.get_all_jobs()
    if search_query:
        filtered_jobs = [
            job
            for job in filtered_jobs
            if search_query.lower() in job['title'].lower() or search_query.lower() in job['company'].lower()
        ]

    # Если нет вакансий после фильтрации
    if not filtered_jobs:
        st.info("Вакансии не найдены. Попробуйте изменить поисковый запрос.")
        return

    # Отображаем вакансии
    for job in filtered_jobs:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            if st.button(f"📋 {job['title']}", key=f"job_{job['id']}"):
                st.session_state.current_job_id = job['id']
                st.session_state.stage = 'matching_resumes'
                st.rerun()

        with col2:
            st.write(job['company'])

        with col3:
            st.write(job['date_posted'].strftime("%d.%m.%Y"))

        with col4:
            if st.button('🗑️', key=f"del_job_{job['id']}"):
                with traced_operation(op_name='delete_job', extra={'job_id': job['id']}):
                    storage.delete_job(job_id=job['id'])
                st.rerun()

        st.markdown("---")

    # Кнопка для добавления новой вакансии (в MVP просто заглушка)
    if st.button("➕ Добавить вакансию"):
        go_forward(stage_name='add_job')
