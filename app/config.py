"""
Application Configuration Settings
Module for managing application-wide configuration and environment variables.
"""

import os
from datetime import timedelta


class Config:
    """Base configuration class with default settings."""
    
    # Application Settings
    APP_NAME = "Fantasy F1"
    DEBUG = False
    TESTING = False
    
    # Security Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Database Settings
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///fantasy_f1.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # API Settings
    API_TITLE = "Fantasy F1 API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "API for Fantasy Formula 1 application"
    
    # Cache Settings
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Logging Settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    LOG_MAX_BYTES = 10485760  # 10MB
    LOG_BACKUP_COUNT = 10
    
    # F1 API Settings
    F1_API_BASE_URL = "https://api.formula1.com"
    F1_API_TIMEOUT = 30
    
    # Pagination Settings
    ITEMS_PER_PAGE = 20
    MAX_ITEMS_PER_PAGE = 100
    
    # Email Settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@fantasy-f1.com')


class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')


class TestingConfig(Config):
    """Testing environment configuration."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production environment configuration."""
    
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    # In production, SECRET_KEY must be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required in production")


# Configuration dictionary for easy access
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    Get configuration class based on environment.
    
    Args:
        env (str, optional): Environment name. If not provided, uses FLASK_ENV variable.
    
    Returns:
        Config: Configuration class instance.
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    
    return config.get(env, config['default'])
