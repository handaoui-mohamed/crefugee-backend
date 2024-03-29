#!/usr/bin/env python
import os
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from config import basedir
import wtforms_json
from flask_socketio import SocketIO
from flask_cors import CORS
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

# initialization
app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/v1') 
app.config.from_object('config')
# resfull api
api = Api(blueprint, version='1.0', title='Connected Refugees',
    description='An api for web and mobile app to help connecting refugees and helpers'
)
app.register_blueprint(blueprint)

# authorization header for swagger documentation
authorization = api.parser()
authorization.add_argument('Authorization', help="Always append 'bacon ' before Token",
                             type=str, location='headers', required=True)
# extensions
db = SQLAlchemy(app)

wtforms_json.init()

#socketio
io = SocketIO(app, async_mode=None)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# import APIs
from app.user import views
from app.tag import views
from app.upload import views
from app.contact import views
from app.moderator import views
from app.post import views
from app.message import views
from app.rating import views

# import models
from app.role.models import Role
from app.user.models import User
from app.tag.models import Tag
from app.upload.models import PostUpload, ProfilePicture, LegalDocument
from app.post.models import Post
from app.message.models import Message
from app.rating.models import Rating