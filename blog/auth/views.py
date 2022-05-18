from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, login_required

from .forms import *
from blog import db
from .utils import send_reset_email
from blog.models import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data,
                    password=password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт успешно создан', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Регистрация', form=form)


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Логин неверный. Пожалуйста проверьте введенные данные', 'danger')
    return render_template('login.html', title='Войти', form=form)


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))


@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('На почту отправлено письмо с инструкциями по сбросу пароля.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Сброс пароля', form=form)


@auth.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт успешно обновлен!', 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
    return render_template('account.html', title='Аккаунт', form=form)