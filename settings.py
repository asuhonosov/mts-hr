from pydantic_settings import BaseSettings, SettingsConfigDict

from constants import BASE_FOLDER


class YCSettings(BaseSettings):
    token: str
    folder_id: str

    model_config = SettingsConfigDict(
        env_prefix='YC_',
        env_file=BASE_FOLDER / '.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )
