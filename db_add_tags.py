#!flask/bin/python
from app import db
from app.tag.models import Tag
import json

with open("tags.json", "r") as tag_json:
    tags = json.load(tag_json)

for tag in tags:
    db.session.add(Tag(name=tag["name"]))
    db.session.commit()
