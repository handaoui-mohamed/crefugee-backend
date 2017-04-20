from app import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    sender_id = db.Column(db.String, db.ForeignKey("user.id"))
    receiver_id = db.Column(db.String)
    content = db.Column(db.String(200))
    sent_at = db.Column(db.DateTime)
 
    def to_json(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content,
            "sent_at": str(self.sent_at)
        }

