from typing import Literal

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_SCHEME: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str

    SECRET_KEY: str
    ENCRYPT_ALGO: str
    REDIS_HOST: str

    EMAIL_HOST: str
    EMAIL_USER: str
    EMAIL_PASS: str
    EMAIL_PORT: int

    @property
    def DB_URL(self):  # noqa
        return (
            f"{self.DB_SCHEME}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def TEST_DB_URL(self):  # noqa
        return (
            f"{self.DB_SCHEME}://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@"
            f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
