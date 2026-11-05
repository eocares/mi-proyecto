import os
from urllib.parse import quote_plus


def _uri_mysql():
    # Permite sobrescribir con DATABASE_URL completa
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    usuario = os.getenv("DB_USER", "root")
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    host = os.getenv("DB_HOST", "localhost")
    puerto = os.getenv("DB_PORT", "3306")
    nombre = os.getenv("DB_NAME", "contactos_db")
    return f"mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{nombre}?charset=utf8mb4"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-inseguro")
    SQLALCHEMY_DATABASE_URI = _uri_mysql()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True


_CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(nombre=None):
    nombre = nombre or os.getenv("APP_ENV", "development")
    return _CONFIGS.get(nombre, DevelopmentConfig)
