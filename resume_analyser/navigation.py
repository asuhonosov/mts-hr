import streamlit as st

from resume_analyser.storage.interface import IStorage


def go_forward(stage_name: str):
    st.session_state.stage = stage_name
    st.session_state.stages_stack.append(stage_name)
    st.rerun()


def show_go_back(button_name: str = 'Назад'):
    if st.button(button_name):
        if len(st.session_state.stages_stack) == 1:
            new_stage = 'jobs_list'
            st.session_state.stages_stack = [new_stage]
        else:
            st.session_state.stages_stack.pop()
            new_stage = st.session_state.stages_stack[-1]

        st.session_state.stage = new_stage
        st.rerun()


def show_sidebar_navigation(storage: IStorage):
    """Основная функция приложения"""
    # Боковое навигационное меню
    with st.sidebar:
        st.title("Навигация")

        # Секция "Вакансии"
        st.subheader("Вакансии")
        if st.sidebar.button("📋 Список вакансий", use_container_width=True):
            st.session_state.current_job_id = None
            go_forward(stage_name='jobs_list')

        if st.sidebar.button("➕ Добавить вакансию", use_container_width=True):
            st.session_state.current_job_id = None
            go_forward(stage_name='add_job')

        # Секция "Резюме"
        st.subheader("Резюме")
        if st.sidebar.button("👤 Список резюме", use_container_width=True):
            st.session_state.current_job_id = None
            go_forward(stage_name='resumes_list')

        if st.sidebar.button("➕ Добавить резюме", use_container_width=True):
            st.session_state.current_job_id = None
            go_forward(stage_name='add_resume')

        # Секция "Анализ"
        # st.subheader("Анализ")
        # if st.sidebar.button("🔍 Сравнить по ссылкам", use_container_width=True):
        #     st.session_state.current_job_id = None
        #     go_forward(stage_name='input')

        # Отображение текущей вакансии, если она выбрана
        # if st.session_state.current_job_id:
            # current_job = storage.get_job_by_id(st.session_state.current_job_id)
            # if current_job:
                # st.markdown("---")
                # st.subheader("Текущая вакансия")
                # st.markdown(f"**{current_job['title']}**")
                # st.markdown(f"*{current_job.get('company', 'Компания не указана')}*")

                # if st.sidebar.button("📊 Подходящие резюме", use_container_width=True):
                #     st.session_state.stage = 'matching_resumes'
                #     st.rerun()

        # Отображение информации о приложении
        st.markdown("---")
        st.caption("HR Assistant")
        st.caption("© 2025 HR Tech")