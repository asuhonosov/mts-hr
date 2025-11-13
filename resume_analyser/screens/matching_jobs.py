import streamlit as st

from resume_analyser.navigation import go_forward
from resume_analyser.storage.interface import IStorage


def view_matching_jobs(storage: IStorage, min_match_score: int = 40):
    # Находим выбранную вакансию
    current_resume = next((resume for resume in storage.get_all_resumes() if resume['id'] == st.session_state.current_resume_id), None)

    if not current_resume:
        st.error("Вакансия не найдена")
        go_forward(stage_name='resumes_list')
        return

    # Кнопка возврата к списку вакансий
    col1,  = st.columns([6])
    with col1:
        st.header(f"Имя: {current_resume['name']}")
        st.subheader(f"Опыт: {current_resume['experience']}")

    # Описание Резюме
    st.markdown("### Резюме")
    st.write(current_resume['full_description'])
    st.markdown("---")

    # Список подходящих резюме
    st.markdown("### Подходящие вакансии")

    matching_jobs = storage.get_matching_jobs(resume_id=current_resume['id'])
    matching_jobs = [match for match in matching_jobs if 'match_score' in match]
    matching_jobs = sorted(matching_jobs, key=lambda x: x['match_score'], reverse=True)

    if st.checkbox('Только подходящие', value=True):
        matching_jobs = [match for match in matching_jobs if match['match_score'] >= min_match_score]

    # Отображение резюме в виде карточек
    for match in matching_jobs:
        job = storage.get_job_by_id(job_id=match['job_id'])
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            if st.button(f"👤 {job['title']} - {job['company']}", key=f"job_{job['id']}"):
                # Подготавливаем данные для экрана сравнения
                st.session_state.current_job = job
                st.session_state.current_resume = current_resume

                # st.session_state.current_resume_id = resume['id']
                # st.session_state.resume_text = resume['full_description']
                # st.session_state.job_text = current_job['full_description']

                st.session_state.match = match
                go_forward(stage_name='result')

        with col2:
            st.write(f"Компания: {job['company']}")

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
    if st.button("➕ Добавить вакансию для сравнения"):
        go_forward(stage_name='add_job')
