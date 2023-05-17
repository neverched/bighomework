from django.conf import settings

from app01.models import ConfirmString
from tools.hash import *

import datetime


def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email_confirm(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '1'

    text_content = '''1\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                       <p>学报，我们走！<a href="{}/#/confirm?code={}" target=blank>1</a>，\
                       </p>
                       <p></p>
                       <p></p>
                       '''.format(settings.FRONTEND, code, 3)  # url must be corrected
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])

    msg.attach_alternative(html_content, "text/html")

    msg.send()
    print("start sending email")
