import datetime
import json
import os
from typing import Any, Optional

from resume_analyser.storage.interface import IStorage


class FileStorage(IStorage):
    """Реализация хранилища данных с использованием файлов JSON"""

    def __init__(self, jobs_file="data/jobs.json", resumes_file="data/resumes.json", matches_file="data/matches.json"):
        self.jobs_file = jobs_file
        self.resumes_file = resumes_file
        self.matches_file = matches_file

        # Инициализация файлов, если они не существуют
        if not os.path.exists(jobs_file):
            with open(jobs_file, 'w') as f:
                json.dump([], f)

        if not os.path.exists(resumes_file):
            with open(resumes_file, 'w') as f:
                json.dump([], f)

        if not os.path.exists(matches_file):
            with open(matches_file, 'w') as f:
                json.dump({}, f)

    def _load_jobs(self) -> list[dict[str, Any]]:
        """Загрузить вакансии из файла"""
        with open(self.jobs_file, 'r') as f:
            jobs = json.load(f)

            # Преобразуем строковые даты в объекты datetime.date
            for job in jobs:
                if 'date_posted' in job and isinstance(job['date_posted'], str):
                    job['date_posted'] = datetime.datetime.strptime(
                        job['date_posted'], "%Y-%m-%d").date()

            return jobs

    def _save_jobs(self, jobs: list[dict[str, Any]]) -> None:
        """Сохранить вакансии в файл"""
        # Преобразуем объекты datetime.date в строки
        jobs_to_save = []
        for job in jobs:
            job_copy = job.copy()
            if 'date_posted' in job_copy and isinstance(job_copy['date_posted'], datetime.date):
                job_copy['date_posted'] = job_copy['date_posted'].strftime("%Y-%m-%d")
            jobs_to_save.append(job_copy)

        with open(self.jobs_file, 'w') as f:
            json.dump(jobs_to_save, f, indent=2, ensure_ascii=False)

    def _load_resumes(self) -> list[dict[str, Any]]:
        """Загрузить резюме из файла"""
        with open(self.resumes_file, 'r') as f:
            return json.load(f)

    def _save_resumes(self, resumes: list[dict[str, Any]]) -> None:
        """Сохранить резюме в файл"""
        with open(self.resumes_file, 'w') as f:
            json.dump(resumes, f, indent=2, ensure_ascii=False)

    def _load_matches(self) -> list[dict[str, Any]]:
        """Загрузить оценки соответствия из файла"""
        with open(self.matches_file, 'r') as f:
            return json.load(f)

    def _save_matches(self, matches: list[dict[str, Any]]) -> None:
        """Сохранить оценки соответствия в файл"""
        with open(self.matches_file, 'w') as f:
            json.dump(matches, f, indent=2, ensure_ascii=False)

    def get_all_jobs(self) -> list[dict[str, Any]]:
        return self._load_jobs()

    def get_job_by_id(self, job_id: int) -> Optional[dict[str, Any]]:
        jobs = self._load_jobs()
        for job in jobs:
            if job['id'] == job_id:
                return job
        return None

    def add_job(self, job_data: dict[str, Any]) -> int:
        # todo.md: реализовать
        jobs = self._load_jobs()

        # Назначаем новый ID
        new_id = 1
        if jobs:
            new_id = max(job['id'] for job in jobs) + 1

        # Добавляем дату публикации, если она не указана
        if 'date_posted' not in job_data:
            job_data['date_posted'] = datetime.date.today()

        # Создаем новую запись о вакансии
        new_job = {
            'id': new_id,
            **job_data
        }

        jobs.append(new_job)
        self._save_jobs(jobs)

        return new_id

    def update_job(self, job_id: int, job_data: dict[str, Any]) -> bool:
        jobs = self._load_jobs()

        for i, job in enumerate(jobs):
            if job['id'] == job_id:
                # Обновляем данные, сохраняя ID
                jobs[i] = {**job_data, 'id': job_id}
                self._save_jobs(jobs)
                return True

        return False

    def get_all_resumes(self) -> list[dict[str, Any]]:
        return self._load_resumes()

    def get_resume_by_id(self, resume_id: int) -> Optional[dict[str, Any]]:
        resumes = self._load_resumes()
        for resume in resumes:
            if resume['id'] == resume_id:
                return resume
        return None

    def add_resume(self, resume_data: dict[str, Any]) -> int:
        resumes = self._load_resumes()

        # Назначаем новый ID
        new_id = 1
        if resumes:
            new_id = max(resume['id'] for resume in resumes) + 1

        # Создаем новую запись о резюме
        new_resume = {
            'id': new_id,
            **resume_data
        }

        resumes.append(new_resume)
        self._save_resumes(resumes)

        return new_id

    def update_resume(self, resume_id: int, resume_data: dict[str, Any]) -> bool:
        resumes = self._load_resumes()

        for i, resume in enumerate(resumes):
            if resume['id'] == resume_id:
                # Обновляем данные, сохраняя ID
                resumes[i] = {**resume_data, 'id': resume_id}
                self._save_resumes(resumes)
                return True

        return False

    def update_matches(self, new_matches: list[dict[str, Any]]) -> bool:
        new_ids = {(match['resume_id'], match['job_id']) for match in new_matches}
        existing_matches = [
            match
            for ex_i, match in enumerate(self._load_matches())
            if (match['resume_id'], match['job_id']) not in new_ids
        ]

        self._save_matches(existing_matches + new_matches)

        return True

    def get_matching_resumes(self, job_id: int) -> list[dict[str, Any]]:
        return [match for match in self._load_matches() if match['job_id'] == job_id]

    def get_matching_jobs(self, resume_id: int) -> list[dict[str, Any]]:
        """Получить подходящие резюме для указанной вакансии"""
        return [match for match in self._load_matches() if match['resume_id'] == resume_id]

    def delete_resume(self, resume_id: int) -> bool:
        resumes = self._load_resumes()
        matches = self._load_matches()

        updated_resumes = [resume for resume in resumes if resume['id'] != resume_id]
        self._save_resumes(updated_resumes)

        updated_matches = [match for match in matches if match['resume_id'] != resume_id]
        self.update_matches(new_matches=updated_matches)

        return len(updated_resumes) < len(resumes) and len(updated_matches) < len(matches)

    def delete_job(self, job_id: int) -> bool:
        jobs = self._load_jobs()
        matches = self._load_matches()

        updated_jobs = [job for job in jobs if job['id'] != job_id]
        self._save_jobs(updated_jobs)

        updated_matches = [match for match in matches if match['job_id'] != job_id]
        self.update_matches(new_matches=updated_matches)

        return len(updated_jobs) < len(jobs) and len(updated_matches) < len(matches)
