#!flask/bin/python
from app import db
from app.tag.models import Tag
from app.user.models import User
from app.role.models import Role
import json
import uuid

# create all tables
db.create_all()

# add tags
with open("tags.json", "r") as tag_json:
    tags = json.load(tag_json)

for tag in tags:
    db.session.add(Tag(name=tag["name"]))
    db.session.commit()

# create roles
user_role = Role(name="User")
moderator_role = Role(name="Moderator")
administrator_role = Role(name="Administrator")
db.session.add(user_role)
db.session.add(moderator_role)
db.session.add(administrator_role)
db.session.commit()

# create super user
super_user = User(id=uuid.uuid4().hex,username="handaoui",email="dm_handaoui@esi.dz",\
            phone_number="0656092713",description="Just an administrator ^_^",\
            address="Domaine Aouf Boualem Bouismail Tipaza",\
            password_hash="$5$rounds=535000$vogLSp3mAM4p/lAl$kVQleIyeJR5z0vNZgvRGWt4w1mGl4GVGQNFu62dyG93",
            full_name="Handaoui Mohamed",validated=True,role=administrator_role)
db.session.add(super_user)
db.session.commit()
super_user.add_tags([1,2,3,4,5])

# create moderator
moderator_user = User(id=uuid.uuid4().hex,username="mohamed",email="handaoui.mohamed@gmail.com",\
            phone_number="0656092713",description="Just a moderator",\
            password_hash="$5$rounds=535000$vogLSp3mAM4p/lAl$kVQleIyeJR5z0vNZgvRGWt4w1mGl4GVGQNFu62dyG93",
            full_name="Handaoui Mohamed",validated=True,role=moderator_role)

db.session.add(super_user)
db.session.add(moderator_user)
db.session.commit()
