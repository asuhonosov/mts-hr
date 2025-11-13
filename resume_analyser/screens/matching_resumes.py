from pprint import pprint

import streamlit as st

from resume_analyser.navigation import go_forward
from resume_analyser.storage.interface import IStorage


def view_matching_resumes(storage: IStorage, min_match_score: int = 40):
    # Находим выбранную вакансию
    current_job = next((job for job in storage.get_all_jobs() if job['id'] == st.session_state.current_job_id), None)

    if not current_job:
        st.error("Вакансия не найдена")
        go_forward(stage_name='jobs_list')
        return

    # Кнопка возврата к списку вакансий
    col1,  = st.columns([6])
    with col1:
        st.header(f"Вакансия: {current_job['title']}")
        st.subheader(f"Компания: {current_job['company']}")

    # Описание вакансии
    st.markdown("### Описание вакансии")
    st.write(current_job['full_description'])
    st.markdown("---")

    # Список подходящих резюме
    st.markdown("### Подходящие кандидаты")

    matching_resumes = storage.get_matching_resumes(job_id=current_job['id'])
    matching_resumes = [match for match in matching_resumes if 'match_score' in match]
    matching_resumes = sorted(matching_resumes, key=lambda x: x['match_score'], reverse=True)

    if st.checkbox('Только подходящие', value=True):
        matching_resumes = [match for match in matching_resumes if match['match_score'] >= min_match_score]

    # Отображение резюме в виде карточек
    for match in matching_resumes:
            resume = storage.get_resume_by_id(resume_id=match['resume_id'])
            try:
                resume['name']
            except:
                pprint(resume)
                pprint(match)

            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                if st.button(f"👤 {resume['name']} - {resume['experience']}", key=f"resume_{resume['id']}"):
                    # Подготавливаем данные для экрана сравнения
                    st.session_state.current_job = current_job
                    st.session_state.current_resume = resume

                    # st.session_state.current_resume_id = resume['id']
                    # st.session_state.resume_text = resume['full_description']
                    # st.session_state.job_text = current_job['full_description']

                    st.session_state.match = match
                    go_forward(stage_name='result')

            with col2:
                st.write(f"Опыт: {resume['experience']}")

            with col3:
                # Отображаем процент соответствия с цветовой индикацией
                match_percentage = int(match['match_score'])

                # Выбираем цвет в зависимости от процента соответствия
                if match_percentage >= 80:
                    color = "green"
                elif match_percentage >= 60:
                    color = "orange"
                else:
                    color = "red"

                st.markdown(f"<p style='color:{color};font-weight:bold;'>{match_percentage}% совпадение</p>",
                            unsafe_allow_html=True)

            st.markdown("---")

    # Кнопка для добавления нового резюме (в MVP просто заглушка)
    if st.button("➕ Добавить резюме для сравнения"):
        go_forward(stage_name='add_resume')
