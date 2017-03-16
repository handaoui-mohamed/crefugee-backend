#!flask/bin/python
from app import db
from app.tag.models import Tag
from app.user.models import User
import json
import uuid

with open("tags.json", "r") as tag_json:
    tags = json.load(tag_json)

for tag in tags:
    db.session.add(Tag(name=tag["name"]))
    db.session.commit()

# create super user
user = User(id=uuid.uuid4().hex,username="handaoui",email="dm_handaoui@esi.dz",full_name="Handaoui Mohamed",validated=True,admin=True)
user.hash_password("03041994")
db.session.add(user)
db.session.commit()
