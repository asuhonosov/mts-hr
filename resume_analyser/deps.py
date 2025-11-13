from functools import lru_cache

from resume_analyser.data import DATA_PATH
from resume_analyser.storage.file_storage import FileStorage
from resume_analyser.storage.interface import IStorage


@lru_cache(maxsize=1)
def get_storage() -> IStorage:
    return FileStorage(
        jobs_file=DATA_PATH / 'jobs.json',
        resumes_file=DATA_PATH / 'resumes.json',
        matches_file=DATA_PATH / 'matches.json',
    )
