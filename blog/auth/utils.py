from flask import url_for
from flask_mail import Message
from blog import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='email@email.com',
                  recipients=[user.email])
    msg.body = f'''Чтобы сбросить пароль, перейдите по следующей ссылке:
    {url_for('users.reset_token', token=token, _external=True)}
    Если вы не отправляли этот запрос, просто проигнорируйте это письмо.'''
    mail.send(msg)