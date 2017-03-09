#!flask/bin/python
from coverage import coverage
cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()

import os
import unittest
from datetime import datetime, timedelta

from config import basedir
# from app import app, db
# from app.user.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # def test_avatar(self):
    #     u = User(nickname='john', email='john@example.com')
    #     avatar = u.avatar(128)
    #     expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
    #     assert avatar[0:len(expected)] == expected

    # def test_follow_posts(self):
    #     # assert f4 == [p4]


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
