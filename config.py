# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))
WTF_CSRF_ENABLED = False
SECRET_KEY = 'k@tj5C:!uj7B}vtJi2p7a0_vGu["x418E=_wU&WohA#>lRYWkX))q5T}h9M_!kskldjfkp'
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    HOST_URL = 'http://localhost:5000/api/v1'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    HOST_URL = 'https://crefugee-api.herokuapp.com/api/v1'
SQLALCHEMY_COMMIT_ON_TEARDOWN=True
SQLALCHEMY_TRACK_MODIFICATIONS=True
ERROR_404_HELP=True
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
CORS_HEADERS = 'Content-Type'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
YEAR = 365
DAY = 24
NUM_PAGES = 10
POSTS_PER_PAGE = 12

#manage.py page 82