from app import db, api, io, authorization
from sqlalchemy import or_, and_
from flask_restplus import Resource
from datetime import datetime
from flask import abort, request, g
from app.user.decorators import login_required
from app.user.models import User
from models import Message
from serializers import message_model
from config import NUM_PAGES
from flask_socketio import emit, disconnect

messages_api = api.namespace('messages', description='For sending and showing messages between users')

@messages_api.route('')
class UserMessage(Resource):
    
    @messages_api.expect(authorization, message_model)
    @login_required 
    def post(self):
        """
        For sending a new message through HTTP
        """
        data = api.payload
        receiver_id = data.get("receiver_id")
        content = data.get("content")
        if not User.query.get(receiver_id):
            abort(400)
        message = Message(content=content,receiver_id=receiver_id,sender=g.user,sent_at=datetime.utcnow())
        db.session.add(message)
        db.session.commit()
        return {"element": message.to_json()}

@messages_api.route('/<string:reciever_id>','/<string:reciever_id>/<int:page>')
class UserMessages(Resource):
    @messages_api.expect(authorization)
    @login_required
    def get(self, reciever_id, page=0):
        """
        Showing all messages bewteen two users by pages
        """
        messages = Message.query.filter(or_(and_(Message.sender_id == g.user.id, Message.receiver_id == reciever_id),
                                           and_(Message.sender_id == reciever_id, Message.receiver_id == g.user.id)))\
                                           .order_by("id").paginate(page, NUM_PAGES, False).items
        messages.sort(key=lambda message:message.id, reverse=False)
        return {"elements": [element.to_json() for element in messages]}

# SocketIo for messages
@io.on('connect', namespace='/message')
def connect():
    pass

@io.on('disconnect_request', namespace='/message')
def disconnect():
    # delete user
    disconnect()

@io.on('message', namespace='/message')
def handle_message(message):
    print message["data"]
    emit('my_response', {'data': message['data']})

@io.on('my_event', namespace='/message')
def test_message(message):
    request.sid
    print('my_response',{'data': message['data']})
    emit('my_response', {'data': message['data']}, broadcast=True)