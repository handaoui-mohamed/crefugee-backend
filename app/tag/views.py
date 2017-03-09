from app import db, app
from flask import abort, request, jsonify, g
from app.user.models import User
from app.tag.models import Tag

# add auth required and verify admin role

# new tag
@app.route('/api/tags', methods=['GET', 'POST'])
def new_tag():
    if request.method == 'GET':
        return jsonify({'elements': [element.to_json() for element in Tag.query.all()]})
    else:
        data = request.get_json(force=True)
        name = data.get('name')
        pass_code = data.get('pass_code')

        if pass_code is None or name is None or Tag.query.filter_by(name=name).first() is not None:
            abort(400)    # missing arguments or existing one 

        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        return jsonify({'element': tag.to_json()}), 201


@app.route('/api/tags/<int:id>', methods=['GET', 'PUT'])
def edit_tag(id):
    tag = Tag.query.get(id)
    if tag is None:
        abort(400)

    if request.method == 'GET':
        return jsonify({'element': tag.to_json_users()})

    data = request.get_json(force=True)
    name = data.get('name')
    description = data.get('description', tag.description)
    pass_code = data.get('pass_code')

    if pass_code is None:
        abort(400)

    new_tag = False
    existing_tag = Tag.query.filter_by(name=name).first()
    if (existing_tag is None) or (existing_tag.id == tag.id and not (name == tag.name)): new_tag =True

    if new_tag and name: tag.name = name
    db.session.add(tag)
    db.session.commit()
    return jsonify({'element': tag.to_json()})
