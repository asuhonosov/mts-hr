import streamlit as st


def apply_custom_css(button_border_color="#ff6b6b", button_hover_border_color="#ff0000",
                     button_text_color="#000000", button_bg_color="#ffffff"):
    """
    Применяет пользовательский CSS для стилизации кнопок.

    Args:
        button_border_color (str): Цвет обводки кнопки в HEX формате
        button_hover_border_color (str): Цвет обводки кнопки при наведении
        button_text_color (str): Цвет текста кнопки
        button_bg_color (str): Цвет фона кнопки
    """

    custom_css = f"""
    <style>
    /* Базовый стиль для всех кнопок Streamlit */
    .stButton > button {{
        border: 1px solid {button_border_color} !important;
        color: {button_text_color} !important;
        background-color: {button_bg_color} !important;
        transition: all 0.3s ease;
    }}

    /* Стиль для кнопок при наведении */
    .stButton > button:hover {{
        border: 2px solid {button_hover_border_color} !important;
        box-shadow: 0 0 5px rgba(255, 0, 0, 0.5);
    }}

    /* Стиль для активных (нажатых) кнопок */
    .stButton > button:active {{
        transform: scale(0.98);
        box-shadow: 0 0 3px rgba(255, 0, 0, 0.7);
    }}
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)


def add_logo_section(company_logo_url=None, product_logo_url=None):
    """
    Добавляет секцию для логотипов в верхней части приложения,
    выравнивая их по центру без текста между ними

    Args:
        company_logo_url (str): URL изображения логотипа компании
        product_logo_url (str): URL изображения логотипа продукта
    """

    # CSS для стилизации верхней панели с логотипами
    logo_css = """
    <style>
    .logo-container {
        display: flex;
        justify-content: right;  /* Центрируем содержимое по горизонтали */
        align-items: left;
        padding: 10px 20px;
        // background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        //box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    .logo-box {
        display: flex;
        align-items: left;
        justify-content: left;
        width: 150px;
        height: 70px;
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        margin: 0 15px;  /* Добавляем отступы между логотипами */
    }

    .logo-box:hover {
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
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
    </style>
    """

    # Формируем HTML в зависимости от наличия логотипов
    company_logo_html = f'<img src="{company_logo_url}" alt="Company Logo" class="logo-img">' if company_logo_url else '<div class="logo-placeholder">Логотип Яндекс</div>'
    product_logo_html = f'<img src="{product_logo_url}" alt="Product Logo" class="logo-img">' if product_logo_url else '<div class="logo-placeholder">Логотип МТС</div>'

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

    # Применяем CSS и HTML
    st.markdown(logo_css, unsafe_allow_html=True)
    st.markdown(logo_html, unsafe_allow_html=True)
