import logging
import time
import uuid
from contextlib import contextmanager

import streamlit as st

from resume_analyser.constants import APP_IDENTIFIER


@contextmanager
def traced_operation(op_name, extra=None):
    """Контекстный менеджер для трейсинга операций"""
    # Убеждаемся, что у нас есть user_trace_id
    if 'user_trace_id' not in st.session_state:
        st.session_state.user_trace_id = f'user-{uuid.uuid4()}'
    if 'op_name_to_op_trace_id' not in st.session_state:
        st.session_state.op_name_to_op_trace_id = {}
    if op_name not in st.session_state.op_name_to_op_trace_id:
        st.session_state.op_name_to_op_trace_id[op_name] = f'op-{uuid.uuid4()}'

    logger = logging.getLogger(APP_IDENTIFIER)

    # Подготавливаем дополнительные данные
    extra_data = {
        "user_trace_id": st.session_state.user_trace_id,
        "op_trace_id": st.session_state.op_name_to_op_trace_id[op_name],
        "op_name": op_name,
        "op_name_to_op_trace_id": st.session_state.op_name_to_op_trace_id,
    }
    if extra:
        extra_data.update(extra)

    start_time = time.time()
    logger.info(f"Начало операции: \"{op_name}\"", extra=extra_data)

    try:
        # Выполняем операцию
        yield

        # Логируем успешное завершение
        duration = time.time() - start_time
        logger.info(
            f"Операция \"{op_name}\" успешно завершена за {duration:.2f}с",
            extra={**extra_data, "duration": duration}
        )
    except Exception as e:
        # Логируем ошибку
        duration = time.time() - start_time
        logger.error(
            f"Ошибка в операции \"{op_name}\": {str(e)}",
            extra={**extra_data, "duration": duration, "error_type": type(e).__name__, "error": str(e)}
        )
        raise
    finally:
        st.session_state.op_name_to_op_trace_id.pop(op_name)
