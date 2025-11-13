import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Tuple

from resume_analyser.comparator import compare_job_and_resume_by_text
from tools.run_gpt import ModelRunner


class TextExtractor:
    """Класс для извлечения текста из веб-страниц"""

    @staticmethod
    def extract_text_from_url(url: str) -> str:
        """Извлечь текст с веб-страницы по URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Удаляем скрипты и стили
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text()
            # Очищаем текст от лишних пробелов и переносов строк
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            print(f"Ошибка при загрузке URL: {e}")
            return ""


class DataAnalyzer:
    """Класс для анализа текстовых данных и извлечения информации"""

    @staticmethod
    def extract_job_info_new(job_text: str):
        ...



    @staticmethod
    def extract_job_info(job_text: str) -> Dict[str, Any]:
        """
        Извлечь информацию о вакансии из текста

        В реальном приложении здесь будет интеграция с моделью ML/AI
        Для MVP используем простые эвристики
        """
        # Простой парсер для демонстрации
        lines = job_text.split('\n')

        # Ищем название вакансии в первых 10 строках
        title = "Неизвестная вакансия"
        for i in range(min(10, len(lines))):
            if any(keyword in lines[i].lower() for keyword in
                   ["вакансия", "должность", "позиция", "работа"]):
                title = lines[i].strip()
                break
            elif len(lines[i]) > 5 and len(lines[i]) < 50:
                title = lines[i].strip()
                break

        # Получаем компанию (если есть)
        company = "Неизвестная компания"
        for i in range(min(15, len(lines))):
            if any(keyword in lines[i].lower() for keyword in
                   ["компания", "организация", "фирма"]):
                company = lines[i].strip()
                break

        # Получаем описание (первые 300 символов для краткого описания)
        description = job_text[:500] + "..." if len(job_text) > 500 else job_text

        return {
            "title": title,
            "company": company,
            "description": job_text,
            "short_description": description
        }

    @staticmethod
    def extract_resume_info(resume_text: str) -> Dict[str, Any]:
        """
        Извлечь информацию о резюме из текста

        В реальном приложении здесь будет интеграция с моделью ML/AI
        Для MVP используем простые эвристики
        """
        # Простой парсер для демонстрации
        lines = resume_text.split('\n')

        # Ищем ФИО в первых строках
        name = "Неизвестный кандидат"
        for i in range(min(5, len(lines))):
            words = lines[i].strip().split()
            if 2 <= len(words) <= 4 and all(len(word) > 1 for word in words):
                name = lines[i].strip()
                break

        # Ищем должность
        position = "Неизвестная должность"
        for i in range(min(15, len(lines))):
            if any(keyword in lines[i].lower() for keyword in
                   ["должность", "позиция", "специальность", "профессия"]):
                position = lines[i].strip()
                break

        # Ищем опыт работы
        experience = "Не указан"
        for i in range(len(lines)):
            if "опыт работы" in lines[i].lower() or "стаж" in lines[i].lower():
                parts = lines[i].split(":")
                if len(parts) > 1:
                    experience = parts[1].strip()
                else:
                    # Ищем в следующей строке
                    if i + 1 < len(lines):
                        experience = lines[i + 1].strip()
                break

        return {
            "name": name,
            "position": position,
            "experience": experience,
            "text": resume_text
        }

    @staticmethod
    def calculate_matching_score(job_text: str, resume_text: str) -> float:
        """
        Рассчитать оценку соответствия между вакансией и резюме

        В реальном приложении здесь будет сложный алгоритм
        Для MVP используем простой подход на основе ключевых слов
        """
        # Простой алгоритм для демонстрации
        job_words = set(job_text.lower().split())
        resume_words = set(resume_text.lower().split())

        # Удаляем стоп-слова
        stop_words = {"и", "в", "на", "с", "по", "для", "от", "к", "за", "из", "о", "а", "но", "то"}
        job_words = job_words - stop_words
        resume_words = resume_words - stop_words

        # Находим пересечение слов
        common_words = job_words.intersection(resume_words)

        # Рассчитываем оценку как отношение общих слов к словам в вакансии
        if len(job_words) == 0:
            return 0.0

        return min(1.0, len(common_words) / len(job_words) * 1.5)  # Множитель для более оптимистичной оценки

    @staticmethod
    def compare_resume_job(resume_text: str, job_text: str) -> Dict[str, Any]:
        """
        Сравнить резюме и вакансию и вернуть подробный результат

        В реальном приложении здесь будет интеграция с моделью ML/AI
        Для MVP используем заглушку
        """
        # Эвристики для извлечения ФИО и названия вакансии
        import re

        # Извлекаем ФИО из резюме
        fio_match = re.search(r'([А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?)', resume_text)
        fio = fio_match.group(1) if fio_match else "Не удалось извлечь"

        # Извлекаем название вакансии
        vacancy_match = re.search(r'([А-ЯЁA-Z][^.!?]*?(?:разработчик|инженер|менеджер|специалист|аналитик)[^.!?]*)',
                                  job_text)
        vacancy = vacancy_match.group(1).strip() if vacancy_match else "Не удалось извлечь"

        # Рассчитываем примерный процент соответствия
        match_score = DataAnalyzer.calculate_matching_score(job_text, resume_text)

        # Определяем краткий вывод на основе оценки
        if match_score >= 0.85:
            brief = "да"
        elif match_score >= 0.7:
            brief = "скорее да"
        elif match_score >= 0.5:
            brief = "есть сомнения"
        elif match_score >= 0.3:
            brief = "скорее нет"
        else:
            brief = "нет"

        # Находим положительные части (просто заглушка для MVP)
        positive_parts = []
        if "Python" in resume_text and "Python" in job_text:
            positive_parts.append("Опыт работы с Python")
        if "SQL" in resume_text and "SQL" in job_text:
            positive_parts.append("Опыт работы с SQL")
        if "JavaScript" in resume_text and "JavaScript" in job_text:
            positive_parts.append("Опыт работы с JavaScript")
        if "проект" in resume_text.lower() and "проект" in job_text.lower():
            positive_parts.append("Опыт работы над проектами")
        if "команд" in resume_text.lower() and "команд" in job_text.lower():
            positive_parts.append("Опыт работы в команде")

        # Находим сомнительные части (просто заглушка для MVP)
        doubtful_parts = []
        if "Linux" in job_text and "Linux" not in resume_text:
            doubtful_parts.append("Нет упоминания опыта работы с Linux")
        if "Docker" in job_text and "Docker" not in resume_text:
            doubtful_parts.append("Нет упоминания опыта работы с Docker")
        if "высшее образование" in job_text.lower() and "высшее образование" not in resume_text.lower():
            doubtful_parts.append("Нет упоминания о высшем образовании")

        return {
            "размышения о кандидате": f"Кандидат имеет определенный опыт и навыки, которые соответствуют вакансии на {int(match_score * 100)}%. Стоит обратить внимание на ключевые требования и соответствие опыта работы.",
            "ФИО кандидата": fio,
            "вакансия": vacancy,
            "вывод кратко": brief,
            "вывод текстом": f"На основе анализа резюме и требований вакансии, кандидат соответствует на {int(match_score * 100)}%. {'Рекомендуется пригласить на интервью.' if match_score >= 0.5 else 'Рекомендуется рассмотреть других кандидатов.'}",
            "положительные части резюме": positive_parts,
            "сомнительные части резюме": doubtful_parts
        }


class MatchingEngine:
    """Класс для переранжирования и сравнения резюме с вакансиями"""

    @staticmethod
    def rerank_resumes_for_job(model: ModelRunner, job_id: int, job_text: str, resumes: List[Dict[str, Any]], verbose: bool = False) -> list[dict[str, Any]]:
        """
        Переранжировать резюме для данной вакансии

        Возвращает словарь {resume_id: match_score}
        """
        matches = []

        for resume in resumes:
            if verbose:
                print('  > ', resume['name'])

            resume_id = resume['id']
            resume_text = resume['full_description']

            # Рассчитываем оценку соответствия
            comparison = compare_job_and_resume_by_text(model=model, job_text=job_text, resume_text=resume_text)
            matches.append({
                'resume_id': resume_id,
                'job_id': job_id,
                **comparison,
            })

        return matches

    @staticmethod
    def rerank_jobs_for_resume(model: ModelRunner, resume_id: int, resume_text: str, jobs: List[Dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Переранжировать вакансии для данного резюме

        Возвращает словарь {job_id: match_score}
        """
        matches = []

        for job in jobs:
            job_id = job['id']
            job_text = job['full_description']

            comparison = compare_job_and_resume_by_text(model=model, job_text=job_text, resume_text=resume_text)
            matches.append({
                'resume_id': resume_id,
                'job_id': job_id,
                **comparison,
            })

        return matches
