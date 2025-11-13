import streamlit as st

from resume_analyser.constants import APP_IDENTIFIER
from resume_analyser.deps import get_storage
from resume_analyser.navigation import show_sidebar_navigation, show_go_back
from resume_analyser.screens.add_job import view_add_job
from resume_analyser.screens.add_resume import view_add_resume
from resume_analyser.screens.links_input import view_links_input_screen
from resume_analyser.screens.jobs_list import view_jobs_list
from resume_analyser.screens.matching_jobs import view_matching_jobs
from resume_analyser.screens.matching_resumes import view_matching_resumes
from resume_analyser.screens.result import view_result_screen
from resume_analyser.screens.resumes_list import view_resumes_list
from resume_analyser.styles_old import apply_custom_css, add_logo_section
from resume_analyser.utils.logs import setup_logging
from resume_analyser.utils.tracing import traced_operation
from resume_analyser.warmup import warmup_state


st.set_page_config(
    page_title="HR Assistant - MVP",
    page_icon="👩‍💼",
    layout="wide"
)

stage_to_screen_action = {
    'input': view_links_input_screen,
    'result': view_result_screen,
    'jobs_list': view_jobs_list,
    'resumes_list': view_resumes_list,
    'matching_resumes': view_matching_resumes,
    'matching_jobs': view_matching_jobs,
    'add_job': view_add_job,
    'add_resume': view_add_resume,
}

# apply_custom_styling()
setup_logging(app_identifier=APP_IDENTIFIER)
apply_custom_css()
warmup_state()



def main():
    add_logo_section(company_logo_url='https://ycpg.ru/yb2btlogo', product_logo_url='https://ycpg.ru/mtslogo')

    storage = get_storage()
    screen_name = st.session_state.stage
    screen_action = stage_to_screen_action[screen_name]

    show_go_back()
    show_sidebar_navigation(storage=storage)

    with traced_operation(
        op_name=f'show_screen-{screen_name}',
        extra={'screen': screen_name, 'session_state': st.session_state},
    ):
        screen_action(storage=storage)


if __name__ == "__main__":
    main()
