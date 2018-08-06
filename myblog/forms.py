# -*- coding: utf-8 -*-
# @Time    : 2018/7/30 18:50
# @Author  : 张坤
# @File    : forms.py
# @Software: PyCharm
# @Contact : sumcets@gmail.com
from django import forms
from captcha.fields import CaptchaField


class LoginForms(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class RegisterForms(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class ResetLinkForms(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})


class ResetUserInformationForms(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField(required=True, error_messages={'invalid': '验证码错误'})