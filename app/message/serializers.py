from app import api
from flask_restplus import fields

message_model = api.model('Message', {
    "reciever_id": fields.String(required=True),
    "content": fields.String(required=True)
})