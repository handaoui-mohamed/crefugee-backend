# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, url_for, request, \
    g, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from flask_login import LoginManager
from app.user.forms import AdminLoginForm
from app.user.models import User


lm = LoginManager()
lm.init_app(app)
lm.login_view = 'index'
lm.login_message = 'Veuillez vous connecter pour acceder a cette page.'

@lm.user_loader
def load_user(id):
    return User.query.get(id)

@app.before_request
def before_request():
    g.user = current_user

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def index():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('non_valid_users'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=form.remember_me.data)
        return redirect(request.args.get('next') or url_for('non_valid_users'))
    # flash("Nom d\'utilisateur ou mot de passe érroné")
    return render_template('index.html',title='Connexion',form=form)


@app.route('/users')
@login_required
def non_valid_users():
    users = User.query.filter_by(validated=False).all()
    return render_template('users.html',title='Validation des Utilisateurs',users=users)

@app.route('/users/<string:id>')
@login_required
def validate_user(id):
    user = User.query.get(id)
    user.validated = True
    db.session.add(user)
    db.session.commit()
    # flash("L\'utilisateur a été valider avec succée")
    return redirect(url_for('non_valid_users'))

@app.route('/users/<int:id>')
@login_required
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    # flash("L\'utilisateur a été supprimer avec succée")
    return redirect(url_for('non_valid_users'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))