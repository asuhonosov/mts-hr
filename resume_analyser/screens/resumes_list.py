from typing import Any

import streamlit as st

from resume_analyser.navigation import go_forward
from resume_analyser.storage.interface import IStorage
from resume_analyser.utils.tracing import traced_operation


def view_resumes_list(storage: IStorage):
    st.header("Доступные резюме")

    searched_resumes = _search_resumes(storage=storage)

    if not searched_resumes:
        st.info("Резюме не найдены. Попробуйте изменить поисковый запрос.")
        return

    _view_resumes(filtered_resumes=searched_resumes, storage=storage)

    if st.button("➕ Добавить резюме"):
        go_forward(stage_name='add_resume')


def _search_resumes(storage: IStorage) -> list[dict[str, Any]]:
    search_query = st.text_input("🔍 Поиск резюме", "")

    searched_resumes = storage.get_all_resumes()
    if search_query:
        searched_resumes = [
            resume
            for resume in searched_resumes
            if search_query.lower() in resume['name'].lower() or search_query.lower() in resume['position'].lower()
        ]

    return searched_resumes

def _view_resumes(filtered_resumes: list[dict[str, Any]], storage: IStorage):
    for resume in filtered_resumes:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            if st.button(f"📋 {resume['name']}", key=f"resume_{resume['id']}"):
                st.session_state.current_resume_id = resume['id']
                go_forward(stage_name='matching_jobs')

        with col2:
            st.write(resume['city'])

        with col3:
            st.write(resume['experience'])

        with col4:
            if st.button('🗑️', key=f"del_resume_{resume['id']}"):
                with traced_operation(op_name='delete_resume', extra={'resume_id': resume['id']}):
                    storage.delete_resume(resume_id=resume['id'])
                st.rerun()

        st.markdown("---")
