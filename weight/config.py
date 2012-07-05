""" Configuration data for weight_app

    :copyright: (c) 2012 by Andreas Madsack.
    :license: BSD, see LICENSE for more details.
"""

import os.path

config_file_path = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    # generated using: import os; os.urandom(24)
    SECRET_KEY = '\xb1D\xaf\x7f\xa2\xd3\xa1\x06,\x95&\xc8\xe3\x1e\xf5\xe6\xc7\x9c\xe5\xb0\x18\x12\xa4L'
    SITE_NAME = 'Weight App'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        config_file_path, 'testing.db')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        config_file_path, 'weight.db')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
