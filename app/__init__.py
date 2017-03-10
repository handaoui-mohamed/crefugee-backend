#!/usr/bin/env python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import basedir
from flask_cors import CORS
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

# initialization
app = Flask(__name__)
app.config.from_object('config')
# extensions
db = SQLAlchemy(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# import APIs
from app.user import views
from app.tag import views
from app.upload import views
from app.contact import views
from app.moderator import views
from app.post import views
from app.message import views

# import models
from app.user.models import User
from app.tag.models import Tag
from app.upload.models import PostUpload, ProfilePicture, LegalDocument
from app.post.models import Post
from app.message.models import Message
