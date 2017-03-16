from app import api
from flask_restplus import Resource
from flask import request
from app.contact.forms import ContactForm
from werkzeug.datastructures import MultiDict

mail_api = api.namespace("contact", "For contacting us by mail")

@mail_api.route('')
class Mail(Resource):
    # TODO:for email support go to miguel book page 89
    def post(self):
        data = request.get_json(force=True)
        form = ContactForm(MultiDict(mapping=data))
        if form.validate():
            username = data.get('user_name')
            phone_number = data.get('phone_number')
            email = data.get('email')
            body = data.get('body')
            print data
            return {"success": "Votre message a ete recu, merci"}, 201
        return {"form_errors": form.errors}, 400
