from random import *

from django.conf import settings

from app01.models import ConfirmString


def generate_random_str(randomlength=16):
    """
  生成一个指定长度的随机字符串
  """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[randint(0, length)]
    return random_str


def make_confirm_string(user):
    # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = generate_random_str(5)
    ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email_confirm(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '1'

    text_content = '''1\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''
    html_content = '''
                       <p>学报，我们走！验证码为{},有效期{}天，\
                       </p>
                       <p></p>
                       <p></p>
                       '''.format(code, 3)  # url must be corrected
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])

    msg.attach_alternative(html_content, "text/html")

    msg.send()
    print("start sending email")
