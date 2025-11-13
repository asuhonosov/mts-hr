import logging
import os
import platform

from systemd import journal

import streamlit as st


def setup_logging(app_identifier='mts_hr_app'):
    logger = logging.getLogger(name=app_identifier)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    logger.addHandler(
        hdlr=_prepare_journald_handler(app_identifier=app_identifier),
    )
    logger.addFilter(
        filter=TraceIDFilter(),
    )

def _prepare_journald_handler(app_identifier: str) -> journal.JournaldLogHandler:
    journald_handler = journal.JournaldLogHandler(identifier=app_identifier)
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - [%(user_trace_id)s] - [%(op_name)s | %(op_trace_id)s] - %(message)s'
    )
    journald_handler.setFormatter(formatter)

    return journald_handler

def _log_system_info(logger: logging.Logger):
    system_info = {
        "hostname": platform.node(),
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "process_id": os.getpid(),
        "op_name": "startup",
        "op_trace_id": "startup",
    }
    logger.info("Приложение запущено", extra={
        "user_trace_id": "startup",
        **system_info,
    })


class TraceIDFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, 'user_trace_id'):
            record.user_trace_id = st.session_state.get('user_trace_id', 'no-trace-id')
        return True
