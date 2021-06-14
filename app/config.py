import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Tallie1234'
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['no-reply@tallie.com']
    PRODUCTS_PER_PAGE = 6
    REVIEWS_PER_PAGE = 8

    # ? For sqlite
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(base_dir, 'app.db')
    # ? For postgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:123456@localhost/Tallie'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    IMAGE_SERVICE_URL = 'http://192.168.1.67:5000'
    PAYMENT_SERVICE_URL = 'https://tallie-payment.herokuapp.com'
    SHIPPING_SERVICE_URL = ''