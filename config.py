import os


class Config(object):
    # SECRET_KEY这个变量配置是对Flask应用非常重要的。Flask的一些扩展用这个作为加密密钥来生成签名或者令牌。
    # Flask-WTF用这个来保护表单避免受到CSRF攻击。
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
