import os
from constants import *

class Settings:
    def __init__(self):
        self.DATABASE_USER = os.getenv("DATABASE_USER", DATABASE_USER)
        self.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", DATABASE_PASSWORD)
        self.DATABASE_HOST = os.getenv("DATABASE_HOST", DATABASE_HOST)
        self.DATABASE_PORT = os.getenv("DATABASE_PORT", DATABASE_PORT)
        self.DATABASE_NAME = os.getenv("DATABASE_NAME", DATABASE_NAME)
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", DATABASE_NAME_ENVIRONMENT)

    @property
    def DATABASE_URL(self) -> str:
        # return f"mysql+mysqlconnector://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        return f"mysql+aiomysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

    @property
    def is_test(self) -> bool:
        return self.ENVIRONMENT == "test"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

settings = Settings()
