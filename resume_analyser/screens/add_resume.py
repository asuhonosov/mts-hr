import streamlit as st
import datetime

from resume_analyser.analyzer_utils import MatchingEngine
from resume_analyser.describer import describe_resume
from resume_analyser.navigation import go_forward
from resume_analyser.storage.interface import IStorage
from resume_analyser.utils.tracing import traced_operation
from resume_analyser.utils.common import clean_url
from tools.run_gpt import ModelRunner


def view_add_resume(storage: IStorage):
    """Экран добавления нового резюме"""
    st.header("Добавление нового резюме")

    # Форма для добавления резюме
    with st.form(key="add_resume_form"):
        new_resume_url = st.text_input("Ссылка на резюме")
        new_resume_url = clean_url(new_resume_url)

        # todo.md: разобраться
        # manual_input = st.checkbox("Ввести данные вручную")
        #
        # # Поля для ручного ввода, отображаются только если включен ручной ввод
        # if manual_input:
        #     name = st.text_input("ФИО кандидата")
        #     position = st.text_input("Должность")
        #     experience = st.text_input("Опыт работы")
        #     resume_text = st.text_area("Текст резюме", height=300)

        submitted = st.form_submit_button("Добавить резюме")

        if submitted:
            try:
                handled_status = add_resume_by_url(new_resume_url=new_resume_url, storage=storage, model=st.session_state.model)
                if handled_status is not None:
                    st.error(handled_status)
                else:
                    st.success("Резюме успешно добавлено!")
                    go_forward(stage_name='resumes_list')
            except Exception as e:
                st.error('Что-то пошло не так. Попробуйте позже')


def add_resume_by_url(new_resume_url: str, storage: IStorage, model: ModelRunner) -> str | None:
    if not new_resume_url:
        return 'Введите ссылку на резюме или выберите ручной ввод'

    all_resumes = storage.get_all_resumes()
    if any(job['url'] == new_resume_url for job in all_resumes):
        return 'Данное резюме уже добавлено'

    # Обработка добавления по ссылке
    with st.spinner("Изучаем резюме..."):
        try:
            with traced_operation(op_name='describe_resume_with_gpt', extra={'resume_url': new_resume_url}):
                resume_data = describe_resume(resume_url=new_resume_url, model=model)
                resume_data["date_posted"]: datetime.date.today()
        except Exception:
            return 'Не удалось получить данные с указанной страницы'

        # Сохраняем резюме
        with traced_operation(op_name='save_resume', extra={'resume_data': resume_data}):
            resume_id = storage.add_resume(resume_data)

    # Запускаем переранжирование для всех вакансий
    with st.spinner("Ищем подходящие вакансии для резюме..."):
        try:
            with traced_operation(op_name='rerank_jobs_for_resume', extra={'resume_id': resume_id}):
                matches = MatchingEngine.rerank_jobs_for_resume(
                    model=model,
                    resume_id=resume_id,
                    resume_text=resume_data['full_description'],
                    jobs=storage.get_all_jobs(),
                )
            with traced_operation(op_name='update_matches', extra={'matches': matches}):
                storage.update_matches(new_matches=matches)
        except Exception:
            storage.delete_resume(resume_id=resume_id)
            return 'Возникла проблема при поиске подходящих вакансий. Попробуйте добавить резюме позже'

    return None
