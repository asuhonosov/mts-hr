from abc import ABC, abstractmethod
from typing import Any, Optional


class IStorage(ABC):
    """Абстрактный класс для хранилища данных"""

    @abstractmethod
    def get_all_jobs(self) -> list[dict[str, Any]]:
        """Получить все вакансии"""
        pass

    @abstractmethod
    def get_job_by_id(self, job_id: int) -> Optional[dict[str, Any]]:
        """Получить вакансию по ID"""
        pass

    @abstractmethod
    def add_job(self, job_data: dict[str, Any]) -> int:
        """Добавить новую вакансию"""
        pass

    @abstractmethod
    def update_job(self, job_id: int, job_data: dict[str, Any]) -> bool:
        """Обновить существующую вакансию"""
        pass

    @abstractmethod
    def get_all_resumes(self) -> list[dict[str, Any]]:
        """Получить все резюме"""
        pass

    @abstractmethod
    def get_resume_by_id(self, resume_id: int) -> Optional[dict[str, Any]]:
        """Получить резюме по ID"""
        pass

    @abstractmethod
    def add_resume(self, resume_data: dict[str, Any]) -> int:
        """Добавить новое резюме"""
        pass

    @abstractmethod
    def update_resume(self, resume_id: int, resume_data: dict[str, Any]) -> bool:
        """Обновить существующее резюме"""
        pass

    @abstractmethod
    def update_matches(self, new_matches: list[dict[str, Any]]) -> bool:
        """Обновить оценки соответствия между вакансией и резюме"""
        pass

    @abstractmethod
    def get_matching_resumes(self, job_id: int) -> list[dict[str, Any]]:
        """Получить подходящие резюме для указанной вакансии"""
        pass

    @abstractmethod
    def get_matching_jobs(self, resume_id: int) -> list[dict[str, Any]]:
        """Получить подходящие резюме для указанной вакансии"""
        pass

    @abstractmethod
    def delete_resume(self, resume_id: int) -> bool:
        pass

    @abstractmethod
    def delete_job(self, job_id: int) -> bool:
        pass
