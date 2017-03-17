from app import api
from flask_restplus import Resource
from flask import request
from app.contact.forms import ContactForm
from flask_restplus import fields

mail_api = api.namespace("contact", "For contacting us by mail")

mail_model = api.model('Mail', {
    'username': fields.String(required=True),
    'phone_number': fields.String(required=True),
    'email': fields.String(required=True),
    'body': fields.String(required=True)
})

@mail_api.route('')
class Mail(Resource):
    # TODO:for email support go to miguel book page 89
    @mail_api.expect(mail_model)
    def post(self):
        """
        For Sending mails to moderators and administrators
        """
        data = api.payload
        form = ContactForm.from_json(data)
        if form.validate():
            username = data.get('username')
            phone_number = data.get('phone_number')
            email = data.get('email')
            body = data.get('body')
            return {"success": "Votre message a ete recu, merci"}, 201
        return {"form_errors": form.errors}, 400
