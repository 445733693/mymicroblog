import os

# 获取项目的根目录
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SECRET_KEY这个变量配置是对Flask应用非常重要的。Flask的一些扩展用这个作为加密密钥来生成签名或者令牌。
    # Flask-WTF用这个来保护表单避免受到CSRF攻击。
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # 数据库配置
    # 默认使用SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 不需要每次数据库变更时都发信号给应用

