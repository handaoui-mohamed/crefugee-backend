from app import db, api, io
from flask_restplus import Resource
from datetime import datetime
from flask import abort, request, g
from app.user.auth import login_required
from app.user.models import User
from app.message.models import Message
from config import NUM_PAGES

messages_api = api.namespace('messages', description='For sending and showing messages between users')

@messages_api.route('')
class UserMessage(Resource):
    @login_required 
    def post(self):
        data = request.get_json(force=True)
        receiver_id = data.get("receiver_id")
        content = data.get("content")
        if not receiver_id or not User.query.get(receiver_id) or not content:
            abort(404)
        message = Message(content=content,receiver_id=receiver_id,sender=g.user,sent_at=datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        return {"element": message.to_json()}

@messages_api.route('/<string:reciever_id>','/<string:reciever_id>/<int:page>')
class UserMessages(Resource):
    @login_required
    def get(self, reciever_id, page=0):
        # TODO: everything using one query!!!!!!!
        sender_message = Message.query.filter_by(sender_id=g.user.id, receiver_id=reciever_id).all()
        receiver_message = Message.query.filter_by(sender_id=reciever_id, receiver_id=g.user.id).all()
        messages = sender_message + receiver_message
        messages.sort(key=getKey, reverse=True)
        messages = messages[page*NUM_PAGES: (page +1)*NUM_PAGES]
        messages.sort(key=getKey, reverse=False)

        return {"elements": [element.to_json() for element in messages]}

def getKey(message):
    return message.sent_at

@io.on('connect', namespace='/message')
def connect():
    print request.sid
    print("user connected to messages")
    io.emit("my_response", "hellp")

@io.on('disconnect', namespace='/message')
def disconnect():
    print('Client disconnected from messages')

@io.on('message', namespace='/message')
def handle_message(message):
    print message["data"]
    io.emit('my_response', {'data': message['data']})

@io.on('my_event', namespace='/message')
def test_message(message):
    io.emit('my_response',{'data': message['data']})