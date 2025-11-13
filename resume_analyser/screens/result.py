import streamlit as st

from resume_analyser.storage.interface import IStorage
from resume_analyser.utils.common import highlight_text


def view_result_screen(storage: IStorage):
    match = st.session_state.match
    resume = st.session_state.current_resume
    job = st.session_state.current_job

    pipeline = [
        view_result_screen_top,
        view_resume_cites,
        view_highlighted_resume_text,
        view_job_text
    ]

    for view_block in pipeline:
        view_block(match, resume, job)


def view_result_screen_top(match, resume, job):
    # Кнопки навигации
    # col1, col2, col3 = st.columns([1, 2, 1])
    # with col1:
    #     if st.button("← Назад к вводу"):
    #         st.session_state.stage = 'input'
    #         st.rerun()
    #
    # with col3:
    #     view_options = {"simple": "Простой вид", "advanced": "Расширенный вид"}
    #     current_view = st.selectbox(
    #         "Режим просмотра:",
    #         options=list(view_options.keys()),
    #         format_func=lambda x: view_options[x],
    #         index=0 if st.session_state.view_mode == "simple" else 1
    #     )
    #     st.session_state.view_mode = current_view

    # Отображение результатов
    st.subheader(f"**Вакансия**: {job['title']}")
    st.subheader(f"**Кандидат**: {resume['name']}")

    # Выбор цвета для вывода - более приятные и менее яркие оттенки
    conclusion_color = {
        "да": "#c8e6c9",  # светлый зеленый
        "скорее да": "#dcedc8",  # очень светлый зеленый
        "есть сомнения": "#fff9c4",  # светло-желтый
        "скорее нет": "#ffccbc",  # светло-оранжевый
        "нет": "#ffcdd2"  # светло-красный
    }.get(match['short_conclusion'], "#e3f2fd")  # светло-голубой по умолчанию

    # Соответствующие цвета текста для контраста
    text_color = {
        "да": "#1b5e20",  # темно-зеленый
        "скорее да": "#33691e",  # темно-зеленый
        "есть сомнения": "#f57f17",  # темно-желтый
        "скорее нет": "#bf360c",  # темно-оранжевый
        "нет": "#b71c1c"  # темно-красный
    }.get(match['short_conclusion'], "#0d47a1")  # темно-синий по умолчанию

    # Блок с выводом
    st.markdown(f"""
                    <div style="padding: 1rem; border-radius: 0.5rem; background-color: {conclusion_color}; margin-bottom: 1rem; border: 1px solid rgba(0,0,0,0.1);">
                        <h2 style="margin-top: 0; color: {text_color};">{match['short_conclusion'].upper()}</h2>
                        <p style="margin-bottom: 0; color: #333;">Схожесть: {match['match_score']}%</p>
                        <p style="margin-bottom: 0; color: #333;">{match['full_conclusion']}</p>
                    </div>
                    """, unsafe_allow_html=True)


def view_highlighted_resume_text(match, resume, job):
    highlighted_resume = highlight_text(
        text=resume['full_description'],
        positive_parts=match['pos_parts'],
        doubt_parts=match['doubt_parts'],
        negative_parts=match['neg_parts'],
    )

    st.subheader("Резюме с подсветкой")
    st.markdown(
        f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; height: 400px; overflow-y: auto;">
                        {highlighted_resume}
                    </div>
                    <div style="margin-top: 10px; font-size: 0.8em;">
                        <span style="background-color: rgba(0, 255, 0, 0.3); padding: 2px; border-radius: 3px;">Положительные аспекты</span> | 
                        <span style="background-color: rgba(255, 255, 0, 0.3); padding: 2px; border-radius: 3px;">Сомнительные аспекты</span>| 
                        <span style="background-color: rgba(255, 0, 0, 0.3); padding: 2px; border-radius: 3px;">Негативные аспекты</span>
                    </div>
                    """,
        unsafe_allow_html=True
    )


def view_job_text(match, resume, job):
    highlighted_job = highlight_text(
        text=job['full_description'],
        positive_parts=match['pos_parts'],
        doubt_parts=match['doubt_parts'],
        negative_parts=match['neg_parts'],
    )

    st.subheader("Описание вакансии")
    st.markdown(
        f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; height: 400px; overflow-y: auto;">
                        {highlighted_job}
                    </div>
                    <div style="margin-top: 10px; font-size: 0.8em;">
                        <span style="background-color: rgba(0, 255, 0, 0.3); padding: 2px; border-radius: 3px;">Положительные аспекты</span> | 
                        <span style="background-color: rgba(255, 255, 0, 0.3); padding: 2px; border-radius: 3px;">Сомнительные аспекты</span>| 
                        <span style="background-color: rgba(255, 0, 0, 0.3); padding: 2px; border-radius: 3px;">Негативные аспекты</span>
                    </div>
                    """,
        unsafe_allow_html=True
    )

def view_resume_cites(match, resume, job):
    if match['pos_parts'] or match['doubt_parts'] or match['neg_parts']:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("📈 Положительные части резюме")
            for item in match['pos_parts']:
                st.markdown(f"✅ {item}")

        with col2:
            st.subheader("🔍 Сомнительные части резюме")
            for item in match['doubt_parts']:
                st.markdown(f"⚠️ {item}")

        with col3:
            st.subheader("⛔ Негативные части резюме")
            for item in match['neg_parts']:
                st.markdown(f"❌ {item}")


def verbose_analysis(match, resume, job):
    with st.expander("Подробный анализ кандидата"):
        try:
            st.write(match["reasoning"])
        except:
            st.write('НЕТ ПОЛЯ "размышления о кандидате"')
            st.write(match)
