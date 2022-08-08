from pydantic import BaseSettings
from decouple import config

class Common(BaseSettings):
    HOST: str = '0.0.0.0'
    PORT: int = 8000


class LocalSettings(Common):
    DEBUG: bool = True
    DB_URI: str = 'postgresql://postgres:root@localhost:5432/ms_auth_db'
    DB_URI: str = 'sqlite:///db.sqlite3'
    
    SECRET_KEY:str = 'someSecretKey'
    ACCESS_TOKEN_EXPIRATION_IN_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRATION_IN_MINUTES: int = 60 * 24 * 3


class DevlopmentSettings(Common):
    DEBUG: bool = True


class TestingSettings(Common):
    DEBUG: bool = True


class StagingSettings(Common):
    DEBUG: bool = True


class ProductionSettings(Common):
    DEBUG: bool = False



if config('ENVIRONMENT') == 'prod':
    Settings = ProductionSettings
elif config('ENVIRONMENT') == 'development':
    Settings = DevlopmentSettings
elif config('ENVIRONMENT') == 'staging':
    Settings = StagingSettings
elif config('ENVIRONMENT') == 'testing':
    Settings = TestingSettings
else:
    Settings = LocalSettings
    

settings = Settings()