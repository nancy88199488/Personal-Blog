import os

class Config:
    QUOTE_API_BASE_URL ='http://quotes.stormconsultancy.co.uk/random.json'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:nancy@localhost/blog'
    SECRET_KEY = os.environ.get('SECRET_KEY')

    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SENDER_EMAIL = 'nancykemuntosalome@gmail.com'


    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

    
class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    
    

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:nancy@localhost/blog_test'


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:nancy@localhost/blog'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}
