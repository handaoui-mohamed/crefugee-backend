from app import app, db
from datetime import datetime
from flask import abort, request, jsonify, g
from app.user.views import login_required
from app.user.models import User
from app.message.models import Message
from config import NUM_PAGES

@app.route('/api/message', methods=['POST'])
@login_required 
def new_message():
    data = request.get_json(force=True)
    receiver_id = data.get("receiver_id")
    content = data.get("content")
    if not receiver_id or not User.query.get(receiver_id) or not content:
        abort(404)
    message = Message(content=content,receiver_id=receiver_id,sender=g.user,sent_at=datetime.utcnow())
    db.session.add(message)
    db.session.commit()
    return jsonify({"element": message.to_json()})

@app.route('/api/message/<int:user_id>', methods=['GET'])
@app.route('/api/message/<int:user_id>/<int:page>', methods=['GET'])
@login_required
def show_messages(user_id, page=0):
    sender_message = Message.query.filter_by(sender_id=g.user.id, receiver_id=user_id).all()
    receiver_message = Message.query.filter_by(sender_id=user_id, receiver_id=g.user.id).all()
    messages = sender_message + receiver_message
    messages.sort(key=getKey, reverse=True)
    messages = messages[page*NUM_PAGES: (page +1)*NUM_PAGES]
    messages.sort(key=getKey, reverse=False)

    return jsonify({"elements": [element.to_json() for element in messages]})

def getKey(message):
    return message.sent_at



