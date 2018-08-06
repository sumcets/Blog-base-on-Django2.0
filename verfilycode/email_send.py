# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 22:47
# @Author  : 张坤
# @File    : email_send.py
# @Software: PyCharm
# @Contact : sumcets@gmail.com
import hashlib

from django.core.mail import send_mail

from myblog_project.settings import EMAIL_FROM


# from myblog.models import VerfilyCode


def send_email(email, request, title, body, code):
    """
    发送验证码
    :param emai:
    :param send_type:
    :return:
    """
    request.session["code"] = code
    request.session['email'] = email

    email_title = title
    email_body = body

    status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if status:
        pass


# 通过hash注册用户的邮箱地址来生成随机用户名
def randomName(email):
    m = hashlib.md5()
    m.update(email.encode('utf-8'))
    return m.hexdigest()


if __name__ == '__main__':
    print(randomName())
