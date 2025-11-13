import streamlit as st


def apply_custom_styling():
    """Применяет глобальные стили для всего приложения"""

    # CSS для стилизации всего приложения
    app_css = """
    <style>
    /* Глобальные стили */
    .main {
        background-color: #f5f7f9 !important;  /* Светло-серый фон для всей страницы */
        padding: 1rem;
    }

    /* Стиль для контейнеров с содержимым */
    .content-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* Стиль для заголовков */
    h1, h2, h3, h4, h5, h6 {
        color: #333;
        font-weight: 600;
    }

    /* Стилизация кнопок */
    .stButton > button {
        border: 2px solid #ff6b6b !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
        background-color: white !important;
        color: #333 !important;
        font-weight: 500 !important;
    }

    .stButton > button:hover {
        border: 2px solid #ff0000 !important;
        box-shadow: 0 0 5px rgba(255, 0, 0, 0.5);
        transform: translateY(-2px);
    }

    /* Стиль для секции логотипов */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 15px 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    .logo-box {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 150px;
        height: 70px;
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        margin: 0 15px;
    }

    .logo-box:hover {
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }

    .logo-placeholder {
        font-size: 14px;
        color: #adb5bd;
        text-align: center;
        font-family: sans-serif;
    }

    .logo-img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }

    /* Улучшенный стиль для карточек и списков */
    .card {
        background-color: white;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        transition: all 0.2s ease;
    }

    .card:hover {
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
    }

    /* Стили для меток и значений в карточках */
    .card-label {
        font-weight: 600;
        color: #555;
        margin-bottom: 5px;
    }

    .card-value {
        color: #333;
    }

    /* Стили для меток статусов */
    .status-positive {
        background-color: #c8e6c9;
        color: #1b5e20;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 500;
        font-size: 0.9em;
    }

    .status-neutral {
        background-color: #fff9c4;
        color: #f57f17;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 500;
        font-size: 0.9em;
    }

    .status-negative {
        background-color: #ffcdd2;
        color: #b71c1c;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 500;
        font-size: 0.9em;
    }

    /* Улучшенный стиль для разделителей */
    hr {
        border: none;
        height: 1px;
        background-color: #e0e0e0;
        margin: 20px 0;
    }

    /* Стиль для боковой панели */
    .css-1d391kg, .css-1lcbmhc {
        background-color: white !important;
        border-right: 1px solid #e0e0e0;
    }

    /* Стиль для виджетов ввода */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
    }

    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border: 1px solid #ff6b6b !important;
        box-shadow: 0 0 0 1px #ff6b6b !important;
    }

    /* Улучшенный стиль для сообщений */
    .success-message, .stSuccess {
        background-color: #e8f5e9 !important;
        border-left-color: #4caf50 !important;
        border-radius: 8px !important;
    }

    .info-message, .stInfo {
        background-color: #e3f2fd !important;
        border-left-color: #2196f3 !important;
        border-radius: 8px !important;
    }

    .warning-message, .stWarning {
        background-color: #fff8e1 !important;
        border-left-color: #ff9800 !important;
        border-radius: 8px !important;
    }

    .error-message, .stError {
        background-color: #ffebee !important;
        border-left-color: #f44336 !important;
        border-radius: 8px !important;
    }
    </style>
    """

    # Применяем CSS
    st.markdown(app_css, unsafe_allow_html=True)


def add_logo_section(company_logo_url=None, product_logo_url=None):
    """
    Добавляет секцию для логотипов в верхней части приложения,
    выравнивая их по центру без текста между ними

    Args:
        company_logo_url (str): URL изображения логотипа компании
        product_logo_url (str): URL изображения логотипа продукта
    """

    # Формируем HTML в зависимости от наличия логотипов
    company_logo_html = f'<img src="{company_logo_url}" alt="Company Logo" class="logo-img">' if company_logo_url else '<div class="logo-placeholder">Логотип компании</div>'
    product_logo_html = f'<img src="{product_logo_url}" alt="Product Logo" class="logo-img">' if product_logo_url else '<div class="logo-placeholder">Логотип продукта</div>'

    logo_html = f"""
    <div class="logo-container">
        <div class="logo-box">
            {company_logo_html}
        </div>
        <div class="logo-box">
            {product_logo_html}
        </div>
    </div>
    """

    # Применяем HTML
    st.markdown(logo_html, unsafe_allow_html=True)


def content_container(content_function, *args, **kwargs):
    """
    Оборачивает содержимое в красивый белый контейнер

    Args:
        content_function: Функция, которая генерирует содержимое
        *args, **kwargs: Аргументы для функции
    """
    html_start = '<div class="content-container">'
    html_end = '</div>'

    st.markdown(html_start, unsafe_allow_html=True)
    result = content_function(*args, **kwargs)
    st.markdown(html_end, unsafe_allow_html=True)

    return result


def styled_card(title, content, status=None):
    """
    Создает стилизованную карточку с заголовком и содержимым

    Args:
        title (str): Заголовок карточки
        content (str): Содержимое карточки
        status (str, optional): Статус (positive, neutral, negative)
    """
    status_html = ""
    if status:
        status_class = {
            "positive": "status-positive",
            "neutral": "status-neutral",
            "negative": "status-negative"
        }.get(status, "status-neutral")

        status_text = {
            "positive": "✓ Подходит",
            "neutral": "⚠ Есть сомнения",
            "negative": "✗ Не подходит"
        }.get(status, status)

        status_html = f'<span class="{status_class}">{status_text}</span>'

    html = f"""
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div style="font-weight: 600; font-size: 1.1em; color: #333;">{title}</div>
            {status_html}
        </div>
        <div>{content}</div>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)


# Пример использования
def main():
    # Применяем общие стили
    apply_custom_styling()

    # Добавляем логотипы
    add_logo_section(
        company_logo_url="https://placehold.co/150x70/f8f9fa/0066ff?text=Company&font=montserrat",
        product_logo_url="https://placehold.co/150x70/f8f9fa/ff6600?text=HR+Assistant&font=montserrat"
    )

    # Заголовок приложения
    st.title("HR Assistant - Анализ соответствия кандидатов")

    # Пример использования контейнера для содержимого
    def show_jobs_list():
        st.header("Доступные вакансии")
        st.write("Здесь будет список вакансий...")

        # Пример карточек
        styled_card(
            "Python разработчик",
            "TechInnovate • Опубликовано: 15.10.2023",
            "positive"
        )

        styled_card(
            "Frontend Developer (React)",
            "WebSolutions • Опубликовано: 10.10.2023",
            "neutral"
        )

        styled_card(
            "Data Scientist",
            "AnalyticsPro • Опубликовано: 05.10.2023",
            "negative"
        )

    # Оборачиваем содержимое в красивый контейнер
    content_container(show_jobs_list)

    # Другой пример контейнера
    with st.container():
        st.markdown('<div class="content-container">', unsafe_allow_html=True)
        st.header("Быстрые действия")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("➕ Добавить вакансию", use_container_width=True)
        with col2:
            st.button("👤 Добавить резюме", use_container_width=True)
        with col3:
            st.button("🔍 Сравнить по ссылкам", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)


# Запуск приложения
if __name__ == "__main__":
    main()
